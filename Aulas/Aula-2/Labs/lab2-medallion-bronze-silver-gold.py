# Databricks notebook source
import random
from pyspark.sql.functions import col, avg, count, lit, to_date
from pyspark.sql.window import Window
# LAB 2 — Pipeline Bronze → Silver → Gold (Medallion)
# Version: free (Unity Catalog: Volume `workspace.lodlog_volumes.raw` em vez de /FileStore, descontinuado)
# Execute in Databricks Free Edition: Workspace > Import > Run All
#
# CENÁRIO: telemetria IoT de frota (JSON raw → Delta validado → agregado)
# GRADE: 5 CDs, 50 veículos, ~50k entregas (dataset piloto)
# ============================================

# COMMAND ----------
# CÉLULA 1 — Catálogo e schemas (Free Edition = Serverless + Unity Catalog)
VOL = "/Volumes/workspace/lodlog_volumes/raw"  # Volume UC = substituto do /FileStore (descontinuado)
try:
    spark.sql("USE CATALOG workspace")
    spark.sql("CREATE DATABASE IF NOT EXISTS lodlog_op COMMENT 'Operacional (ER 3FN)'")
    spark.sql("CREATE DATABASE IF NOT EXISTS lodlog_dw COMMENT 'Star Schema DW/ML'")
    spark.sql("CREATE DATABASE IF NOT EXISTS lodlog_volumes")
    spark.sql("CREATE VOLUME IF NOT EXISTS lodlog_volumes.raw")
    print("✅ Catálogo workspace — schemas prontos")
except Exception as e:
    print(f"⚠️  Catálogo (modo local?): {e}")

# COMMAND ----------
# CÉLULA 2 — Bronze: ingestão raw schema-on-read (JSON IoT)
# Simula 864k eventos/dia → recorte piloto 50 veículos × 288 leituras/dia
import json, random, datetime

random.seed(42)
VEICULOS = 50
DIAS = 30
LEITURAS_POR_DIA = 288  # a cada 5 min

rows = []
for v in range(1, VEICULOS + 1):
    for d in range(DIAS):
        base = datetime.datetime(2025, 7, 1) + datetime.timedelta(days=d)
        for l in range(LEITURAS_POR_DIA):
            ts = base + datetime.timedelta(minutes=5 * l)
            rows.append({
                "veiculo_id": v,
                "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
                "latitude": round(-23.5 + random.gauss(0, 0.5), 6),
                "longitude": round(-46.6 + random.gauss(0, 0.5), 6),
                "velocidade_kmh": round(random.uniform(0, 120), 1),
                "rpm_motor": random.randint(800, 4500),
                "temperatura_motor_c": round(random.uniform(70, 110), 1),
                "nivel_combustivel_pct": round(random.uniform(10, 100), 1),
                "peso_carga_kg": round(random.uniform(0, 15000), 1),
                "hodometro_km": round(10000 + d * 150 + l * 0.5, 1),
            })

df_bronze = spark.createDataFrame(rows)
df_bronze.write.format("delta").mode("overwrite").save(f"{VOL}/bronze/iot")
print(f"✅ Bronze: {df_bronze.count():,} linhas gravadas")

# COMMAND ----------
# CÉLULA 3 — Silver: 4 camadas de Veracidade (edge/stream/cross/trust)
from pyspark.sql.functions import col, to_date, avg, lag
from pyspark.sql.window import Window

df_silver = (
    spark.read.format("delta").load(f"{VOL}/bronze/iot")
    # Edge: range checks (vel 0-200, temp 50-150)
    .filter((col("velocidade_kmh") >= 0) & (col("velocidade_kmh") <= 200))
    .filter((col("temperatura_motor_c") >= 50) & (col("temperatura_motor_c") <= 150))
    # Stream: dedup por veículo+timestamp
    .dropDuplicates(["veiculo_id", "timestamp"])
    # Trust: adiciona data e provenance
    .withColumn("data", to_date(col("timestamp")))
    .withColumn("provenance", lit("IoT-sensor-v1"))
)

df_silver.write.format("delta").mode("overwrite") \
    .option("mergeSchema", "true").save(f"{VOL}/silver/iot")
print(f"✅ Silver: {df_silver.count():,} linhas (dedup + validação)")

# COMMAND ----------
# CÉLULA 4 — Gold: agregação para análise executiva
df_gold = (
    df_silver
    .groupBy("veiculo_id", "data")
    .agg(
        avg("velocidade_kmh").alias("avg_vel"),
        avg("temperatura_motor_c").alias("avg_temp"),
        avg("nivel_combustivel_pct").alias("avg_fuel"),
        count("*").alias("leituras"),
    )
    .orderBy("data", "veiculo_id")
)

df_gold.write.format("delta").mode("overwrite").save(f"{VOL}/gold/iot")
print(f"✅ Gold: {df_gold.count():,} linhas (agregado veículo/dia)")

# COMMAND ----------
# CÉLULA 5 — Time-travel: auditoria de versão
print("Versões Gold:", spark.sql(f"DESCRIBE HISTORY delta.`{VOL}/gold/iot`").count())
display(spark.read.format("delta").load(f"{VOL}/gold/iot").limit(10))

# COMMAND ----------
# CÉLULA 6 — Resumo executivo
spark.sql("""
SELECT data,
       COUNT(DISTINCT veiculo_id) AS veiculos,
       ROUND(AVG(avg_vel), 1) AS vel_media_frota,
       ROUND(AVG(avg_temp), 1) AS temp_media_frota
FROM delta.`/Volumes/workspace/lodlog_volumes/raw/gold/iot`
GROUP BY data ORDER BY data LIMIT 10
""").show()