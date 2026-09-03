# Contexto da Pasta: Aula 3 — Organização e Manuseio de Dados em Bases Distribuídas

**Aula 3** do Módulo 3 (29 de setembro de 2026). Cloud (IaaS/PaaS/SaaS), Hadoop/Spark/Hive, pipelines ETL/ELT, Lambda/Kappa e arquitetura em camadas.

## Principais arquivos
- `aula-3.md` — Conteúdo completo do slide deck (≈571 linhas): cloud computing, Hadoop (HDFS/YARN/MapReduce), Spark Catalyst, Kafka/Flink/Airflow/dbt/Debezium/NiFi, formatos CSV/JSON/Avro/Parquet/ORC/Delta, ETL vs ELT, batch vs streaming, Lambda vs Kappa vs híbrido, pipeline fim-a-fim LODLog.
- `Labs/lodlog_lab3_seed_free.py` — Seed de dados adaptado ao Databricks Free Edition (original: `../../../Labs/lodlog_lab3_seed_v3.py`).

## Regras e padrões
- Slides com `<!-- Slide number: N -->` e validação GraphRAG `[DRIFT-xx]`.
- **Regra dura:** 50% teoria / 50% prática.
- Prática: desenhar pipeline conceitual ingestão → processamento → consumo por domínio LODLog, justificando ETL/ELT + batch/streaming/Lambda/Kappa.
- Laboratório executável em Databricks Free Edition (`%sql` + PySpark, compute Serverless, catálogo `workspace`).

## Informações relevantes
- Aula conecta "onde guardar" (Aula 2) ao "como mover e transformar" (pipelines).
- LODLog usa os 5 padrões de ingestão: streaming (IoT/TMS), batch (ERP/IBGE), CDC, API pull, micro-batch (WMS).
- Recomendação: **híbrido** — streaming para alertas, batch para analytics/ML.
- Conexão direta com LAB3 (SQL avançado + feature engineering) e LAB4 (miniprojeto).
- "Armazenamento Bronze nunca é reescrito destrutivamente" — princípio-chave do ELT Lakehouse.
