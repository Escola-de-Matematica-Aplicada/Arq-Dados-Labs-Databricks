# Contexto Completo do Projeto - Hermes

**EDA — Engenharia de Dados para Inteligência Artificial** | MBA em IA e Analytics Aplicados a Negócios — FGV

## Visão Geral

Repositório de labs da disciplina **Engenharia de Dados para IA** (MBA FGV), usando como estudo de caso contínuo a empresa fictícia de logística **LODLog Transportes e Distribuição S.A.** (450 veículos, 5 CDs, ~50k entregas/mês). A disciplina é isenta de prova — avaliação por trabalho (70% individual + 30% grupo). Labs 1–2 e 4 são teóricos; apenas o **LAB3** é executável em Databricks Community Edition.

## Árvore de Diretórios Resumida

```
/workspaces/
├── README.md                    # ID do repositório (EDIA-Labs-DataBricks)
├── syllabus.md                  # Ementa completa: 4 módulos, cronograma, avaliação, bibliografia
├── CLAUDE.md                    # Contexto do projeto (modelo de dados, regras hard)
├── Labs/                        # Laboratórios (markdown + docx + scripts SQL/Python)
│   ├── LAB1.md / LAB2.md / LAB3.md / LAB4.md   # Labs teoria + exercícios
│   ├── lodlog_modelo_dados_v3.sql             # DDL completa ER 3FN + Star Schema (Databricks)
│   ├── lodlog_lab3_seed_v3.py                 # Gerador de dados sintéticos + ETL v3
│   └── para-postgresql/                       # DDLs equivalentes para PostgreSQL
├── Aulas/                     # Slides das 4 aulas (módulos 1–4)
│   ├── Aula-1/  (tipos de dados, 5 Vs, OLTP vs OLAP)
│   ├── Aula-2/  (NoSQL, DW/Lake/Lakehouse, Medallion, RPG)
│   ├── Aula-3/  (cloud, Hadoop/Spark, ETL/ELT, Lambda/Kappa)
│   └── Aula-4-5/ (miniprojeto lakehouse, governança, MLOps)
└── Diagramas/               # Diagramas ER (lodlog_op) e Star Schema (lodlog_dw) em PNG
```

## Modelo de Dados LODLog (Duas Camadas)

**`lodlog_op`** (operacional, 3FN): domínios `cliente/endereco_cliente/contrato`, `veiculo/motorista/manutencao/telemetria` (IoT particionada por `data_evento`), `centro_distribuicao/produto/estoque/movimentacao_estoque`, `pedido/item_pedido/entrega` (propositalmente em 2FN — exercício LAB2).

**`lodlog_dw`** (analítico, Star Schema): fato `fato_entregas` (~50k rows, target `indicador_atraso`), dims `dim_tempo`, `dim_cliente` (SCD2), `dim_veiculo` (SCD2), `dim_motorista` (SCD2), `dim_centro_distribuicao` (SCD1), `dim_cat_atraso` (minidimensão Kimball). Usando Delta Lake com `ZORDER BY` em high-cardinality.

**Regra hard:** sempre atualizar `lodlog_dw` de forma coerente com `lodlog_op` — mudanças operacionais primeiro.

## Lab 3 — Executável (único lab com código)

Ambiente: Databricks Community Edition (importar repo `https://github.com/Escola-de-Matematica-Aplicada/EDIA-Labs-DataBricks.git`). Após rodar `lodlog_lab3_seed_v3.py` e `lodlog_modelo_dados_v3.sql`:
- **Parte 1:** SQL analítico (JOINs, agregações, correlação) e query de pontualidade por cliente.
- **Parte 2:** Window Functions — média móvel 7d, NTILE/PERCENT_RANK por motorista.
- **Parte 3:** Feature Engineering — view `vw_features_ml` com 9 features + target para ML.
- **Parte 4:** Qualidade de dados — detecção de duplicatas, negativos, outliers, FK quebrada (anti-join).

