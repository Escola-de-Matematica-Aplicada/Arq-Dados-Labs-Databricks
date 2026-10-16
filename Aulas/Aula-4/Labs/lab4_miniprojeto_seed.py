# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC # LAB 4 — Seed do Miniprojeto: o Data Lake da LODLog (70% pronto · 30% do grupo)
# MAGIC ### Databricks Free Edition · Arquitetura Medallion (Bronze → Silver → Gold)
# MAGIC
# MAGIC **Como este notebook funciona.** Ele já traz **70% do data lake pronto e explicado**: seis fontes
# MAGIC da LODLog (estruturadas, semiestruturadas e não estruturadas), todas carregadas na Bronze, quatro
# MAGIC delas tratadas na Silver, uma Gold de referência e um exemplo de análise e de governança.
# MAGIC Os **30% restantes são do grupo** e estão marcados com **🟨 TODO**. São quatro, todos curtos:
# MAGIC
# MAGIC | TODO | O que o grupo faz | Onde | Tempo sugerido |
# MAGIC |---|---|---|---|
# MAGIC | **1** | Leva **uma fonte semi/não estruturada** até a Silver, decidindo as regras de qualidade | Etapa 4 | 20 min |
# MAGIC | **2** | Constrói a **Gold do seu cenário**, escrevendo a métrica-chave | Etapa 5 | 25 min |
# MAGIC | **3** | Conduz a **análise**: pergunta de negócio, consulta e interpretação | Etapa 6 | 25 min |
# MAGIC | **4** | Aplica **governança mínima** na Gold do grupo (dono, PII, retenção, regra de qualidade) | Etapa 7 | 15 min |
# MAGIC
# MAGIC A **Etapa 8** confere sozinha o que falta e imprime os números para o pitch.
# MAGIC
# MAGIC **Como executar:**
# MAGIC 1. Login no Databricks Free Edition — https://login.databricks.com (compute Serverless).
# MAGIC 2. Workspace › Import › este arquivo › **Run All** (~2 min). Ele roda inteiro mesmo antes dos TODOs —
# MAGIC    as partes do grupo só ficam "em branco" até vocês preencherem.
# MAGIC 3. Preencham os TODOs **na ordem** e rodem de novo a partir da célula editada (ou Run All).
# MAGIC
# MAGIC > 💡 *Vocês não precisam escrever pipeline do zero. O trabalho de vocês é o de um líder de dados:
# MAGIC > decidir regras, escolher a métrica que responde ao negócio, interpretar o número e assumir a governança.*

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🟨 Decisão inicial do grupo — o cenário
# MAGIC
# MAGIC | Cenário | Pergunta de negócio (do caso LODLog) | Fonte extra recomendada para o TODO 1 |
# MAGIC |---|---|---|
# MAGIC | **A — Rotas de entrega** | Como reduzir os 23% de atraso e as multas de R$ 4,2 MM/ano? | `clima` (API externa, JSON) |
# MAGIC | **B — Manutenção preditiva** | Como evitar quebras e R$ 2,1 MM/ano em reboque? | `ocorrencias` (texto livre dos motoristas) |
# MAGIC | **C — Estoque e reposição** | Como evitar ruptura e +R$ 1,8 MM em horas extras? | `clima` (API externa, JSON) |
# MAGIC | **D — Fraude em faturamento** | Como detectar divergências entre TMS e ERP? | `ocorrencias` (texto livre dos motoristas) |

# COMMAND ----------

# 🟨 TODO (decisão do grupo): escolha o cenário — "A", "B", "C" ou "D"
CENARIO = None

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 0 — Catálogo e schemas (pronto)
# MAGIC
# MAGIC Um schema por camada espelha as **zonas do data lake** vistas na Aula 2: a Bronze guarda o dado
# MAGIC como chegou, a Silver o dado confiável e a Gold o dado pronto para o consumo.

# COMMAND ----------

CATALOG = "workspace"
try:
    spark.sql(f"USE CATALOG {CATALOG}")
    print(f"Catálogo ativo: {CATALOG}")
except Exception as e:
    print(f"Aviso: seguindo com o catálogo padrão ({str(e).splitlines()[0]})")

for camada in ["lodlog_bronze", "lodlog_silver", "lodlog_gold"]:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {camada}")
print("Schemas prontos: lodlog_bronze · lodlog_silver · lodlog_gold")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 1 — As seis fontes da LODLog (pronto)
# MAGIC
# MAGIC Na vida real cada fonte chega por um caminho diferente — a telemetria IoT por **streaming** (como no
# MAGIC Lab 3), os sistemas internos por **batch/CDC**, a API de clima por chamadas diárias. Aqui nós
# MAGIC **geramos** os dados, mas com o formato e a sujeira do mundo real: campos faltando, duplicatas,
# MAGIC valores absurdos, chaves órfãs e texto livre.
# MAGIC
# MAGIC | # | Fonte | Sistema | Tipo de dado | Ingestão típica |
# MAGIC |---|---|---|---|---|
# MAGIC | 1 | Telemetria da frota | IoT | **semiestruturado** (JSON) | streaming |
# MAGIC | 2 | Entregas | TMS | estruturado | batch / CDC |
# MAGIC | 3 | Faturas | ERP | estruturado | batch diário |
# MAGIC | 4 | Posição de estoque | WMS | estruturado | batch diário |
# MAGIC | 5 | Clima por CD | API externa (INMET) | **semiestruturado** (JSON) | batch diário |
# MAGIC | 6 | Ocorrências dos motoristas | App do motorista | **não estruturado** (texto livre) | micro-batch |
# MAGIC
# MAGIC > Os dados têm **padrões escondidos** que a análise do grupo pode descobrir — não leia o código
# MAGIC > gerador procurando a resposta; descubra pelos dados, como faria na empresa.

# COMMAND ----------

import json
import random
from datetime import date, datetime, timedelta

