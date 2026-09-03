# Contexto da Pasta: para-postgresql

Adaptações dos scripts SQL do modelo de dados LODLog para **PostgreSQL** (em oposição ao Databricks Community Edition). Scripts de referência para quem precisa rodar o modelo em um SGBD relacional tradicional.

## Principais arquivos
- `lodlog_v3_dbo.sql` — DDL do **schema operacional** `lodlog_op` em PostgreSQL: domínios cliente, endereço, contrato, frota (veiculo/motorista/manutencao), estoque, pedido, entrega (em 2FN proposital).
- `lodlog_v3_dw.sql` — DDL do **schema analítico** `lodlog_dw` em PostgreSQL: dimensões Star Schema + `fato_entregas`.

## Regras e padrões
- Conversões do Databricks para PostgreSQL:
  - `SCHEMA` → `DATABASE`
  - `BIGINT SERIAL` (IDENTITY) em vez de PKs geradas na aplicação
  - `STRING` → `TEXT`, `DECIMAL` → `NUMERIC`
  - `USING DELTA` removido (Delta Lake é específico do Databricks)
  - `FOREIGN KEY` agora executável (PostgreSQL aplica)
  - `COMMENT ON TABLE` em vez de `COMMENT` inline no Databricks
- A estrutura conceitual do modelo é idêntica ao Databricks — só muda a sintaxe DDL e o engine de storage.
- Anomalias propositais em `entrega` (2FN) mantidas para exercício LAB2.

## Informações relevantes
- Útil para execução local/offline do modelo antes de subir para Databricks.
- O seed de dados sintéticos (`lodlog_lab3_seed_v3.py`) é Databricks-only (PySpark); o PostgreSQL é só para DDL de referência.
- Versões: v2 (junho/2026) — `lodlog_modelo_dados.sql` — e v3 (junho/2026) — `lodlog_modelo_dados_v3.sql`.