Anomalias propositais em `fato_entregas`: 100 duplicatas `pedido_id`, 50 valores negativos, 30 outliers estatísticos, 50 linhas com FK quebrada (`sk_cliente` 201–300).

## Aulas — Estrutura

| Aula | Data | Módulo | Foco |
|------|------|--------|------|
| 1 | 22-set | M1 | Tipos de dados, 5 Vs, OLTP vs OLAP, LODLog fontes |
| 2 | 28-set | M2 | NoSQL, DW/Lake/Lakehouse, Medallion, RPG 5 Torres |
| 3 | 29-set | M3 | Cloud IaaS/PaaS/SaaS, Spark, ETL/ELT, Lambda/Kappa |
| 4-5 | 03-out | M4 | Miniprojeto lakehouse (governança 4 pilares, MLOps) |

Cada aula: 19h–22h20, 50% teoria / 50% prática, 15min intervalo.

## Conceitos-Chave
- **5 Vs** (Volume/Variedade/Velocidade/Veracidade/Valor) aplicados às 8 fontes LODLog (IoT, ERP, WMS, TMS, Maps, INMET, ANTT, IBGE).
- **Medallion:** Bronze (raw) → Silver (limpo) → Gold (curado) — padrão Zaloni 5 zonas.
- **Arquiteturas:** DW, Data Lake, Lakehouse (Delta/Iceberg/Hudi), Data Mesh, Data Fabric — Lakehouse recomendado para LODLog.
- **SCD Tipo 2** para dimensões que evoluem (cliente, veículo, motorista); **SCD Tipo 1** para CD e categoria de atraso.
- **Mini-dimensão** Kimball para KPI de baixa cardinalidade (`dim_cat_atraso`, 5 registros).
- **Feature Store** em SQL: view `vw_features_ml` alimentando modelo de predição de atraso.
- **LGPD:** anonimização na Gold, direito ao esquecimento, retenção por camada, controle de acesso.

## Referências
- **Bibliografia básica:** Serra (2024) *Deciphering Data Architectures*; Silva et al. (2020) *Cloud Computing*; Inmon et al. (2019) *Data Architecture*.
- **Complementar:** Kaufmann & Meier (2023); Kleppmann (2017) *Designing Data-Intensive Applications*.
- Validação GraphRAG drift em `/workspaces/graphrag/hpc-v100` (modelo `agnes-2.5-flash`) — conteúdo do curso possui anotações `[DRIFT-xx]`.

## Subpastas — AGENTS.md

Cada subpasta possui um arquivo `AGENTS.md` com descrição, arquivos principais, regras e informações específicas para trabalho no contexto daquela pasta:

- `Labs/AGENTS.md` — Laboratórios, scripts SQL, seed, estrutura de dados e regras Databricks.
- `Aulas/Aula-1/AGENTS.md` — Slides Aula 1 (tipos de dados, 5 Vs, OLTP vs OLAP).
- `Aulas/Aula-2/AGENTS.md` — Slides Aula 2 (NoSQL, Medallion, RPG).
- `Aulas/Aula-3/AGENTS.md` — Slides Aula 3 (cloud, Spark, pipelines, ETL/ELT).
- `Aulas/Aula-4-5/AGENTS.md` — Slides Aula 4-5 (miniprojeto lakehouse, governança, MLOps).
- `Diagramas/AGENTS.md` — Diagramas ER e Star Schema (PNG).
- `Labs/para-postgresql/AGENTS.md` — DDLs para PostgreSQL (adaptação do Databricks).

<!-- RESUMIDO: conteúdo detalhado dos arquivos individuais (aula-1.md ≈1029 linhas, aula-2.md ≈597 linhas, aula-3.md ≈571 linhas, aula-4-5.md ≈677 linhas, lodlog_lab3_seed_v3.py ≈1283 linhas, lodlog_modelo_dados_v3.sql ≈512 linhas) está resumido neste contexto. Consulte os AGENTS.md de cada subpasta e os arquivos-fonte para detalhes. -->

Total de caracteres: 18432/20000