random.seed(2026)
BASE = date(2026, 8, 1)
DIAS = 60
CDS = {1: "São Paulo", 2: "Campinas", 3: "Rio de Janeiro", 4: "Belo Horizonte", 5: "Curitiba"}
_perfil = random.Random(7)                       # perfis de comportamento da frota e da carteira
VEICULOS_ATENCAO = set(_perfil.sample(range(1, 51), 3))
CLIENTES_ATENCAO = set(_perfil.sample(range(1, 201), 2))

# chuva "verdadeira" por CD e dia — base comum para clima, atrasos e rupturas
chuva = {}
for cd in CDS:
    for d in range(DIAS):
        mm = random.choice([0, 0, 0, 0, 0, 2, 5, 12, 25, 45, 70])
        chuva[(cd, d)] = round(mm * (1.5 if cd == 3 else 1.0) * random.uniform(0.8, 1.2), 1)

# ── Fonte 1 · IoT (JSON) ──
iot_raw = []
for _ in range(20_000):
    v = random.randint(1, 50)
    ts = datetime(2026, 8, 1, 5) + timedelta(minutes=random.randint(0, 60 * 24 * DIAS - 1))
    temp = random.gauss(104, 7) if v in VEICULOS_ATENCAO else random.gauss(92, 5)
    ev = {"veiculo_id": v, "ts": ts.strftime("%Y-%m-%dT%H:%M:%S"),
          "gps": {"lat": round(random.uniform(-30.0, -19.0), 6), "lon": round(random.uniform(-51.5, -43.0), 6)},
          "velocidade_kmh": round(random.uniform(0, 110), 1),
          "temperatura_motor_c": round(temp, 1),
          "nivel_combustivel_pct": round(random.uniform(5, 100), 1)}
    r = random.random()
    if r < 0.02:
        ev.pop("temperatura_motor_c")            # sensor falhou
    elif r < 0.03:
        ev["velocidade_kmh"] = 977.0             # leitura absurda
    elif r < 0.05:
        iot_raw.append(json.dumps(ev))           # evento duplicado
    iot_raw.append(json.dumps(ev))

# ── Fonte 2 · TMS entregas (estruturado, chega como texto de um extrato) ──
tms_raw = []
for eid in range(1, 6_001):
    cd = random.randint(1, 5)
    d = random.randint(0, DIAS - 1)
    v = random.randint(1, 50)
    prevista = BASE + timedelta(days=d)
    p_atraso = 0.12 + (0.35 if chuva[(cd, d)] > 30 else 0) + (0.20 if v in VEICULOS_ATENCAO else 0)
    status = random.choices(["Entregue", "Cancelado", "Em rota"], [0.93, 0.04, 0.03])[0]
    entrega = None
    if status == "Entregue":
        entrega = prevista + timedelta(days=random.randint(1, 3) if random.random() < p_atraso else 0)
    valor = round(random.uniform(120, 4800), 2)
    if random.random() < 0.005:
        valor = -valor                           # valor negativo (erro de digitação)
    linha = (str(eid), f"PED-2026-{eid:06d}", str(random.randint(1, 200)), str(cd), str(v),
             str(random.randint(1, 80)), prevista.isoformat(), entrega.isoformat() if entrega else "",
             status, f"{valor:.2f}", f"{random.uniform(8, 420):.1f}")
    tms_raw.append(linha)
    if random.random() < 0.01:
        tms_raw.append(linha)                    # reenvio duplicado do extrato

# ── Fonte 3 · ERP faturas (estruturado) ──
erp_raw = []
fid = 0
for l in {l[0]: l for l in tms_raw}.values():      # 1 fatura por entrega entregue
    if l[8] != "Entregue":
        continue
    fid += 1
    valor = abs(float(l[9]))
    p_div = 0.45 if int(l[2]) in CLIENTES_ATENCAO else 0.015
    faturado = round(valor * random.uniform(1.08, 1.45), 2) if random.random() < p_div else valor
    erp_raw.append((str(fid), l[0], l[2], f"{faturado:.2f}", l[7]))
for _ in range(30):                                # faturas órfãs (entrega inexistente)
    fid += 1
    erp_raw.append((str(fid), str(random.randint(90_000, 99_999)), str(random.randint(1, 200)),
                    f"{random.uniform(200, 3000):.2f}", (BASE + timedelta(days=random.randint(0, DIAS - 1))).isoformat()))

# ── Fonte 4 · WMS estoque (estruturado, foto diária por CD × SKU) ──
wms_raw = []
for cd in CDS:
    for sku in range(1, 21):
        for d in range(DIAS):
            demanda = random.randint(5, 40)
            p_rupt = 0.04 + (0.25 if chuva[(cd, d)] > 30 else 0) + (0.10 if cd == 3 and sku <= 4 else 0)
            saldo = 0 if random.random() < p_rupt else random.randint(demanda, demanda * 6)
            if random.random() < 0.005:
                saldo = -random.randint(1, 50)   # saldo negativo (erro de inventário)
            wms_raw.append((str(cd), f"SKU-{sku:03d}", (BASE + timedelta(days=d)).isoformat(),
                            str(saldo), str(demanda), str(demanda * 2)))

# ── Fonte 5 · API de clima (JSON externo) ──
clima_raw = []
for (cd, d), mm in chuva.items():
    reg = {"estacao": f"INMET-A7{cd:02d}", "cd_id": cd, "data": (BASE + timedelta(days=d)).isoformat(),
           "medicoes": {"chuva_mm": mm, "temp_max_c": round(random.uniform(17, 34), 1)},
           "alerta": "laranja" if mm > 45 else ("amarelo" if mm > 25 else None)}
    r = random.random()
    if r < 0.03:
        reg["medicoes"].pop("chuva_mm")          # medição ausente
    elif r < 0.05:
        reg["medicoes"]["chuva_mm"] = 9999.0     # código de erro do sensor
    elif r < 0.08:
        clima_raw.append(json.dumps(reg))        # resposta duplicada da API
    clima_raw.append(json.dumps(reg))

