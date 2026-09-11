# Databricks notebook source
import random
# LAB 2 — Simulação NoSQL com PySpark + Delta (poliglota persistence)
# Version: free (Unity Catalog: Volume `workspace.lodlog_volumes.raw` em vez de /FileStore, descontinuado)
# Execute: Workspace > Import > Run All
# ============================================

# COMMAND ----------
# CÉLULA 1 — Catálogo
VOL = "/Volumes/workspace/lodlog_volumes/raw"  # Volume UC = substituto do /FileStore (descontinuado)
try:
    spark.sql("USE CATALOG workspace")
    spark.sql("CREATE DATABASE IF NOT EXISTS lodlog_volumes")
    spark.sql("CREATE VOLUME IF NOT EXISTS lodlog_volumes.raw")
    print("✅ Catálogo workspace")
except Exception as e:
    print(f"⚠️  {e}")

# COMMAND ----------
# CÉLULA 2 — KV (Redis): cache de rotas origem→destino → distância/tempo
# Simula Redis como dict chave-valor O(1)
kv_data = []
cidades = ["SAO","RIO","BHZ","CGH","BSB","FOR","REC","SSA","FLR","POA"]
for i in range(200):
    orig = random.choice(cidades)
    dest = random.choice([c for c in cidades if c != orig])
    kv_data.append({
        "chave": f"route:{orig}:{dest}",
        "distancia_km": round(random.uniform(100, 3000), 1),
        "tempo_min": round(random.uniform(60, 360), 0),
        "ttl": 3600,  # segundos (TTL = Redis expire)
    })

df_kv = spark.createDataFrame(kv_data)
df_kv.write.format("delta").mode("overwrite").save(f"{VOL}/nosql/kv")
print(f"✅ KV (Redis): {df_kv.count()} rotas em cache")

# COMMAND ----------
# CÉLULA 3 — Documento (MongoDB): eventos IoT heterogêneos
# Cada veículo tem payload diferente (schema flexível)
doc_rows = []
for v in range(1, 21):
    base = {"veiculo_id": v, "tipo": "telemetria", "ts": "2025-07-01T08:00:00"}
    if v % 3 == 0:
        base.update({"rpm": 2200, "temp_motor": 88.5, "combustivel": 72.0})  # campo extra
    elif v % 3 == 1:
        base.update({"velocidade": 85.3, "odometro": 15000})  # campo diferente
    else:
        base.update({"status": "EM_ROTA", "motor_on": True})  # campo diferente
    doc_rows.append(base)

df_doc = spark.createDataFrame(doc_rows)
df_doc.write.format("delta").mode("overwrite").save(f"{VOL}/nosql/doc")
print(f"✅ Documento (MongoDB): {df_doc.count()} eventos heterogêneos")

# COMMAND ----------
# CÉLULA 4 — Coluna / Wide-Column (Cassandra): série temporal apend-only
# Simula HBase/Cassandra com writes sequenciais + partição por tempo
col_rows = []
for v in range(1, 11):
    for d in range(7):  # 7 dias
        col_rows.append({
            "row_key": f"{v}:2025-07-{d+1:02d}",
            "veiculo_id": v,
            "data": f"2025-07-{d+1:02d}",
            "velocidade_media": round(random.uniform(30, 90), 1),
            "diesel_consumido": round(random.uniform(50, 200), 1),
            "km_rotdos": round(random.uniform(200, 800), 1),
        })

df_col = spark.createDataFrame(col_rows)
df_col.write.format("delta").mode("overwrite").save(f"{VOL}/nosql/col")
print(f"✅ Coluna (Cassandra): {df_col.count()} registros série temporal")

# COMMAND ----------
# CÉLULA 5 — Grafo (Neo4j): topologia CD → veículo → entrega → cliente
# Simula relacionamentos como pares (origem, destino, peso)
import itertools
cds = [f"CD-{c}" for c in ["SAO","RIO","BHZ","CGH","BSB"]]
grafos = []
for cd in cds:
    for v in range(1, 6):
        grafos.append({"origem": cd, "destino": f"veiculo_{v}", "tipo_aresta": "operacao", "peso": round(random.uniform(1, 10), 1)})
for v in range(1, 6):
    for c in range(1, 4):
        grafos.append({"origem": f"veiculo_{v}", "destino": f"cliente_{c}", "tipo_aresta": "entrega", "peso": round(random.uniform(1, 5), 1)})

df_grafo = spark.createDataFrame(grafos)
df_grafo.write.format("delta").mode("overwrite").save(f"{VOL}/nosql/grafo")
print(f"✅ Grafo (Neo4j): {df_grafo.count()} arestas (CD→veículo→cliente)")

# COMMAND ----------
# CÉLULA 6 — Polyglot summary: quantos bancos por workload
spark.sql(f"""
SELECT 'KV-Redis' AS banco, COUNT(*) AS registros FROM delta.`{VOL}/nosql/kv`
UNION ALL
SELECT 'Documento-MongoDB', COUNT(*) FROM delta.`{VOL}/nosql/doc`
UNION ALL
SELECT 'Coluna-Cassandra', COUNT(*) FROM delta.`{VOL}/nosql/col`
UNION ALL
SELECT 'Grafo-Neo4j', COUNT(*) FROM delta.`{VOL}/nosql/grafo`
""").show()

print("\n💡 POLÍGLOTA PERSISTENCE: cada banco é escolhido pelo workload,")
print("   não por preferência. NoSQL é INGESTÃO; Delta Lake é ANALÍTICO.")