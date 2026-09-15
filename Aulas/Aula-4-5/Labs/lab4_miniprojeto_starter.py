# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC # LAB 4 — Starter do Miniprojeto: Data Lake da LODLog
# MAGIC ### Databricks Free Edition · Arquitetura Medallion (Bronze → Silver → Gold)
# MAGIC
# MAGIC **Para quem é este notebook:** seu grupo escolheu um cenário (Rotas, Manutenção Preditiva,
# MAGIC Estoque ou Fraude) e precisa construir um data lake de ponta a ponta. Este starter mostra o
# MAGIC caminho completo com **uma fonte semiestruturada (eventos IoT em JSON)** e **uma fonte
# MAGIC estruturada (pedidos do TMS)** — vocês adaptam cada etapa ao cenário do grupo.
# MAGIC
# MAGIC **Como executar:**
# MAGIC 1. Login no Databricks Free Edition — https://login.databricks.com (compute Serverless).
# MAGIC 2. Workspace > Import > este arquivo `.py` > Run All (~1 min).
# MAGIC 3. Leia os comentários de cada célula: eles explicam *o que* está acontecendo e *por que*.
# MAGIC
# MAGIC > 💡 *Regra de ouro do Medallion: a camada Bronze guarda o dado exatamente como chegou.
# MAGIC > Se algo der errado depois, você sempre pode reprocessar a partir do bruto.*

# COMMAND ----------

# ─────────────────────────────────────────────────────────────
# CÉLULA 0 — Catálogo (Unity Catalog do Free Edition) e schemas
# Criamos um schema por camada — espelha as zonas do data lake.
# ─────────────────────────────────────────────────────────────
CATALOG = "workspace"
try:
    spark.sql(f"USE CATALOG {CATALOG}")
    print(f"Catálogo ativo: {CATALOG}")
except Exception as e:
    print(f"Aviso: seguindo com o catálogo padrão ({e})")

for camada in ["lodlog_bronze", "lodlog_silver", "lodlog_gold"]:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {camada}")
print("Schemas criados: lodlog_bronze · lodlog_silver · lodlog_gold")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 1 — Simular as fontes de dados
# MAGIC
# MAGIC Na vida real, os eventos IoT chegariam por streaming (Kafka/Kinesis) e os pedidos por
# MAGIC CDC ou batch do banco do TMS. Aqui nós **geramos** os dados para o exercício — mas o
# MAGIC formato é fiel ao real: JSON cru com problemas típicos (campos faltando, duplicatas,
# MAGIC valores absurdos), exatamente o que um pipeline de verdade recebe.

# COMMAND ----------

import json
import random
from datetime import datetime, timedelta

random.seed(42)

# ── Fonte 1 · SEMIESTRUTURADA: eventos IoT da frota (JSON cru) ──
eventos_raw = []
base = datetime(2026, 8, 1, 6, 0, 0)
for i in range(5_000):
    veiculo = random.randint(1, 50)
    ts = base + timedelta(minutes=random.randint(0, 60 * 24 * 30))
    evento = {
        "veiculo_id": veiculo,
        "ts": ts.strftime("%Y-%m-%dT%H:%M:%S"),
        "gps": {"lat": round(random.uniform(-30.0, -19.0), 6),
                "lon": round(random.uniform(-51.5, -43.0), 6)},
        "velocidade_kmh": round(random.uniform(0, 115), 1),
        "temperatura_motor_c": round(random.uniform(78, 118), 1),
        "nivel_combustivel_pct": round(random.uniform(5, 100), 1),
    }
    # Sujeira proposital — como no mundo real:
    r = random.random()
    if r < 0.02:
        evento.pop("temperatura_motor_c")          # sensor falhou
    elif r < 0.03:
        evento["velocidade_kmh"] = 977.0           # leitura absurda
    elif r < 0.05:
        eventos_raw.append(json.dumps(evento))     # evento duplicado
    eventos_raw.append(json.dumps(evento))

# ── Fonte 2 · ESTRUTURADA: pedidos do TMS (linhas tipo CSV) ──
pedidos_raw = []
for pid in range(1, 2_001):
    dt_pedido = base + timedelta(hours=random.randint(0, 24 * 30))
    pedidos_raw.append((
        pid,
        f"PED-2026-{pid:06d}",
        random.randint(1, 200),                    # cliente_id
        random.randint(1, 5),                      # cd_origem_id
        dt_pedido.strftime("%Y-%m-%d %H:%M:%S"),
        random.choice(["Entregue", "Entregue", "Entregue", "Cancelado"]),
        round(random.uniform(80, 4500), 2),        # valor_frete
    ))