# ── Fonte 6 · Ocorrências (texto livre) ──
TEXTOS = {
    "mecanica": ["Motor esquentando na subida, parei pra esfriar", "luz do painel acesa e barulho no motor",
                 "freio fazendo barulho estranho", "superaquecimento de novo, temperatura no talo",
                 "pneu furado na BR-116, troquei no acostamento"],
    "clima_transito": ["chuva forte, via alagada, esperei baixar", "transito parado na marginal por acidente",
                       "temporal na serra, reduzi a velocidade", "engarrafamento na entrada do CD"],
    "cobranca": ["cliente reclamou do valor cobrado na nota", "cliente diz que a cobrança veio em duplicidade",
                 "nota fiscal com valor diferente do combinado", "cliente recusou assinar por divergência de valor"],
    "avaria": ["caixa amassada na descarga", "produto molhado, embalagem rasgada", "volume avariado no transporte"],
}
entregas_ok = [l for l in {l[0]: l for l in tms_raw}.values() if l[8] == "Entregue"]
ocorr_raw = []
for oid in range(1, 1_201):
    l = random.choice(entregas_ok)
    v, cli, d = int(l[4]), int(l[2]), (date.fromisoformat(l[6]) - BASE).days
    pesos = {"mecanica": 3 if v in VEICULOS_ATENCAO else 1, "clima_transito": 3 if chuva[(int(l[3]), d)] > 30 else 1,
             "cobranca": 8 if cli in CLIENTES_ATENCAO else 1, "avaria": 1}
    cat = random.choices(list(pesos), list(pesos.values()))[0]
    texto = random.choice(TEXTOS[cat])
    texto = random.choice([texto, texto.upper(), texto.capitalize(), "  " + texto + "  "])
    if random.random() < 0.04:
        texto = random.choice(["", "   ", "ok", "-"])   # registros vazios/inúteis
    ocorr_raw.append((str(oid), l[0], l[4], f"{l[7]}T{random.randint(7, 19):02d}:{random.randint(0, 59):02d}:00", texto))

print(f"IoT: {len(iot_raw):,} · TMS: {len(tms_raw):,} · ERP: {len(erp_raw):,} · WMS: {len(wms_raw):,} · "
      f"Clima: {len(clima_raw):,} · Ocorrências: {len(ocorr_raw):,}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 2 — Camada BRONZE: o recibo da ingestão (pronto)
# MAGIC
# MAGIC Tudo entra **como chegou**, mais dois metadados: *quando* chegou (`_ingestao_ts`) e *de onde*
# MAGIC veio (`_fonte`). JSON e texto entram como texto puro; os extratos estruturados entram com todas
# MAGIC as colunas como texto. Nada é validado aqui — se a Silver errar, reprocessamos a partir da Bronze.

# COMMAND ----------

from pyspark.sql import functions as F


def para_bronze(linhas, colunas, tabela, fonte):
    df = (spark.createDataFrame(linhas, colunas)
          .withColumn("_ingestao_ts", F.current_timestamp())
          .withColumn("_fonte", F.lit(fonte)))
    df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"lodlog_bronze.{tabela}")
    print(f"Bronze {tabela:22s} {spark.table(f'lodlog_bronze.{tabela}').count():>7,} linhas  ← {fonte}")


para_bronze([(e,) for e in iot_raw], ["payload_json"], "iot_telemetria_raw", "iot-frota (streaming)")
para_bronze(tms_raw, ["entrega_id", "numero_pedido", "cliente_id", "cd_id", "veiculo_id", "motorista_id",
                      "data_prevista", "data_entrega", "status", "valor_frete", "distancia_km"],
            "tms_entregas_raw", "tms (batch/CDC)")
para_bronze(erp_raw, ["fatura_id", "entrega_id", "cliente_id", "valor_faturado", "data_emissao"],
            "erp_faturas_raw", "erp (batch diário)")
para_bronze(wms_raw, ["cd_id", "sku", "data", "saldo", "demanda_dia", "ponto_reposicao"],
            "wms_estoque_raw", "wms (batch diário)")
para_bronze([(e,) for e in clima_raw], ["payload_json"], "clima_api_raw", "api-inmet (externa)")
para_bronze(ocorr_raw, ["ocorrencia_id", "entrega_id", "veiculo_id", "registrado_em", "texto"],
            "ocorrencias_raw", "app-motorista (texto livre)")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 3 — Camada SILVER das fontes prontas (pronto)
# MAGIC
# MAGIC Na Silver o dado ganha **tipo, regra e dono**: aplicamos o schema, removemos duplicatas e barramos o
# MAGIC que viola regra de negócio. Cada `WHERE` abaixo é uma **regra de qualidade explícita e auditável** —
# MAGIC é isso que separa um data lake de um pântano de dados.
# MAGIC
# MAGIC **3.1 · IoT (semiestruturado):** o JSON vira colunas; leituras sem veículo ou com velocidade absurda saem.

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS lodlog_silver.iot_telemetria;
# MAGIC CREATE TABLE lodlog_silver.iot_telemetria USING DELTA AS
# MAGIC WITH parseado AS (
# MAGIC   SELECT from_json(payload_json,
# MAGIC     'veiculo_id INT, ts TIMESTAMP, gps STRUCT<lat: DOUBLE, lon: DOUBLE>,
# MAGIC      velocidade_kmh DOUBLE, temperatura_motor_c DOUBLE, nivel_combustivel_pct DOUBLE') AS e
# MAGIC   FROM lodlog_bronze.iot_telemetria_raw
# MAGIC )
# MAGIC SELECT DISTINCT                                   -- remove eventos duplicados
# MAGIC   e.veiculo_id, e.ts AS timestamp_evento, DATE(e.ts) AS data_evento,
# MAGIC   e.gps.lat AS latitude, e.gps.lon AS longitude,
# MAGIC   e.velocidade_kmh, e.temperatura_motor_c, e.nivel_combustivel_pct
# MAGIC FROM parseado
# MAGIC WHERE e.veiculo_id IS NOT NULL
# MAGIC   AND e.velocidade_kmh BETWEEN 0 AND 160;         -- regra: leitura fisicamente plausível

