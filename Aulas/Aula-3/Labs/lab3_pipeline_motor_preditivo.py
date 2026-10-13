# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC # LAB 3 — Mão na massa: do evento ao score de risco
# MAGIC ### Databricks Free Edition · Lote + streaming → Bronze → Silver → Gold → motor preditivo
# MAGIC
# MAGIC **O que este notebook faz:** coloca em execução, em escala de laboratório, o pipeline que
# MAGIC vocês desenharam na primeira parte do Lab 3 para o domínio **Operação/Frota** da LODLog:
# MAGIC
# MAGIC | Fonte | Tipo | Como chega | Padrão de ingestão |
# MAGIC |---|---|---|---|
# MAGIC | Entregas do TMS | estruturada (CSV) | um arquivo por dia | **lote** (ELT) |
# MAGIC | Telemetria IoT dos caminhões | semiestruturada (JSON) | arquivos pequenos a cada poucos segundos | **streaming** (micro-lotes) |
# MAGIC
# MAGIC No fim, um **motor preditivo já pronto** — entregue pelo time de Ciência de Dados da LODLog —
# MAGIC lê a camada Gold e calcula o **risco de atraso** de cada entrega. Vocês **não** criam features
# MAGIC nem treinam modelo: vocês operam o pipeline, observam o que cada camada faz e interpretam o
# MAGIC resultado como gestores.
# MAGIC
# MAGIC **Como executar:** Databricks Free Edition (https://login.databricks.com) → Workspace → Import →
# MAGIC este arquivo `.py` → **Run All** (~2 min, compute Serverless). Depois faça os exercícios do fim.

# COMMAND ----------

# ─────────────────────────────────────────────────────────────
# CÉLULA 0 — Catálogo, schema e Volume
# O Volume do Unity Catalog é a "pasta de chegada" (landing) dos arquivos.
# ─────────────────────────────────────────────────────────────
CATALOG = "workspace"
SCHEMA = "lodlog_lab3"
VOL = f"/Volumes/{CATALOG}/{SCHEMA}/landing"   # fora do try: o caminho existe nos dois ambientes

try:
    spark.sql(f"USE CATALOG {CATALOG}")
except Exception as e:
    print(f"Aviso: seguindo com o catálogo padrão ({e})")

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {SCHEMA}")
try:
    spark.sql(f"CREATE VOLUME IF NOT EXISTS {SCHEMA}.landing")
except Exception as e:
    print(f"Aviso: Volume não criado ({e})")
spark.sql(f"USE {SCHEMA}")

# Recomeça do zero a cada Run All (o laboratório é idempotente)
for t in ["bronze_tms_entregas", "bronze_iot_eventos", "silver_tms_entregas", "silver_iot_eventos",
          "gold_entregas_contexto", "gold_score_risco"]:
    spark.sql(f"DROP TABLE IF EXISTS {SCHEMA}.{t}")
try:
    dbutils.fs.rm(VOL, True)
except NameError:
    import shutil
    shutil.rmtree(VOL, ignore_errors=True)
