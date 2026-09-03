# Contexto da Pasta: Aula 4-5 — Miniprojeto: Construção e Avaliação de Data Lake

**Aulas 4 e 5** — sessão dupla (03 de outubro de 2026), Módulo 4. Miniprojeto de construção e avaliação de data lake para a LODLog (lakehouse Bronze→Silver→Gold, governança, MLOps).

## Principais arquivos
- `aula-4-5.md` — Conteúdo completo do slide deck (≈677 linhas): 4 pilares de governança, pântano de dados, feature store + MLOps, checklist do miniprojeto, 4 sub-cenários (Rotas/Manutenção/Estoque/Fraude), hands-on Databricks (Lab 4.1/4.2/4.3), rubrica de avaliação (70% individual + 30% grupo).
- `../../../Labs/LAB4.md` — Laboratório teórico complementar.
- `../../../Labs/lodlog_modelo_dados_v3.sql` — DDL de referência para construção do lakehouse.

## Regras e padrões
- **Sessão dupla:** 40 min teoria + 2h20 miniprojeto prático (15 min intervalos obrigatórios).
- Entregáveis da noite: diagrama + tabela fonte×camada + 1 análise Gold + pitch 5 min/grupo.
- **Entrega individual (70%, 15 dias):** relatório + DDL + 2 queries analíticas + 1 de qualidade + conexão IA.
- **Grupo (30%):** apresentação + avaliação pós-projeto.
- 4 sub-cenários: (A) Rotas, (B) Manutenção Preditiva, (C) Estoque, (D) Fraude em Faturamento.
- Cada grupo escolhe **1 cenário** e entrega lakehouse simplificado com análise e pós-projeto.

## Informações relevantes
- Culminação das Aulas 1–3: "construir de ponta a ponta".
- Recomendação: **Lakehouse Delta** (Bronze JSON/CSV + Silver/Gold Parquet Delta); evolução futura para Data Mesh quando LODLog escalar.
- Não federar prematuramente — 450 veículos/5 CDs cabem em single-workspace Databricks CE.
- 4 pilares: Qualidade (DAMA 6 dimensões), Segurança/LGPD, Catálogo/Linhagem, Ciclo de Vida/Opera