print(f"Eventos IoT gerados (JSON cru): {len(eventos_raw):,}")
print(f"Pedidos gerados (estruturados): {len(pedidos_raw):,}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 2 — Camada BRONZE: guardar o dado bruto, sem mexer
# MAGIC
# MAGIC O JSON entra como **texto puro** + metadados de ingestão (quando chegou, de onde veio).
# MAGIC Nada é validado ainda — Bronze é o "recibo" da ingestão.

# COMMAND ----------

from pyspark.sql import functions as F

# Bronze IoT: 1 coluna com o JSON cru + metadados de ingestão
df_bronze_iot = (spark.createDataFrame([(e,) for e in eventos_raw], ["payload_json"])
    .withColumn("_ingestao_ts", F.current_timestamp())
    .withColumn("_fonte", F.lit("iot-frota-simulado")))
df_bronze_iot.write.format("delta").mode("overwrite").saveAsTable("lodlog_bronze.iot_eventos_raw")

# Bronze Pedidos: colunas como vieram do sistema de origem (sem tipos refinados)
df_bronze_ped = (spark.createDataFrame(
        pedidos_raw,
        ["pedido_id", "numero_pedido", "cliente_id", "cd_origem_id",
         "data_pedido", "status_pedido", "valor_frete"])
    .withColumn("_ingestao_ts", F.current_timestamp())
    .withColumn("_fonte", F.lit("tms-pedidos-simulado")))
df_bronze_ped.write.format("delta").mode("overwrite").saveAsTable("lodlog_bronze.tms_pedidos_raw")

print(f"Bronze IoT:     {spark.table('lodlog_bronze.iot_eventos_raw').count():,} linhas (com duplicatas e sujeira!)")
print(f"Bronze Pedidos: {spark.table('lodlog_bronze.tms_pedidos_raw').count():,} linhas")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 3 — Camada SILVER: aplicar schema, limpar e deduplicar
# MAGIC
# MAGIC Aqui o JSON vira colunas tipadas, as leituras absurdas são filtradas e as duplicatas
# MAGIC removidas. **Regra de negócio explícita = qualidade auditável.**

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS lodlog_silver.iot_eventos;
# MAGIC CREATE TABLE lodlog_silver.iot_eventos USING DELTA AS
# MAGIC WITH parseado AS (
# MAGIC   SELECT
# MAGIC     from_json(payload_json,
# MAGIC       'veiculo_id INT, ts TIMESTAMP, gps STRUCT<lat: DOUBLE, lon: DOUBLE>,
# MAGIC        velocidade_kmh DOUBLE, temperatura_motor_c DOUBLE, nivel_combustivel_pct DOUBLE'
# MAGIC     ) AS e,
# MAGIC     _ingestao_ts
# MAGIC   FROM lodlog_bronze.iot_eventos_raw
# MAGIC )
# MAGIC SELECT DISTINCT                     -- deduplicação
# MAGIC   e.veiculo_id,
# MAGIC   e.ts                       AS timestamp_evento,
# MAGIC   DATE(e.ts)                 AS data_evento,   -- coluna de partição lógica
# MAGIC   e.gps.lat                  AS latitude,
# MAGIC   e.gps.lon                  AS longitude,
# MAGIC   e.velocidade_kmh,
# MAGIC   e.temperatura_motor_c,
# MAGIC   e.nivel_combustivel_pct
# MAGIC FROM parseado
# MAGIC WHERE e.veiculo_id IS NOT NULL
# MAGIC   AND e.velocidade_kmh BETWEEN 0 AND 160;      -- descarta leituras absurdas

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS lodlog_silver.tms_pedidos;
# MAGIC CREATE TABLE lodlog_silver.tms_pedidos USING DELTA AS
# MAGIC SELECT
# MAGIC   CAST(pedido_id AS BIGINT)          AS pedido_id,
# MAGIC   numero_pedido,
# MAGIC   CAST(cliente_id AS BIGINT)         AS cliente_id,
# MAGIC   CAST(cd_origem_id AS BIGINT)       AS cd_origem_id,
# MAGIC   CAST(data_pedido AS TIMESTAMP)     AS data_pedido,
# MAGIC   status_pedido,
# MAGIC   CAST(valor_frete AS DECIMAL(12,2)) AS valor_frete
# MAGIC FROM lodlog_bronze.tms_pedidos_raw
# MAGIC WHERE status_pedido <> 'Cancelado';            -- regra de negócio: só pedidos válidos

# COMMAND ----------

n_bronze = spark.table("lodlog_bronze.iot_eventos_raw").count()
n_silver = spark.table("lodlog_silver.iot_eventos").count()
print(f"IoT Bronze → Silver: {n_bronze:,} → {n_silver:,} "
      f"({n_bronze - n_silver:,} linhas removidas na limpeza — conte essa história no pitch!)")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 4 — Camada GOLD: agregar e integrar para o consumo
# MAGIC
# MAGIC A Gold junta a fonte **semiestruturada** (IoT) com a **estruturada** (pedidos):
# MAGIC visão diária por veículo/CD, pronta para dashboard ou modelo de IA.
# MAGIC *(Adaptem as métricas ao cenário do grupo: rotas, manutenção, estoque ou fraude.)*

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS lodlog_gold.resumo_diario_frota;
# MAGIC CREATE TABLE lodlog_gold.resumo_diario_frota USING DELTA AS
# MAGIC SELECT
# MAGIC   i.data_evento,
# MAGIC   i.veiculo_id,
# MAGIC   COUNT(*)                              AS eventos_iot,
# MAGIC   ROUND(AVG(i.velocidade_kmh), 1)       AS velocidade_media,
# MAGIC   ROUND(MAX(i.temperatura_motor_c), 1)  AS temperatura_max_motor,
# MAGIC   ROUND(MIN(i.nivel_combustivel_pct),1) AS menor_nivel_combustivel
# MAGIC FROM lodlog_silver.iot_eventos i
# MAGIC GROUP BY i.data_evento, i.veiculo_id;

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS lodlog_gold.receita_diaria;
# MAGIC CREATE TABLE lodlog_gold.receita_diaria USING DELTA AS
# MAGIC SELECT
# MAGIC   DATE(data_pedido)        AS data,
# MAGIC   cd_origem_id,
# MAGIC   COUNT(*)                 AS pedidos,
# MAGIC   SUM(valor_frete)         AS receita_frete
# MAGIC FROM lodlog_silver.tms_pedidos
# MAGIC GROUP BY DATE(data_pedido), cd_origem_id;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 5 — Análise sobre a Gold (exemplo de insight)
# MAGIC
# MAGIC *Pergunta de negócio: quais veículos rodaram com o motor mais quente — candidatos à
# MAGIC manutenção preventiva antes que virem entrega atrasada?*

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT veiculo_id,
# MAGIC        ROUND(AVG(temperatura_max_motor), 1) AS temp_max_media,
# MAGIC        SUM(eventos_iot)                     AS total_eventos
# MAGIC FROM lodlog_gold.resumo_diario_frota
# MAGIC GROUP BY veiculo_id
# MAGIC ORDER BY temp_max_media DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC ## ✅ O que vocês acabaram de construir
# MAGIC
# MAGIC | Camada | Tabela | O que demonstra |
# MAGIC |--------|--------|-----------------|
# MAGIC | Bronze | `lodlog_bronze.iot_eventos_raw` | Ingestão bruta de fonte **semiestruturada** (JSON) |
# MAGIC | Bronze | `lodlog_bronze.tms_pedidos_raw` | Ingestão bruta de fonte **estruturada** (TMS) |
# MAGIC | Silver | `lodlog_silver.iot_eventos` | Schema aplicado + dedup + filtro de qualidade |
# MAGIC | Silver | `lodlog_silver.tms_pedidos` | Tipos corretos + regra de negócio |
# MAGIC | Gold | `lodlog_gold.resumo_diario_frota` | Agregação pronta para consumo/IA |
# MAGIC | Gold | `lodlog_gold.receita_diaria` | Métrica de negócio por CD |
# MAGIC
# MAGIC ## 🎯 Agora é com o grupo — adaptem ao cenário escolhido
# MAGIC
# MAGIC 1. **Troquem/adicionem fontes** conforme o cenário (mínimo 3–5, internas e externas —
# MAGIC    podem reutilizar as tabelas `lodlog_op.*` do LAB 3 como fonte estruturada real).
# MAGIC 2. **Adaptem as regras da Silver** (que validações fazem sentido no seu cenário?).
# MAGIC 3. **Redesenhem a Gold** para responder à pergunta de negócio do grupo.
# MAGIC 4. **Executem 2 queries analíticas** com interpretação + **1 query de qualidade**.
# MAGIC 5. **Governança:** para cada um dos 4 pilares (Qualidade, Segurança/LGPD, Catálogo/Linhagem,
# MAGIC    Ciclo de Vida), escrevam 1 parágrafo de como o pilar se aplica ao seu lake.
# MAGIC
# MAGIC > 🧹 *Para recomeçar do zero:* `DROP SCHEMA lodlog_bronze CASCADE;` (idem silver/gold).