# COMMAND ----------

# MAGIC %md
# MAGIC **3.2 · TMS entregas:** tipos corretos, uma linha por entrega (o extrato reenviado gera duplicata),
# MAGIC frete negativo barrado e duas colunas derivadas que o negócio entende: `atraso_dias` e `no_prazo`.

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS lodlog_silver.tms_entregas;
# MAGIC CREATE TABLE lodlog_silver.tms_entregas USING DELTA AS
# MAGIC SELECT DISTINCT
# MAGIC   CAST(entrega_id AS BIGINT)            AS entrega_id,
# MAGIC   numero_pedido,
# MAGIC   CAST(cliente_id AS INT)               AS cliente_id,
# MAGIC   CAST(cd_id AS INT)                    AS cd_id,
# MAGIC   CAST(veiculo_id AS INT)               AS veiculo_id,
# MAGIC   CAST(motorista_id AS INT)             AS motorista_id,
# MAGIC   CAST(data_prevista AS DATE)           AS data_prevista,
# MAGIC   CAST(NULLIF(data_entrega, '') AS DATE) AS data_entrega,
# MAGIC   status,
# MAGIC   CAST(valor_frete AS DECIMAL(12,2))    AS valor_frete,
# MAGIC   CAST(distancia_km AS DOUBLE)          AS distancia_km,
# MAGIC   DATEDIFF(CAST(NULLIF(data_entrega, '') AS DATE), CAST(data_prevista AS DATE)) AS atraso_dias,
# MAGIC   DATEDIFF(CAST(NULLIF(data_entrega, '') AS DATE), CAST(data_prevista AS DATE)) <= 0 AS no_prazo
# MAGIC FROM lodlog_bronze.tms_entregas_raw
# MAGIC WHERE CAST(valor_frete AS DECIMAL(12,2)) > 0;      -- regra: frete precisa ser positivo

# COMMAND ----------

# MAGIC %md
# MAGIC **3.3 · ERP faturas:** tipos corretos e uma marca de **integridade referencial** — a fatura aponta
# MAGIC para uma entrega que existe? (No Unity Catalog, chave estrangeira é só informativa: quem garante é
# MAGIC a regra da Silver.) Não apagamos a órfã: marcamos, porque ela é evidência para auditoria.

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS lodlog_silver.erp_faturas;
# MAGIC CREATE TABLE lodlog_silver.erp_faturas USING DELTA AS
# MAGIC SELECT
# MAGIC   CAST(f.fatura_id AS BIGINT)            AS fatura_id,
# MAGIC   CAST(f.entrega_id AS BIGINT)           AS entrega_id,
# MAGIC   CAST(f.cliente_id AS INT)              AS cliente_id,
# MAGIC   CAST(f.valor_faturado AS DECIMAL(12,2)) AS valor_faturado,
# MAGIC   CAST(f.data_emissao AS DATE)           AS data_emissao,
# MAGIC   e.entrega_id IS NOT NULL               AS tem_entrega   -- FALSE = fatura órfã
# MAGIC FROM lodlog_bronze.erp_faturas_raw f
# MAGIC LEFT JOIN (SELECT DISTINCT CAST(entrega_id AS BIGINT) AS entrega_id
# MAGIC            FROM lodlog_bronze.tms_entregas_raw) e
# MAGIC   ON CAST(f.entrega_id AS BIGINT) = e.entrega_id;

# COMMAND ----------

# MAGIC %md
# MAGIC **3.4 · WMS estoque:** saldo negativo é erro de inventário e sai; `ruptura` vira uma coluna explícita.

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS lodlog_silver.wms_estoque;
# MAGIC CREATE TABLE lodlog_silver.wms_estoque USING DELTA AS
# MAGIC SELECT
# MAGIC   CAST(cd_id AS INT)            AS cd_id,
# MAGIC   sku,
# MAGIC   CAST(data AS DATE)            AS data,
# MAGIC   CAST(saldo AS INT)            AS saldo,
# MAGIC   CAST(demanda_dia AS INT)      AS demanda_dia,
# MAGIC   CAST(ponto_reposicao AS INT)  AS ponto_reposicao,
# MAGIC   CAST(saldo AS INT) = 0        AS ruptura
# MAGIC FROM lodlog_bronze.wms_estoque_raw
# MAGIC WHERE CAST(saldo AS INT) >= 0;          -- regra: saldo negativo é erro de inventário

# COMMAND ----------

for t in ["iot_telemetria", "tms_entregas", "erp_faturas", "wms_estoque"]:
    nb = spark.table(f"lodlog_bronze.{t}_raw").count()
    ns = spark.table(f"lodlog_silver.{t}").count()
    print(f"{t:16s} Bronze → Silver: {nb:>7,} → {ns:>7,}  ({nb - ns:,} barradas pela qualidade)")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 4 — 🟨 TODO 1 · Levar uma fonte semi/não estruturada até a Silver
# MAGIC
# MAGIC Duas fontes ficaram só na Bronze. O grupo leva **uma delas** (a recomendada para o seu cenário)
# MAGIC até a Silver. O código está pronto; **as regras são decisão de vocês**:
# MAGIC
# MAGIC - **`clima`** (JSON da API do INMET) — que valor de chuva diária é plausível? A API às vezes
# MAGIC   devolve `9999` como código de erro. Acima de qual limite vocês descartam a leitura?
# MAGIC - **`ocorrencias`** (texto livre) — o motorista escreve como quer. Para virar dado analisável,
# MAGIC   cada texto recebe uma **categoria** pelas palavras-chave que vocês definem. Olhem a amostra
# MAGIC   abaixo e completem as listas. Quanto menos texto cair em `outros`, melhor a regra.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Amostra para inspirar as regras (pronto)
# MAGIC SELECT texto, COUNT(*) AS vezes FROM lodlog_bronze.ocorrencias_raw GROUP BY texto ORDER BY vezes DESC LIMIT 25;

