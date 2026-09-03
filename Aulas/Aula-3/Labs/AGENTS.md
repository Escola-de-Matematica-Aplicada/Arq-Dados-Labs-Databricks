# Contexto da Pasta: Labs da Aula 3

Pasta de laboratório da **Aula 3 — Organização e Manuseio de Dados em Bases Distribuídas** (29 de setembro de 2026), Módulo 3 da disciplina **Arquitetura de Dados e Big Data** (MBA FGV).

## Principais arquivos
- `LAB3.md` — Laboratório adaptado: SQL Avançado e Pipeline de Feature Engineering (executivo/estudante).
- `lodlog_lab3_seed_free.py` — Seed de dados sintéticos adaptado ao **Databricks Free Edition** (Unity Catalog). Inclui bugfix da `dim_tempo` (`descricao_feriado` toda NULL quebrava a inferência de tipos). **Validado em simulação local Spark+Delta (ago/2026): 50.000 linhas na fato, 230 anômalas.**
- `LAB3_apoio_free.ipynb` — Notebook de apoio com as queries guiadas + células TODO. Correções vs. original: `nome_completo` (não existe `nome_motorista` em `dim_motorista`) e JOIN da `vw_features_ml` por `sk_entrega` (o JOIN por cliente+data multiplicava linhas: 68.762 em vez de 50.000).
- `../aula-3.md` — Conteúdo completo do slide deck da Aula 3.
- `../syllabus.md` — Ementa oficial da disciplina.

## Regras e padrões
- **Linguagem:** português brasileiro, acessível para executivos e estudantes. Linguagem direta, exemplos práticos, sem jargão desnecessário.
- **Único lab executável obrigatório da disciplina** — atividades em Databricks Free Edition (SQL + Python, compute Serverless).
- **Alinhamento obrigatório** com `syllabus.md` — seção Módulo 3 (objetivos de aprendizagem, conteúdo programático, avaliação).
- **Conexão:** este lab é a base técnica para o miniprojeto da Aula 4-5 — as queries e a view `vw_features_ml` aqui criadas alimentam o projeto final.

## Informações relevantes
- **Ambiente:** Databricks **Free Edition** (https://login.databricks.com — o Community Edition foi descontinuado). Dados no catálogo `workspace`, schemas `lodlog_op`/`lodlog_dw`.
- **Scripts desta pasta:** `lodlog_lab3_seed_free.py`, `LAB3_apoio_free.ipynb`; DDL em `../../Aula-2/Labs/lodlog_modelo_dados_free.sql`. Originais (Community Edition) preservados em `../../../Labs/`.
- **Regra hard:** `lodlog_dw` deve ser atualizado de forma coerente com `lodlog_op` — mudanças operacionais primeiro.
- **Anomalias propositais** em `fato_entregas` (230/49.770): duplicatas, negativos, outliers, FK quebrada — usadas nos exercícios de data quality.
- **Conteúdo técnico:** Window Functions, Feature Store, Data Quality SQL, correlação, médias móveis.
