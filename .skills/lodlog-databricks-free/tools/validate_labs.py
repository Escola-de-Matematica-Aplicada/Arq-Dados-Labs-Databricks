# -*- coding: utf-8 -*-
"""Valida as queries dos LABs 2/3 e executa o starter do LAB 4 no warehouse local."""
import re, traceback
from pyspark.sql import SparkSession
from delta import configure_spark_with_delta_pip

WAREHOUSE = "/tmp/claude-0/-workspaces/f209aedd-7cbf-4af5-840f-f53030ae5fea/scratchpad/warehouse"
builder = (SparkSession.builder.appName("lodlog-validate").master("local[4]")
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    .config("spark.sql.warehouse.dir", WAREHOUSE)
    .config("spark.driver.memory", "4g")
    .config("spark.sql.shuffle.partitions", "8")
    .config("spark.hadoop.javax.jdo.option.ConnectionURL",
            f"jdbc:derby:;databaseName={WAREHOUSE}/metastore_db;create=true")
    .enableHiveSupport())
spark = configure_spark_with_delta_pip(builder).getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
spark.sql("USE lodlog_dw")

OK, FAIL = [], []
def run(nome, sql, show=3):
    try:
        df = spark.sql(sql)
        rows = df.limit(200).collect()
        OK.append(nome)
        print(f"\n✅ {nome} — {len(rows)}{'+' if len(rows)==200 else ''} linhas")
        for r in rows[:show]:
            print("   ", r.asDict())
    except Exception as e:
        FAIL.append((nome, str(e)[:400]))
        print(f"\n❌ {nome}\n   {str(e)[:400]}")

# ═══ LAB 2 ═══
run("LAB2 4.2 · taxa pontualidade por região", """
SELECT c.regiao,
       SUM(CASE WHEN f.indicador_atraso = 0 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS taxa_pontualidade
FROM fato_entregas f
INNER JOIN dim_centro_distribuicao c ON f.sk_cd_origem = c.sk_cd
GROUP BY c.regiao""")

run("LAB2 4.2 · entregas por categoria (mini-dimensão)", """
SELECT d.categoria, COUNT(*) AS entregas
FROM fato_entregas f
JOIN dim_cat_atraso d ON f.sk_cat_atraso = d.sk_cat_atraso
GROUP BY d.categoria ORDER BY MIN(d.ordem)""", show=5)

run("LAB2 2.1 · inspecionar entrega 2FN (colunas redundantes)", """
SELECT entrega_id, cliente_id, cliente_razao_social, veiculo_placa, motorista_nome, cd_origem_uf
FROM lodlog_op.entrega LIMIT 3""")

# ═══ LAB 3 Parte 1 ═══
run("LAB3 Q1 · volume e atrasos por mês", """
SELECT DATE_TRUNC('month', data_entrega) AS mes, COUNT(*) AS total_entregas,
       SUM(CASE WHEN minutos_atraso > 0 THEN 1 ELSE 0 END) AS entregas_atrasadas
FROM fato_entregas GROUP BY 1 ORDER BY 1""")

run("LAB3 Q2 · ranking CDs 90 dias", """
SELECT cd.codigo AS cd_origem, ROUND(AVG(fe.minutos_atraso), 2) AS atraso_medio_min,
       ROUND(SUM(fe.custo_combustivel + fe.custo_pedagio), 2) AS custo_total_operacional,
       COUNT(DISTINCT fe.sk_veiculo) AS frota_alocada
FROM fato_entregas fe
INNER JOIN dim_centro_distribuicao cd ON fe.sk_cd_origem = cd.sk_cd
WHERE fe.data_entrega >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY cd.codigo ORDER BY atraso_medio_min ASC""", show=5)

run("LAB3 Q3 · correlação distância x custo (30 dias)", """
SELECT corr(distancia_km, custo_combustivel) AS correlacao_distancia_custo
FROM fato_entregas WHERE data_entrega >= CURRENT_DATE - INTERVAL '30 days'""")