# COMMAND ----------

# 🟨 TODO 1a — qual fonte o grupo leva para a Silver? "clima" ou "ocorrencias"
FONTE_EXTRA = None

# 🟨 TODO 1b (se escolheram "clima") — maior chuva diária plausível, em mm.
#    Dica: o recorde brasileiro em 24h fica na casa dos 300 mm.
CHUVA_MAX_MM = None

# 🟨 TODO 1b (se escolheram "ocorrencias") — completem as palavras-chave de cada categoria.
#    Use pedaços de palavra em minúsculas e sem acento quando possível ("cobr" pega cobrança e cobrado).
CATEGORIAS = {
    "mecanica":       ["motor", "freio"],    # completem: o que mais indica problema mecânico?
    "clima_transito": [],                    # completem
    "cobranca":       [],                    # completem
    "avaria":         ["amassad"],           # completem
}

# COMMAND ----------

# Construção da Silver da fonte extra (pronto — usa as decisões acima)
FONTES_EXTRAS = [FONTE_EXTRA] if isinstance(FONTE_EXTRA, str) else list(FONTE_EXTRA or [])

if not FONTES_EXTRAS:
    print("⏸  TODO 1 pendente: defina FONTE_EXTRA na célula acima.")

if "clima" in FONTES_EXTRAS:
    if CHUVA_MAX_MM is None:
        print("⏸  TODO 1b pendente: defina CHUVA_MAX_MM.")
    else:
        spark.sql("DROP TABLE IF EXISTS lodlog_silver.clima_diario")
        spark.sql(f"""
            CREATE TABLE lodlog_silver.clima_diario USING DELTA AS
            WITH p AS (
              SELECT from_json(payload_json,
                'estacao STRING, cd_id INT, data DATE,
                 medicoes STRUCT<chuva_mm: DOUBLE, temp_max_c: DOUBLE>, alerta STRING') AS c
              FROM lodlog_bronze.clima_api_raw)
            SELECT DISTINCT c.cd_id, c.data, c.estacao,
                   c.medicoes.chuva_mm AS chuva_mm, c.medicoes.temp_max_c AS temp_max_c,
                   COALESCE(c.alerta, 'sem alerta') AS alerta
            FROM p
            WHERE c.medicoes.chuva_mm IS NOT NULL
              AND c.medicoes.chuva_mm BETWEEN 0 AND {float(CHUVA_MAX_MM)}""")
        nb = spark.table("lodlog_bronze.clima_api_raw").count()
        ns = spark.table("lodlog_silver.clima_diario").count()
        print(f"clima Bronze → Silver: {nb:,} → {ns:,}  ({nb - ns:,} barradas: duplicatas, ausentes e códigos de erro)")

