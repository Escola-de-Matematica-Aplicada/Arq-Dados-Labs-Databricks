# Contexto da Pasta: Labs da Aula 2

Pasta de laboratório da **Aula 2 — Ferramentas para Gerenciamento de Dados Distribuídos** (28 de setembro de 2026), Módulo 2 da disciplina **Arquitetura de Dados e Big Data** (MBA FGV).

## Principais arquivos
- `LAB2.md` — Laboratório adaptado: Modelagem de Dados para Analytics (executivo/estudante).
- `lodlog_modelo_dados_free.sql` — DDL completa (ER 2FN/3FN + Star Schema) adaptada ao **Databricks Free Edition** (Unity Catalog, catálogo `workspace`). **Validada em simulação local Spark+Delta (ago/2026).**
- `../aula-2.md` — Conteúdo completo do slide deck da Aula 2.
- `../syllabus.md` — Ementa oficial da disciplina.

## Regras e padrões
- **Linguagem:** português brasileiro, acessível para executivos e estudantes. Analogias claras, foco no que importa para o negócio.
- **Aulas 1 e 2 são teóricas** — o lab combina teoria de arquiteturas + atividades de modelagem.
- **Alinhamento obrigatório** com `syllabus.md` — seção Módulo 2 (objetivos de aprendizagem, conteúdo programático, avaliação).
- **Conexão:** este lab é a base para o Lab 3 (Aula 3) e o miniprojeto da Aula 4-5 — a modelagem definida aqui alimenta as queries e o lakehouse.

## Informações relevantes
- O cenário LODLog é o estudo de caso contínuo.
- **Conteúdo técnico principal:** arquiteturas (DW/Lake/Lakehouse/Mesh), Medallion (Bronze/Silver/Gold), normalização 3FN, Star Schema, mini-dimensão Kimball.
- **Pode usar o RPG "As Cinco Torres Isoladas"** como dinâmica complementar (materiais em `docs/Aulas-de-outros-cursos/Aula 8 Arquitetura de Dados/`).
- **Ambiente:** Databricks **Free Edition** (https://login.databricks.com — o Community Edition foi descontinuado). Compute Serverless; schemas no catálogo `workspace`.
- Scripts de referência: `lodlog_modelo_dados_free.sql` e `lodlog_lab2_seed_free.py` (ambos nesta pasta — DDL + seed/ETL são executados na Aula 2). Originais (Community Edition) preservados em `../../../Labs/`.
- **Números do cenário:** narrativa = 450 veículos, 12 CDs, ~18 mil entregas/mês; dataset de lab = recorte com 5 CDs, 50 veículos, ~50 mil entregas (2024–2026).