run("LAB3 1.2 · gabarito pontualidade por cliente", """
SELECT dc.razao_social, COUNT(*) AS total_entregas,
       ROUND(100.0 * SUM(CASE WHEN fe.indicador_atraso = 0 THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_no_prazo
FROM fato_entregas fe
INNER JOIN dim_cliente dc ON fe.sk_cliente = dc.sk_cliente
WHERE fe.data_entrega >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY dc.razao_social HAVING COUNT(*) > 10 ORDER BY pct_no_prazo ASC""")

# ═══ LAB 3 Parte 2 ═══
run("LAB3 2.1 · gabarito média móvel 7 linhas por CD", """
SELECT cd.codigo, fe.data_entrega, fe.minutos_atraso,
       ROUND(AVG(fe.minutos_atraso) OVER (
         PARTITION BY fe.sk_cd_origem ORDER BY fe.data_entrega
         ROWS BETWEEN 6 PRECEDING AND CURRENT ROW), 2) AS media_movel_7
FROM fato_entregas fe
JOIN dim_centro_distribuicao cd ON fe.sk_cd_origem = cd.sk_cd
LIMIT 50""")

run("LAB3 2.2 · ranking motoristas COMO ESTÁ NO LAB (nome_motorista)", """
WITH custo_por_motorista AS (
  SELECT sk_motorista, SUM(custo_combustivel) / NULLIF(SUM(distancia_km), 0) AS custo_por_km
  FROM fato_entregas WHERE data_entrega >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY sk_motorista)
SELECT m.nome_motorista, c.custo_por_km,
       NTILE(4) OVER (ORDER BY c.custo_por_km ASC) AS quartil,
       PERCENT_RANK() OVER (ORDER BY c.custo_por_km ASC) AS percentil
FROM custo_por_motorista c
INNER JOIN dim_motorista m ON c.sk_motorista = m.sk_motorista""")

run("LAB3 2.2 · ranking motoristas CORRIGIDO (nome_completo)", """
WITH custo_por_motorista AS (
  SELECT sk_motorista, SUM(custo_combustivel) / NULLIF(SUM(distancia_km), 0) AS custo_por_km
  FROM fato_entregas WHERE data_entrega >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY sk_motorista)
SELECT m.nome_completo AS nome_motorista, ROUND(c.custo_por_km, 4) AS custo_por_km,
       NTILE(4) OVER (ORDER BY c.custo_por_km ASC) AS quartil,
       ROUND(PERCENT_RANK() OVER (ORDER BY c.custo_por_km ASC), 3) AS percentil
FROM custo_por_motorista c
INNER JOIN dim_motorista m ON c.sk_motorista = m.sk_motorista""")

# ═══ LAB 3 Parte 3 · Feature Store ═══
run("LAB3 3.1 · CREATE VIEW vw_features_ml", """
CREATE OR REPLACE VIEW lodlog_dw.vw_features_ml AS
WITH hist_cliente AS (
    SELECT sk_entrega, sk_cliente, data_entrega,
           AVG(minutos_atraso) OVER (
             PARTITION BY sk_cliente ORDER BY data_entrega
             ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS hist_7d
    FROM fato_entregas),
manut_veiculo AS (
    SELECT veiculo_id, data_conclusao,
           ROW_NUMBER() OVER (PARTITION BY veiculo_id ORDER BY data_conclusao DESC) AS rn
    FROM lodlog_op.manutencao WHERE status = 'Concluída')
SELECT
    fe.sk_entrega, fe.distancia_km, fe.peso_total_kg,
    hour(fe.hora_saida) AS hora_saida,
    dayofweek(fe.data_entrega) AS dia_semana,
    dt.flag_feriado AS eh_feriado,
    fe.temperatura_media_motor,
    ROUND(h.hist_7d, 2) AS historico_atrasos_7d,
    DATEDIFF(fe.data_entrega, mv.data_conclusao) AS dias_ultima_manutencao,
    fe.indicador_atraso AS target_atraso
FROM fato_entregas fe
INNER JOIN dim_tempo dt ON fe.sk_data = dt.sk_tempo
LEFT JOIN hist_cliente h ON fe.sk_entrega = h.sk_entrega  -- grain 1:1 (por entrega)
LEFT JOIN manut_veiculo mv ON fe.sk_veiculo = mv.veiculo_id AND mv.rn = 1 AND mv.data_conclusao <= fe.data_entrega""")

