# Contexto da Pasta: Labs da Aula 4-5

Pasta de laboratório da **Aulas 4 e 5 — Miniprojeto: Construção e Avaliação de Data Lake** (03 de outubro de 2026), Módulo 4 da disciplina **Arquitetura de Dados e Big Data** (MBA FGV).

## Principais arquivos
- `LAB4.md` — Laboratório adaptado: Miniprojeto de Construção e Avaliação de Data Lake (executivo/estudante).
- `lab4_miniprojeto_starter.py` — Notebook starter executável no **Databricks Free Edition**: pipeline Medallion completo (Bronze JSON semiestruturado + TMS estruturado → Silver limpa/deduplicada → Gold agregada + análise). Roda em ~1 min; os grupos adaptam ao cenário escolhido. **Validado em simulação local Spark+Delta (ago/2026).**
- `../aula-4-5.md` — Conteúdo completo do slide deck da Aula 4-5.
- `../syllabus.md` — Ementa oficial da disciplina.

## Regras e padrões
- **Linguagem:** português brasileiro, acessível para executivos e estudantes. Linguagem direta, foco no que importa para o negócio.
- **Sessão dupla:** teoria curta (40 min) + miniprojeto prático (2h20), com 2 intervalos de 15 min obrigatórios.
- **Alinhamento obrigatório** com `syllabus.md` — seção Módulo 4 (objetivos de aprendizagem, conteúdo programático, avaliação).
- **Avaliação:** trabalho (70% individual + 30% grupo). Disciplina isenta de prova.
- **Conexão:** culminação de tudo que foi visto nas Aulas 1–3. O miniprojeto exige dados, arquitetura, queries e governança.

## Informações relevantes
- **4 sub-cenários disponíveis:** (A) Rotas, (B) Manutenção Preditiva, (C) Estoque, (D) Fraude em Faturamento.
- **Entrega individual (70%, prazo 15 dias após última aula):** relatório + DDL + 2 queries analíticas + 1 de qualidade + conexão IA.
- **Entrega em grupo (30%):** apresentação + avaliação pós-projeto.
- **Entregáveis da noite:** diagrama + tabela fonte×camada + 1 análise Gold + pitch 5 min/grupo.
- **Recomendação arquitetural para LODLog:** Lakehouse Delta (Bronze JSON/CSV + Silver/Gold Parquet Delta).
- **Não federar prematuramente** — o cenário LODLog cabe em um único workspace do Databricks Free Edition.
- **Ambiente:** Databricks **Free Edition** (https://login.databricks.com), compute Serverless, catálogo `workspace`. Schemas do miniprojeto: `lodlog_bronze`, `lodlog_silver`, `lodlog_gold` (podem consumir `lodlog_op.*` do LAB 3 como fonte estruturada).
- **Scripts de referência:** `lab4_miniprojeto_starter.py` (nesta pasta), `../../Aula-2/Labs/lodlog_modelo_dados_free.sql`, `../../Aula-2/Labs/lodlog_lab2_seed_free.py`, `../../Aula-3/Labs/LAB3.md`.
