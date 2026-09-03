# -*- coding: utf-8 -*-
"""Gera as versões 'Databricks Free Edition' do seed e da DDL a partir dos originais."""
import re

# ────────────────────────────────────────────────────────────────
# 1) SEED  →  Aulas/Aula-3/Labs/lodlog_lab3_seed_free.py
# ────────────────────────────────────────────────────────────────
src = open("/workspaces/Labs/lodlog_lab3_seed_v3.py", encoding="utf-8").read()

header_old = """# Databricks notebook source
# Importar este arquivo no Databricks como notebook Python e executar UMA VEZ antes do LAB 2.
# File: lodlog_lab3_seed_v3.py
# Uso: Workspace > Import > selecione este arquivo (.py) > Run All
#"""
header_new = """# Databricks notebook source
# Importar este arquivo no Databricks Free Edition como notebook Python e executar UMA VEZ antes do LAB 3.
# File: lodlog_lab3_seed_free.py
# Uso: Workspace > Import > selecione este arquivo (.py) > Run All (compute Serverless)
#
# ════════════════════════════════════════════════════════════════
# VERSÃO "FREE" (agosto/2026) — adaptada ao Databricks FREE EDITION
# ════════════════════════════════════════════════════════════════
# O Databricks Community Edition foi descontinuado. Esta versão roda no
# Databricks Free Edition (https://www.databricks.com/learn/free-edition):
#   · Login: https://login.databricks.com (conta gratuita, sem cartão)
#   · Compute: SOMENTE Serverless (não há criação de cluster)
#   · Governança: Unity Catalog habilitado por padrão — os schemas
#     lodlog_op e lodlog_dw são criados dentro do catálogo `workspace`
#   · O comando USE CATALOG workspace (primeira célula) garante que
#     todos os objetos fiquem no lugar certo
#"""
assert header_old in src
src = src.replace(header_old, header_new)

# Célula de catálogo logo após a 1ª célula markdown (antes do "import random")
anchor = "# COMMAND ----------\n\nimport random"
cat_cell = """# COMMAND ----------

# ─────────────────────────────────────────────────────────────
# CÉLULA 0 — Unity Catalog (Databricks Free Edition)
# No Free Edition todos os dados vivem no catálogo `workspace`.
# ─────────────────────────────────────────────────────────────
CATALOG = "workspace"
try:
    spark.sql(f"USE CATALOG {CATALOG}")
    print(f"Catálogo ativo: {CATALOG}")
except Exception as e:  # ambiente sem Unity Catalog (ex.: Spark local)
    print(f"Aviso: seguindo com o catálogo padrão ({e})")

# COMMAND ----------

import random"""
assert anchor in src
src = src.replace(anchor, cat_cell, 1)

# OPTIMIZE tolerante a falha (Predictive Optimization do Free Edition já otimiza tabelas gerenciadas)
opt_old = """print("\\nOtimizando tabelas...")
spark.sql("OPTIMIZE lodlog_dw.fato_entregas ZORDER BY (sk_data, sk_cd_origem, indicador_atraso, sk_cat_atraso)")
spark.sql("OPTIMIZE lodlog_dw.dim_tempo ZORDER BY (sk_tempo)")
spark.sql("OPTIMIZE lodlog_dw.dim_cat_atraso ZORDER BY (sk_cat_atraso)")
spark.sql("OPTIMIZE lodlog_op.entrega ZORDER BY (status_entrega, data_saida)")
spark.sql("OPTIMIZE lodlog_op.pedido ZORDER BY (cliente_id, status_pedido)")
print("Otimização concluída.")"""
opt_new = """print("\\nOtimizando tabelas...")
# No Free Edition as tabelas gerenciadas já contam com Predictive Optimization;
# o OPTIMIZE manual é didático. Se alguma tabela recusar ZORDER, seguimos em frente.
_zorders = [
    ("lodlog_dw.fato_entregas", "(sk_data, sk_cd_origem, indicador_atraso, sk_cat_atraso)"),
    ("lodlog_dw.dim_tempo", "(sk_tempo)"),
    ("lodlog_dw.dim_cat_atraso", "(sk_cat_atraso)"),
    ("lodlog_op.entrega", "(status_entrega, data_saida)"),
    ("lodlog_op.pedido", "(cliente_id, status_pedido)"),
]
for _tbl, _cols in _zorders:
    try:
        spark.sql(f"OPTIMIZE {_tbl} ZORDER BY {_cols}")
        print(f"  ✓ OPTIMIZE {_tbl}")
    except Exception as e:
        print(f"  · {_tbl}: OPTIMIZE ignorado ({str(e)[:120]})")
print("Otimização concluída.")"""
assert opt_old in src
src = src.replace(opt_old, opt_new)