run("LAB3 3.2.0 · contagem de linhas da view", "SELECT COUNT(*) AS n FROM vw_features_ml")
run("LAB3 3.2.1 · completude manutenção", "SELECT COUNT(*) AS nulos FROM vw_features_ml WHERE dias_ultima_manutencao IS NULL")
run("LAB3 3.2.2 · balanceamento target", """
SELECT target_atraso, COUNT(*) AS volume, ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) AS pct
FROM vw_features_ml GROUP BY 1""")
run("LAB3 3.2.3 · corr distancia x target", "SELECT corr(distancia_km, target_atraso) AS c FROM vw_features_ml")

# ═══ LAB 3 Parte 4 · Qualidade (gabaritos) ═══
run("LAB3 4.1a · duplicatas por pedido_id", """
SELECT pedido_id, COUNT(*) AS n FROM fato_entregas
GROUP BY pedido_id HAVING COUNT(*) > 1 ORDER BY n DESC""")
run("LAB3 4.1a-agg · total de pares duplicados", """
SELECT COUNT(*) AS pedidos_duplicados FROM (
  SELECT pedido_id FROM fato_entregas GROUP BY pedido_id HAVING COUNT(*) > 1)""")
run("LAB3 4.1b · valores negativos", """
SELECT COUNT(*) AS negativos FROM fato_entregas
WHERE distancia_km < 0 OR peso_total_kg < 0 OR custo_combustivel < 0""")
run("LAB3 4.1c · outliers de atraso", """
SELECT COUNT(*) AS outliers FROM fato_entregas
WHERE minutos_atraso > 1440 OR minutos_atraso < -480""")
run("LAB3 4.1d · órfãos de cliente (anti-join)", """
SELECT COUNT(*) AS orfaos FROM fato_entregas fe
LEFT JOIN dim_cliente dc ON fe.sk_cliente = dc.sk_cliente
WHERE dc.sk_cliente IS NULL""")

# ═══ LAB 4 · starter — executa células Python e %sql do notebook ═══
print("\n" + "═"*60 + "\n LAB 4 · lab4_miniprojeto_starter.py\n" + "═"*60)
src = open("/workspaces/Aulas/Aula-4-5/Labs/lab4_miniprojeto_starter.py", encoding="utf-8").read()
cells = src.split("# COMMAND ----------")
g = {"spark": spark}
for idx, cell in enumerate(cells):
    stripped = cell.strip()
    if not stripped:
        continue
    if stripped.startswith("# MAGIC %md"):
        continue
    if stripped.startswith("# MAGIC %sql"):
        sql = "\n".join(l.replace("# MAGIC", "", 1) for l in stripped.splitlines()[1:])
        try:
            stmts = [q.strip() for q in sql.split(";") if q.strip()]
            for q in stmts:
                df = spark.sql(q)
            n = len(df.limit(20).collect())
            OK.append(f"LAB4 célula sql #{idx}")
            print(f"✅ LAB4 célula %sql #{idx} — ok ({n} linhas retornadas)")
        except Exception as e:
            FAIL.append((f"LAB4 célula sql #{idx}", str(e)[:300]))
            print(f"❌ LAB4 célula %sql #{idx}: {str(e)[:300]}")
    else:
        try:
            exec(compile(cell, f"lab4_cell_{idx}", "exec"), g)
            OK.append(f"LAB4 célula py #{idx}")
            print(f"✅ LAB4 célula python #{idx}")
        except Exception as e:
            FAIL.append((f"LAB4 célula py #{idx}", str(e)[:300]))
            print(f"❌ LAB4 célula python #{idx}: {str(e)[:300]}")
            traceback.print_exc()

print("\n" + "═"*60)
print(f"RESULTADO: {len(OK)} OK · {len(FAIL)} FALHAS")
for nome, err in FAIL:
    print(f"  ❌ {nome}: {err[:200]}")