if "ocorrencias" in FONTES_EXTRAS:
    def _regra(cat, palavras):
        cond = " OR ".join(f"t LIKE '%{p.lower().replace(chr(39), '')}%'" for p in palavras if p.strip())
        return f"WHEN {cond} THEN '{cat}'" if cond else ""
    casos = "\n".join(_regra(c, ps) for c, ps in CATEGORIAS.items())
    spark.sql("DROP TABLE IF EXISTS lodlog_silver.ocorrencias")
    spark.sql(f"""
        CREATE TABLE lodlog_silver.ocorrencias USING DELTA AS
        WITH limpo AS (
          SELECT CAST(ocorrencia_id AS BIGINT) AS ocorrencia_id,
                 CAST(entrega_id AS BIGINT)    AS entrega_id,
                 CAST(veiculo_id AS INT)       AS veiculo_id,
                 CAST(registrado_em AS TIMESTAMP) AS registrado_em,
                 TRIM(texto) AS texto,
                 translate(lower(TRIM(texto)), 'áàâãéêíóôõúç', 'aaaaeeiooouc') AS t
          FROM lodlog_bronze.ocorrencias_raw)
        SELECT ocorrencia_id, entrega_id, veiculo_id, registrado_em, texto,
               CASE {casos} ELSE 'outros' END AS categoria
        FROM limpo
        WHERE LENGTH(t) >= 5                -- regra: descarta registros vazios ou inúteis
        """)
    dist = spark.sql("SELECT categoria, COUNT(*) n FROM lodlog_silver.ocorrencias GROUP BY categoria ORDER BY n DESC")
    display(dist)
    total = spark.table("lodlog_silver.ocorrencias").count()
    outros = spark.sql("SELECT COUNT(*) FROM lodlog_silver.ocorrencias WHERE categoria = 'outros'").first()[0]
    print(f"ocorrências classificadas: {total:,} · em 'outros': {outros:,} ({100 * outros / total:.0f}%)"
          + ("  ← acima de 10%: revisem as palavras-chave" if outros / total > 0.10 else "  ✅"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 5 — Camada GOLD
# MAGIC
# MAGIC ### 5.1 · Gold de referência (pronto)
# MAGIC Um exemplo completo: resumo diário da frota, a partir da telemetria. Notem o padrão que a Gold
# MAGIC do grupo vai seguir — **chaves de negócio + contagens + uma métrica que alguém usa para decidir.**

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS lodlog_gold.resumo_diario_frota;
# MAGIC CREATE TABLE lodlog_gold.resumo_diario_frota USING DELTA AS
# MAGIC SELECT data_evento, veiculo_id,
# MAGIC        COUNT(*)                               AS leituras,
# MAGIC        ROUND(AVG(velocidade_kmh), 1)          AS velocidade_media,
# MAGIC        ROUND(MAX(temperatura_motor_c), 1)     AS temperatura_max_motor,
# MAGIC        ROUND(MIN(nivel_combustivel_pct), 1)   AS menor_nivel_combustivel
# MAGIC FROM lodlog_silver.iot_telemetria
# MAGIC GROUP BY data_evento, veiculo_id;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5.2 · 🟨 TODO 2 · A Gold do cenário do grupo
# MAGIC
# MAGIC Cada cenário tem um **modelo de Gold quase pronto**: junta uma fonte estruturada com a fonte extra
# MAGIC do TODO 1 e já calcula as contagens. Falta **uma linha — a métrica-chave**, o número que vai
# MAGIC para o pitch. Encontrem o seu cenário abaixo e troquem `CAST(NULL AS DOUBLE)` pela fórmula
# MAGIC (a dica está no comentário). Mexam nos outros cenários só se quiserem.

# COMMAND ----------

GOLD = {
    "A": ("lodlog_gold.cenario_a_pontualidade", """
        SELECT e.cd_id, e.data_prevista AS data,
               COUNT(*)                                          AS entregas,
               SUM(CASE WHEN e.no_prazo THEN 1 ELSE 0 END)       AS entregas_no_prazo,
               ROUND(AVG(e.atraso_dias), 2)                      AS atraso_medio_dias,
               MAX(c.chuva_mm)                                   AS chuva_mm,
               CAST(NULL AS DOUBLE) AS metrica_chave   -- 🟨 TODO 2: % de entregas no prazo.
                                                       --    Dica: ROUND(100.0 * <no prazo> / <entregas>, 1)
        FROM lodlog_silver.tms_entregas e
        LEFT JOIN lodlog_silver.clima_diario c ON c.cd_id = e.cd_id AND c.data = e.data_prevista
        WHERE e.status = 'Entregue'
        GROUP BY e.cd_id, e.data_prevista"""),
    "B": ("lodlog_gold.cenario_b_saude_frota", """
        WITH iot AS (
          SELECT veiculo_id,
                 COUNT(*)                                                    AS leituras,
                 ROUND(AVG(temperatura_motor_c), 1)                          AS temp_media_motor,
                 SUM(CASE WHEN temperatura_motor_c > 105 THEN 1 ELSE 0 END)  AS leituras_superaquecimento
          FROM lodlog_silver.iot_telemetria GROUP BY veiculo_id),
        oc AS (
          SELECT veiculo_id, COUNT(*) AS ocorrencias_mecanicas
          FROM lodlog_silver.ocorrencias WHERE categoria = 'mecanica' GROUP BY veiculo_id)
        SELECT i.veiculo_id, i.leituras, i.temp_media_motor, i.leituras_superaquecimento,
               COALESCE(o.ocorrencias_mecanicas, 0) AS ocorrencias_mecanicas,
               CAST(NULL AS DOUBLE) AS metrica_chave   -- 🟨 TODO 2: % das leituras em superaquecimento.
                                                       --    Dica: ROUND(100.0 * <superaquecimento> / <leituras>, 1)
        FROM iot i LEFT JOIN oc o ON o.veiculo_id = i.veiculo_id"""),
    "C": ("lodlog_gold.cenario_c_ruptura", """
        SELECT w.cd_id, w.sku,
               COUNT(*)                                                         AS dias_observados,
               SUM(CASE WHEN w.ruptura THEN 1 ELSE 0 END)                       AS dias_em_ruptura,
               SUM(CASE WHEN w.ruptura AND c.chuva_mm > 30 THEN 1 ELSE 0 END)   AS rupturas_com_chuva_forte,
               CAST(NULL AS DOUBLE) AS metrica_chave   -- 🟨 TODO 2: taxa de ruptura (%).
                                                       --    Dica: ROUND(100.0 * <dias em ruptura> / <dias observados>, 1)
        FROM lodlog_silver.wms_estoque w
        LEFT JOIN lodlog_silver.clima_diario c ON c.cd_id = w.cd_id AND c.data = w.data
        GROUP BY w.cd_id, w.sku"""),
    "D": ("lodlog_gold.cenario_d_divergencia", """
        WITH fat AS (
          SELECT e.cliente_id, e.entrega_id, e.valor_frete, f.valor_faturado
          FROM lodlog_silver.tms_entregas e
          JOIN lodlog_silver.erp_faturas f ON f.entrega_id = e.entrega_id),
        oc AS (
          SELECT e.cliente_id, COUNT(*) AS reclamacoes_cobranca
          FROM lodlog_silver.ocorrencias o
          JOIN lodlog_silver.tms_entregas e ON e.entrega_id = o.entrega_id
          WHERE o.categoria = 'cobranca' GROUP BY e.cliente_id)
        SELECT fat.cliente_id,
               COUNT(*)                                                                      AS faturas,
               SUM(CASE WHEN ABS(fat.valor_faturado - fat.valor_frete) > 0.01 THEN 1 ELSE 0 END) AS faturas_divergentes,
               ROUND(SUM(fat.valor_faturado - fat.valor_frete), 2)                           AS diferenca_total_rs,
               COALESCE(MAX(oc.reclamacoes_cobranca), 0)                                     AS reclamacoes_cobranca,
               CAST(NULL AS DOUBLE) AS metrica_chave   -- 🟨 TODO 2: % de faturas divergentes.
                                                       --    Dica: ROUND(100.0 * <divergentes> / <faturas>, 1)
        FROM fat LEFT JOIN oc ON oc.cliente_id = fat.cliente_id
        GROUP BY fat.cliente_id"""),
}
FONTE_DO_CENARIO = {"A": "clima", "B": "ocorrencias", "C": "clima", "D": "ocorrencias"}

# COMMAND ----------

# Construção da Gold do grupo (pronto)
CENARIOS = [CENARIO] if isinstance(CENARIO, str) else list(CENARIO or [])
if not CENARIOS:
    print("⏸  Escolha o CENARIO no início do notebook.")
for cen in CENARIOS:
    tabela, sql = GOLD[cen]
    precisa = FONTE_DO_CENARIO[cen]
    if precisa not in FONTES_EXTRAS:
        print(f"⏸  Cenário {cen} usa a Silver de '{precisa}': conclua o TODO 1 com essa fonte.")
        continue
    spark.sql(f"DROP TABLE IF EXISTS {tabela}")
    spark.sql(f"CREATE TABLE {tabela} USING DELTA AS {sql}")
    preenchida = spark.sql(f"SELECT COUNT(metrica_chave) FROM {tabela}").first()[0]
    print(f"Gold {tabela}: {spark.table(tabela).count():,} linhas · métrica-chave "
          + ("✅ preenchida" if preenchida else "⏸  ainda NULL — falta o TODO 2"))
    display(spark.table(tabela).limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 6 — Análise sobre a Gold
# MAGIC
# MAGIC ### 6.1 · Exemplo pronto
# MAGIC *Pergunta: quantos veículos por dia chegam à reserva de combustível (abaixo de 10%) — risco de
# MAGIC parada em rota?* Repare no formato: **pergunta → consulta → frase para a diretoria.**

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT data_evento,
# MAGIC        COUNT(*)                                                   AS veiculos_ativos,
# MAGIC        SUM(CASE WHEN menor_nivel_combustivel < 10 THEN 1 ELSE 0 END) AS veiculos_na_reserva
# MAGIC FROM lodlog_gold.resumo_diario_frota
# MAGIC GROUP BY data_evento
# MAGIC ORDER BY veiculos_na_reserva DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC > **Frase para a diretoria (exemplo):** *"Nos piores dias, um em cada quatro veículos ativos chega
# MAGIC > à reserva; uma regra de abastecimento antes da saída custa menos que um caminhão parado em rota."*
# MAGIC
# MAGIC ### 6.2 · 🟨 TODO 3 · A análise do grupo
# MAGIC 1. Escrevam a **pergunta de negócio** que a Gold do grupo responde.
# MAGIC 2. Rodem a consulta sugerida para o seu cenário (podem adaptar o `ORDER BY`, o `WHERE` ou o `LIMIT`).
# MAGIC 3. Escrevam a **interpretação**: o que vocês diriam ao diretor com esse número? Que decisão ela apoia?

# COMMAND ----------

# 🟨 TODO 3a — a pergunta de negócio do grupo (uma frase)
PERGUNTA_NEGOCIO = ""

ANALISE = {
    "A": """SELECT cd_id, SUM(entregas) AS entregas,
                   ROUND(AVG(CASE WHEN chuva_mm > 30 THEN metrica_chave END), 1) AS pct_no_prazo_dia_chuvoso,
                   ROUND(AVG(CASE WHEN chuva_mm <= 30 THEN metrica_chave END), 1) AS pct_no_prazo_dia_seco
            FROM lodlog_gold.cenario_a_pontualidade GROUP BY cd_id ORDER BY cd_id""",
    "B": """SELECT veiculo_id, metrica_chave AS pct_leituras_superaquecimento, ocorrencias_mecanicas, temp_media_motor
            FROM lodlog_gold.cenario_b_saude_frota ORDER BY metrica_chave DESC LIMIT 10""",
    "C": """SELECT cd_id, ROUND(AVG(metrica_chave), 1) AS taxa_ruptura_pct,
                   SUM(dias_em_ruptura) AS dias_em_ruptura, SUM(rupturas_com_chuva_forte) AS com_chuva_forte
            FROM lodlog_gold.cenario_c_ruptura GROUP BY cd_id ORDER BY taxa_ruptura_pct DESC""",
    "D": """SELECT cliente_id, faturas, metrica_chave AS pct_divergentes, diferenca_total_rs, reclamacoes_cobranca
            FROM lodlog_gold.cenario_d_divergencia ORDER BY metrica_chave DESC LIMIT 10""",
}
for cen in CENARIOS:
    try:
        display(spark.sql(ANALISE[cen]))
    except Exception as e:
        print(f"⏸  Cenário {cen}: a Gold ainda não existe ({str(e).splitlines()[0][:80]})")

# COMMAND ----------

# 🟨 TODO 3b — depois de ver o resultado: o que vocês diriam à diretoria? Que decisão isso apoia?
INTERPRETACAO = ""

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 7 — Governança
# MAGIC
# MAGIC ### 7.1 · Exemplo pronto na Gold de referência
# MAGIC Os 4 pilares da Aula 4 viram **metadados na própria tabela**: quem é o dono, o que ela contém,
# MAGIC se tem dado pessoal (LGPD) e por quanto tempo guardar. Qualquer pessoa que achar a tabela no
# MAGIC catálogo encontra essas respostas — é o antídoto contra o "de onde veio esse número?".

# COMMAND ----------

def aplicar_governanca(tabela, g):
    descricao = g["descricao"].replace("'", "")
    spark.sql(f"COMMENT ON TABLE {tabela} IS '{descricao}'")
    spark.sql(f"""ALTER TABLE {tabela} SET TBLPROPERTIES (
        'lodlog.dono' = '{g["dono"]}',
        'lodlog.contem_dados_pessoais' = '{str(g["contem_dados_pessoais"]).lower()}',
        'lodlog.retencao_dias' = '{g["retencao_dias"]}',
        'lodlog.regra_qualidade' = '{g["regra_qualidade"]}')""")
    props = {r["key"]: r["value"] for r in spark.sql(f"SHOW TBLPROPERTIES {tabela}").collect()
             if r["key"].startswith("lodlog.")}
    print(f"Governança aplicada em {tabela}: {props}")


aplicar_governanca("lodlog_gold.resumo_diario_frota", {
    "dono": "Gerência de Manutenção de Frota",
    "descricao": "Resumo diário por veículo a partir da telemetria IoT (Silver iot_telemetria).",
    "contem_dados_pessoais": False,
    "retencao_dias": 730,
    "regra_qualidade": "leituras_positivas",
})

# COMMAND ----------

# MAGIC %md
# MAGIC ### 7.2 · 🟨 TODO 4 · Governança da Gold do grupo
# MAGIC Preencham o dicionário. Para a regra de qualidade, escolham uma das regras prontas:
# MAGIC
# MAGIC | Regra | O que verifica |
# MAGIC |---|---|
# MAGIC | `metrica_entre_0_e_100` | A métrica-chave é um percentual válido |
# MAGIC | `metrica_sem_nulos` | Nenhuma linha da Gold ficou sem métrica |
# MAGIC | `chave_unica` | Não há linha duplicada para a mesma chave de negócio |

# COMMAND ----------

# 🟨 TODO 4 — governança da Gold do grupo
GOVERNANCA_GRUPO = {
    "dono": "",                       # área de negócio responsável (não uma pessoa)
    "descricao": "",                  # uma frase: o que a tabela contém e de quais Silvers vem
    "contem_dados_pessoais": None,    # True / False — pensem em cliente_id e motorista_id
    "retencao_dias": None,            # por quanto tempo guardar? (número de dias)
    "regra_qualidade": "",            # uma das três regras da tabela acima
}

# COMMAND ----------

# Aplicação e checagem da governança (pronto)
CHAVES = {"A": "cd_id, data", "B": "veiculo_id", "C": "cd_id, sku", "D": "cliente_id"}
REGRAS = {
    "metrica_entre_0_e_100": "SELECT COUNT(*) FROM {t} WHERE metrica_chave < 0 OR metrica_chave > 100",
    "metrica_sem_nulos":     "SELECT COUNT(*) FROM {t} WHERE metrica_chave IS NULL",
    "chave_unica":           "SELECT COUNT(*) FROM (SELECT {k} FROM {t} GROUP BY {k} HAVING COUNT(*) > 1)",
}
g = GOVERNANCA_GRUPO
governanca_ok = bool(g["dono"] and g["descricao"] and g["contem_dados_pessoais"] is not None
                     and g["retencao_dias"] and g["regra_qualidade"] in REGRAS)
for cen in CENARIOS:
    tabela = GOLD[cen][0]
    if not spark.catalog.tableExists(tabela):
        print(f"⏸  {tabela} ainda não existe.")
    elif not governanca_ok:
        print("⏸  TODO 4 pendente: preencham todos os campos de GOVERNANCA_GRUPO.")
    else:
        aplicar_governanca(tabela, g)
        violacoes = spark.sql(REGRAS[g["regra_qualidade"]].format(t=tabela, k=CHAVES[cen])).first()[0]
        print(f"Regra '{g['regra_qualidade']}': {violacoes} violação(ões) " + ("✅" if violacoes == 0 else "⚠️ investiguem"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 8 — Conferência final e números para o pitch (pronto)
# MAGIC Rodem esta célula ao fim de cada sessão. Tudo ✅ = notebook pronto para a apresentação da Aula 5.

# COMMAND ----------

def _existe(t):
    return spark.catalog.tableExists(t)


print("═" * 72)
print(f"Cenário: {CENARIO or '— não definido —'}")
cen = CENARIOS[0] if CENARIOS else None
gold = GOLD[cen][0] if cen else None
checks = [
    ("Cenário escolhido", bool(cen)),
    ("TODO 1 · fonte extra na Silver",
     bool(cen) and _existe({"clima": "lodlog_silver.clima_diario", "ocorrencias": "lodlog_silver.ocorrencias"}[FONTE_DO_CENARIO[cen]])),
    ("TODO 2 · Gold do cenário com métrica-chave",
     bool(gold) and _existe(gold) and spark.sql(f"SELECT COUNT(metrica_chave) FROM {gold}").first()[0] > 0),
    ("TODO 3 · pergunta de negócio", len(PERGUNTA_NEGOCIO.strip()) > 10),
    ("TODO 3 · interpretação", len(INTERPRETACAO.strip()) > 20),
    ("TODO 4 · governança aplicada",
     bool(gold) and _existe(gold) and any(r["key"] == "lodlog.dono" for r in spark.sql(f"SHOW TBLPROPERTIES {gold}").collect())),
]
for nome, ok in checks:
    print(f"  {'✅' if ok else '⬜'} {nome}")

print("\nNúmeros do pipeline (para o slide de execução):")
for camada in ["lodlog_bronze", "lodlog_silver", "lodlog_gold"]:
    for r in spark.sql(f"SHOW TABLES IN {camada}").collect():
        t = f"{camada}.{r['tableName']}"
        print(f"  {t:45s} {spark.table(t).count():>8,} linhas")
if PERGUNTA_NEGOCIO.strip():
    print(f"\nPergunta: {PERGUNTA_NEGOCIO}\nInterpretação: {INTERPRETACAO or '—'}")
print("═" * 72)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Para levar para a apresentação (Aula 5)
# MAGIC
# MAGIC - **Arquitetura:** as seis fontes → Bronze → Silver → Gold, destacando **o que veio pronto e o que o grupo construiu**.
# MAGIC - **Integração:** a Gold de vocês junta uma fonte estruturada (TMS, WMS ou ERP) com uma semi/não estruturada (clima ou ocorrências).
# MAGIC - **Execução:** os números da Etapa 8 — quantas linhas a qualidade barrou em cada camada e por quê.
# MAGIC - **Análise:** a pergunta, a consulta e a frase para a diretoria (TODO 3).
# MAGIC - **Avaliação pós-projeto (preliminar):** 2 vantagens, 2 limitações e 1 lição. A versão completa é a entrega individual.
# MAGIC
# MAGIC > 🧹 *Para recomeçar do zero:* `DROP SCHEMA lodlog_gold CASCADE` (idem silver e bronze) e Run All.