# Referência textual ao LAB
src = src.replace("Execute este notebook **uma única vez** antes do LAB 2.",
                  "Execute este notebook **uma única vez** antes do LAB 3 (compute Serverless).")

# BUGFIX validado em simulação: coluna descricao_feriado 100% None quebra a
# inferência de tipos do createDataFrame (CANNOT_DETERMINE_TYPE).
fix_old = '"descricao_feriado": None,'
fix_new = '"descricao_feriado": "Feriado nacional" if ds in _feriados else None,'
assert fix_old in src
src = src.replace(fix_old, fix_new)

open("/workspaces/Aulas/Aula-3/Labs/lodlog_lab3_seed_free.py", "w", encoding="utf-8").write(src)
print("seed free OK")

# ────────────────────────────────────────────────────────────────
# 2) DDL  →  Aulas/Aula-2/Labs/lodlog_modelo_dados_free.sql
# ────────────────────────────────────────────────────────────────
ddl = open("/workspaces/Labs/lodlog_modelo_dados_v3.sql", encoding="utf-8").read()

ddl = ddl.replace(
"""-- Modelo de Dados Completo — LAB 2 (Scaffold / Gabarito) — VERSÃO 2
-- Databricks SQL · Delta Lake · Community Edition compatible""",
"""-- Modelo de Dados Completo — LAB 2 (Scaffold / Gabarito) — VERSÃO FREE
-- Databricks SQL · Delta Lake · Databricks FREE EDITION (Unity Catalog)""")

ddl = ddl.replace(
"""-- COMO USAR:
--   1. Abra um notebook SQL no Databricks (Language: SQL)
--   2. Cole este script inteiro em uma célula  OU
--      divida cada bloco em células separadas (recomendado)
--   3. Execute de cima para baixo
--""",
"""-- COMO USAR (Databricks Free Edition — https://login.databricks.com):
--   1. Abra um notebook no Databricks Free Edition (Language: SQL)
--   2. O compute é Serverless (padrão do Free Edition) — nada a configurar
--   3. Cole este script inteiro em uma célula  OU
--      divida cada bloco em células separadas (recomendado)
--   4. Execute de cima para baixo
--
-- ════════════════════════════════════════════════════════════════
-- O QUE MUDA NA VERSÃO FREE (agosto/2026)
-- ════════════════════════════════════════════════════════════════
-- · O Community Edition foi descontinuado; o Free Edition usa
--   Unity Catalog: os schemas lodlog_op/lodlog_dw ficam dentro do
--   catálogo `workspace` (primeiro comando: USE CATALOG workspace)
-- · PRIMARY KEY / FOREIGN KEY são aceitas no Unity Catalog como
--   constraints INFORMATIVAS (não são fiscalizadas na escrita —
--   por isso o LAB 3 consegue "caçar" duplicatas e FKs órfãs!)
--""")

ddl = ddl.replace(
"""-- Diferenças vs PostgreSQL:
--   · SCHEMA → DATABASE  (Databricks Community usa Hive Metastore)""",
"""-- Diferenças vs PostgreSQL:
--   · SCHEMA/DATABASE são sinônimos, dentro do catálogo `workspace`""")

ddl = ddl.replace(
"""-- ================================================================
-- CÉLULA 1 — Criar databases (equivalente a schemas)
-- ================================================================

CREATE DATABASE IF NOT EXISTS lodlog_op""",
"""-- ================================================================
-- CÉLULA 1 — Catálogo e schemas
-- No Free Edition todos os objetos vivem no catálogo `workspace`.
-- ================================================================

USE CATALOG workspace;

CREATE DATABASE IF NOT EXISTS lodlog_op""")

open("/workspaces/Aulas/Aula-2/Labs/lodlog_modelo_dados_free.sql", "w", encoding="utf-8").write(ddl)
print("ddl free OK")
