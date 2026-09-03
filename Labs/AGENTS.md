# Contexto da Pasta: Labs

> ⚠️ **Nota (ago/2026):** esta pasta guarda o material **original** da disciplina Engenharia de Dados para IA, que roda(va) no Databricks Community Edition (descontinuado). As versões adaptadas para a disciplina **Arquitetura de Dados e Big Data** no **Databricks Free Edition** estão em `Aulas/Aula-X/Labs/` (ver `Aulas/VALIDACAO-LABS.md`). Não edite os arquivos daqui para a nova disciplina — eles são a referência histórica.

Pasta de laboratórios práticos da disciplina **Engenharia de Dados para IA** (MBA FGV). Contém os 4 labs (LAB1–LAB4) em markdown, os documentos `.docx` correspondentes, scripts de seed de dados sintéticos e DDLs SQL para Databricks Community Edition (Spart

## Principais arquivos
- `LAB1.md` / `LAB2.md` / `LAB3.md` / `LAB4.md` — Laboratórios (teoria + exercícios)
- `LAB1.docx` … `LAB4.docx` — Versões Office dos labs
- `lodlog_lab3_seed_v3.py` — Gerador de dados sintéticos + ETL v3 (notebook Python Databricks)
- `lodlog_modelo_dados_v3.sql` — DDL completa ER 3FN + Star Schema (Databricks SQL)
- `lodlog_modelo_dados.sql` — DDL v2 (versão anterior, referenciada nos labs)
- `para-postgresql/lodlog_v3_dbo.sql` e `lodlog_v3_dw.sql` — DDLs equivalentes para PostgreSQL (adaptação SGBD)
- `LAB3_apoio.ipynb` — Notebook de apoio para execução das queries do LAB3
- `Suporte LODLog.ipynb` — Notebook de limpeza/reset do banco (DROP SCHEMA)

## Regras e padrões
- **Linguagem:** todo o conteúdo em **português brasileiro**.
- **Ambiente:** Databricks Community Edition (SQL + Python notebooks).
- **Esquema:** dois schemas — `lodlog_op` (3FN, transacional) e `lodlog_dw` (Star Schema analítico).
- **Tabelas de domínio operacional:** `cliente`, `endereco_cliente`, `contrato`, `veiculo`, `motorista`, `manutencao`, `telemetria`, `centro_distribuicao`, `produto`, `estoque`, `movimentacao_estoque`, `pedido`, `item_pedido`, `entrega`.
- **Dimensões DW:** `dim_tempo`, `dim_cliente` (SCD2), `dim_veiculo` (SCD2), `dim_motorista` (SCD2), `dim_centro_distribuicao` (SCD1), `dim_cat_atraso` (minidimensão Kimball).
- **Fato:** `fato_entregas` (~50k rows, target `indicador_atraso`).
- **Formato:** tabelas `USING DELTA`, `ZORDER BY` em high-cardinality.
- **Regra hard:** sempre atualizar `lodlog_dw` de forma coerente com `lodlog_op` — mudanças operacionais primeiro.
- **Anomalias propositais** em `fato_entregas` (230/49.770): duplicatas, negativos, outliers, FK quebrada — usadas no LAB3 QA.
- Executar com `%sql` ou notebook Python; `SHOW TABLES` após seed.

## Informações relevantes
- Labs 1–2 e 4 são teóricos (entrega em documento/diagrama); apenas LAB3 é executável.
- O seed v3 introduz anomalias de propósito para exercícios de qualidade de dados.
- Acesso Databricks: https://community.cloud.databricks.com — importar repo `https://github.com/Escola-de-Matematica-Aplicada/EDIA-Labs-DataBricks.git`.