print(f"Schema {SCHEMA} pronto · landing em {VOL}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 1 — As fontes chegam à landing
# MAGIC
# MAGIC Geramos um dia de operação de 40 caminhões. Os dados vêm **com os problemas de sempre**:
# MAGIC entregas duplicadas, distâncias negativas, sensores com leitura absurda (999 °C) e eventos
# MAGIC repetidos. É o que um pipeline real recebe — e é por isso que existem camadas.

# COMMAND ----------

import csv
import json
import os
import random
from datetime import datetime, timedelta

random.seed(7)
DIA = datetime(2026, 11, 16)
VEICULOS = [f"TRK-{i:04d}" for i in range(1, 41)]
CDS = ["CD-SP", "CD-RJ", "CD-BH", "CD-CWB", "CD-POA"]


def gravar(caminho, texto):
    try:
        dbutils.fs.put(caminho, texto, True)
    except NameError:
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(texto)


# ── Fonte 1 · ESTRUTURADA: entregas do TMS (um CSV por dia) ──
linhas = [["entrega_id", "veiculo_id", "cd_origem", "distancia_km", "peso_kg", "hora_saida", "prazo_min"]]
for i in range(1, 801):
    linhas.append([f"ENT-{i:05d}", random.choice(VEICULOS), random.choice(CDS),
                   round(random.uniform(5, 420), 1), round(random.uniform(80, 9000), 0),
                   random.choice(range(5, 21)), random.choice([120, 240, 480, 720])])
linhas += [linhas[10], linhas[11], linhas[12]]                       # 3 duplicatas
linhas[20][3], linhas[21][4] = -35.0, -120.0                          # 2 valores negativos
buf = []
for l in linhas:
    buf.append(",".join(str(x) for x in l))
gravar(f"{VOL}/tms/entregas_2026-11-16.csv", "\n".join(buf) + "\n")


# ── Fonte 2 · SEMIESTRUTURADA: telemetria IoT (JSON, chega em micro-lotes) ──
def lote_iot(n_lote, n_eventos):
    eventos = []
    for _ in range(n_eventos):
        ts = DIA + timedelta(hours=random.uniform(5, 22))
        ev = {"veiculo_id": random.choice(VEICULOS), "ts": ts.isoformat(),
              "velocidade_kmh": round(random.uniform(0, 110), 1),
              "temperatura_motor_c": round(random.gauss(92, 8), 1),
              "parado": random.random() < 0.18}
        if random.random() < 0.02:
            ev["temperatura_motor_c"] = 999.0                          # sensor com defeito
        eventos.append(ev)
    eventos += eventos[:5]                                             # reenvio duplicado
    gravar(f"{VOL}/iot/lote_{n_lote:02d}.json", "\n".join(json.dumps(e) for e in eventos) + "\n")


for n in (1, 2, 3):
    lote_iot(n, 1200)
print("Landing: 1 CSV do TMS + 3 micro-lotes JSON de IoT")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 2 — Bronze: carregar cru (ELT)
# MAGIC
# MAGIC **Lote (TMS):** lê o CSV do dia e grava como está, com a origem e a hora da carga.
# MAGIC **Streaming (IoT):** o Structured Streaming lê só os arquivos novos da pasta e anota no
# MAGIC *checkpoint* o que já processou. `availableNow` processa tudo o que chegou e para — é como um
# MAGIC streaming que você liga de tempos em tempos (no Databricks pago, ficaria sempre ligado).

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.types import BooleanType, DoubleType, StringType, StructField, StructType

# Lote — TMS
bronze_tms = (spark.read.option("header", True).option("inferSchema", True).csv(f"{VOL}/tms/")
              .withColumn("_origem", F.lit("tms_csv"))
              .withColumn("_carga_em", F.current_timestamp()))
bronze_tms.write.format("delta").mode("overwrite").saveAsTable(f"{SCHEMA}.bronze_tms_entregas")

# Streaming — IoT
SCHEMA_IOT = StructType([StructField("veiculo_id", StringType()), StructField("ts", StringType()),
                         StructField("velocidade_kmh", DoubleType()),
                         StructField("temperatura_motor_c", DoubleType()),
                         StructField("parado", BooleanType())])


def rodar_stream_iot():
    """Processa os micro-lotes novos da landing para a Bronze e para."""
    q = (spark.readStream.schema(SCHEMA_IOT).json(f"{VOL}/iot/")
         .withColumn("_carga_em", F.current_timestamp())
         .writeStream.format("delta")
         .option("checkpointLocation", f"{VOL}/_checkpoints/bronze_iot")
         .trigger(availableNow=True)
         .toTable(f"{SCHEMA}.bronze_iot_eventos"))
    q.awaitTermination()


rodar_stream_iot()
print("Bronze TMS:", spark.table(f"{SCHEMA}.bronze_tms_entregas").count(), "linhas")
print("Bronze IoT:", spark.table(f"{SCHEMA}.bronze_iot_eventos").count(), "eventos")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 3 — Silver: limpar e barrar o que não presta
# MAGIC
# MAGIC Aqui entram as regras de qualidade: sem duplicatas, sem distâncias ou pesos negativos, sem
# MAGIC leituras de sensor fora da faixa física (velocidade 0–200 km/h, motor 50–150 °C).
# MAGIC A Bronze continua guardando tudo — se a regra mudar, reprocessamos a partir dela.

# COMMAND ----------

def construir_silver():
    tms = spark.table(f"{SCHEMA}.bronze_tms_entregas")
    silver_tms = (tms.dropDuplicates(["entrega_id"])
                  .filter((F.col("distancia_km") > 0) & (F.col("peso_kg") > 0)))
    silver_tms.write.format("delta").mode("overwrite").saveAsTable(f"{SCHEMA}.silver_tms_entregas")

    iot = spark.table(f"{SCHEMA}.bronze_iot_eventos")
    silver_iot = (iot.dropDuplicates(["veiculo_id", "ts"])
                  .filter(F.col("velocidade_kmh").between(0, 200) &
                          F.col("temperatura_motor_c").between(50, 150))
                  .withColumn("ts", F.to_timestamp("ts")))
    silver_iot.write.format("delta").mode("overwrite").saveAsTable(f"{SCHEMA}.silver_iot_eventos")

    for camada in ("tms_entregas", "iot_eventos"):
        b = spark.table(f"{SCHEMA}.bronze_{camada}").count()
        s = spark.table(f"{SCHEMA}.silver_{camada}").count()
        print(f"{camada:13s} Bronze {b:6d} → Silver {s:6d}  (barrados: {b - s})")


construir_silver()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 4 — Gold: a tabela que o negócio (e o modelo) consome
# MAGIC
# MAGIC Uma linha por entrega, com o contexto do caminhão no dia: temperatura média do motor,
# MAGIC % do tempo parado e velocidade média. Esta tabela é o **contrato** entre a engenharia de
# MAGIC dados e o time de Ciência de Dados: colunas, tipos e significado combinados.

# COMMAND ----------

def construir_gold():
    contexto_frota = (spark.table(f"{SCHEMA}.silver_iot_eventos")
                      .groupBy("veiculo_id")
                      .agg(F.round(F.avg("temperatura_motor_c"), 1).alias("temp_media_motor_c"),
                           F.round(F.avg(F.col("parado").cast("int")) * 100, 1).alias("pct_tempo_parado"),
                           F.round(F.avg("velocidade_kmh"), 1).alias("velocidade_media_kmh"),
                           F.count("*").alias("eventos_iot")))
    gold = (spark.table(f"{SCHEMA}.silver_tms_entregas")
            .join(contexto_frota, "veiculo_id", "left")
            .withColumn("saida_horario_pico", F.col("hora_saida").isin(7, 8, 17, 18, 19).cast("int"))
            .select("entrega_id", "veiculo_id", "cd_origem", "distancia_km", "peso_kg", "prazo_min",
                    "saida_horario_pico", "temp_media_motor_c", "pct_tempo_parado",
                    "velocidade_media_kmh", "eventos_iot"))
    gold.write.format("delta").mode("overwrite").saveAsTable(f"{SCHEMA}.gold_entregas_contexto")
    print("Gold:", gold.count(), "entregas com contexto da frota")


construir_gold()
display(spark.table(f"{SCHEMA}.gold_entregas_contexto").limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 5 — Motor preditivo (pronto): risco de atraso
# MAGIC
# MAGIC O time de Ciência de Dados entregou o **modelo `risco_atraso` v1.2** (regressão logística
# MAGIC treinada com o histórico 2024–2026). Ele chega como uma lista de pesos — vocês só o
# MAGIC **aplicam** sobre a Gold. Peso positivo aumenta o risco; negativo, diminui.
# MAGIC
# MAGIC O resultado vira a tabela `gold_score_risco`, que alimentaria o painel do supervisor de
# MAGIC frota. **O limiar de alerta é uma decisão de negócio**, não do modelo — é o primeiro
# MAGIC exercício.

# COMMAND ----------

MODELO_RISCO_ATRASO_V1_2 = {          # entregue pelo time de Ciência de Dados — não alterar
    "intercepto": -4.10,
    "distancia_km": 0.0085,
    "peso_kg": 0.00012,
    "saida_horario_pico": 0.90,
    "temp_media_motor_c": 0.012,
    "pct_tempo_parado": 0.045,
    "prazo_min": -0.0021,
}
LIMIAR_ALERTA = 0.60                  # ← exercício 1: experimente 0.40 e 0.80


def aplicar_motor(limiar=LIMIAR_ALERTA):
    m = MODELO_RISCO_ATRASO_V1_2
    z = F.lit(m["intercepto"])
    for coluna, peso in m.items():
        if coluna != "intercepto":
            z = z + F.lit(peso) * F.coalesce(F.col(coluna).cast("double"), F.lit(0.0))
    score = (spark.table(f"{SCHEMA}.gold_entregas_contexto")
             .withColumn("prob_atraso", F.round(1 / (1 + F.exp(-z)), 3))
             .withColumn("alerta", (F.col("prob_atraso") >= limiar).cast("int"))
             .withColumn("modelo_versao", F.lit("risco_atraso v1.2"))
             .withColumn("limiar_usado", F.lit(limiar))
             .withColumn("calculado_em", F.current_timestamp()))
    score.write.format("delta").mode("overwrite").saveAsTable(f"{SCHEMA}.gold_score_risco")
    resumo = score.agg(F.count("*").alias("entregas"), F.sum("alerta").alias("alertas"),
                       F.round(F.avg("prob_atraso"), 3).alias("prob_media")).collect()[0]
    print(f"Limiar {limiar:.2f}: {resumo['alertas']} alertas em {resumo['entregas']} entregas "
          f"(probabilidade média {resumo['prob_media']})")


aplicar_motor()
display(spark.sql(f"""
    SELECT cd_origem, COUNT(*) AS entregas, SUM(alerta) AS alertas,
           ROUND(AVG(prob_atraso), 3) AS prob_media
    FROM {SCHEMA}.gold_score_risco GROUP BY cd_origem ORDER BY alertas DESC"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 6 — Chegou mais telemetria (simulação de streaming)
# MAGIC
# MAGIC Rode a célula abaixo: ela deixa um **4º micro-lote** na landing e reprocessa o pipeline.
# MAGIC Observe que o streaming lê **só o arquivo novo** (o checkpoint lembra dos anteriores) e que o
# MAGIC score muda sem ninguém reextrair nada da origem.

# COMMAND ----------

lote_iot(4, 1200)
rodar_stream_iot()
print("Bronze IoT agora:", spark.table(f"{SCHEMA}.bronze_iot_eventos").count(), "eventos")
construir_silver()
construir_gold()
aplicar_motor()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 7 — Auditoria: o que aconteceria sem a Silver?
# MAGIC
# MAGIC A consulta abaixo aplica o mesmo modelo direto sobre a **Bronze** (sem limpeza) e compara
# MAGIC com o resultado oficial. É o argumento de negócio para as regras de qualidade.

# COMMAND ----------

display(spark.sql(f"""
    SELECT 'Bronze (sem regras)'   AS origem,
           ROUND(AVG(temperatura_motor_c), 1) AS temp_media_c,
           SUM(CASE WHEN temperatura_motor_c > 150 THEN 1 ELSE 0 END) AS leituras_absurdas
    FROM {SCHEMA}.bronze_iot_eventos
    UNION ALL
    SELECT 'Silver (com regras)', ROUND(AVG(temperatura_motor_c), 1),
           SUM(CASE WHEN temperatura_motor_c > 150 THEN 1 ELSE 0 END)
    FROM {SCHEMA}.silver_iot_eventos"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Exercícios (anotem as respostas no notebook do grupo)
# MAGIC
# MAGIC 1. **Limiar é decisão de negócio.** Rode `aplicar_motor(0.40)` e `aplicar_motor(0.80)` numa
# MAGIC    célula nova. Quantos alertas cada um gera? Se o supervisor só consegue tratar 30 alertas
# MAGIC    por dia, qual limiar vocês defenderiam — e qual risco aceitam?
# MAGIC 2. **Lote × streaming.** Qual fonte entrou em lote e qual em streaming? Se o score fosse usado
# MAGIC    para replanejar a rota **durante** a viagem, o TMS poderia continuar em lote diário? Que
# MAGIC    padrão vocês usariam (CDC? micro-lote?) e por quê?
# MAGIC 3. **Qualidade.** Quantos registros cada Silver barrou (Etapa 3)? Pela Etapa 7, o que a leitura
# MAGIC    de 999 °C faria com a temperatura média — e com o risco — se fosse direto para a Gold?
# MAGIC 4. **Reprocessamento.** Na Etapa 6, por que não foi preciso reler os lotes 1–3? O que mudaria
# MAGIC    se a regra de temperatura da Silver passasse de 150 °C para 130 °C?
# MAGIC 5. **Ferramenta por camada.** Para cada etapa deste notebook, anotem o serviço que fariam em
# MAGIC    produção na nuvem escolhida pelo grupo (ex.: landing → S3/ADLS; streaming → Kinesis/Event
# MAGIC    Hubs/Pub/Sub + Structured Streaming; motor → endpoint de modelo). Levem isso para a matriz.
# MAGIC
# MAGIC > Fora do escopo desta disciplina: criar features e treinar o modelo — isso é tarefa das
# MAGIC > disciplinas de Ciência de Dados. Aqui o modelo é um **consumidor** da Gold, como um
# MAGIC > dashboard: o que importa é a Gold ser confiável, documentada e chegar a tempo.
