# Arquitetura de Dados e Big Data
Aula 4-5 — 03 de outubro de 2026
Módulo 4 — Miniprojeto: Construção e Avaliação de Data Lake para a LODLog

### Notes:
Turma MBA em Inteligência Artificial e Analytics Aplicados a Negócios
Professor: Júlio César Chaves — julio.cesar.chaves@fgv.br
Horário: 19h00 às 22h20 — Sessão dupla (Aulas 4 e 5) | Teoria curta 40min | Miniprojeto em grupo 2h40 + intervalos
Syllabus: Módulo 4 — Miniprojeto lakehouse. Duração 24h/a total. Disciplina isenta de prova.

<!-- Slide 1: Capa -->
# Arquitetura de Dados e Big Data
## Aulas 4 e 5 — Módulo 4: Miniprojeto — Construção e Avaliação de Data Lake
### 03 de outubro de 2026 | 19h00–22h20 | Sessão dupla | FGV MBA em IA e Analytics
**Lakehouse LODLog · Governança (4 pilares) · Bronze → Silver → Gold · Dados estruturados + não estruturados · Análise e Pós-projeto**
> Sessão dupla de encerramento — da teoria à entrega. Validado via GraphRAG drift — root `/workspaces/graphrag/hpc-v100` — modelo `agnes-2.5-flash` — 4 queries a validar

### Notes:
Capa. Posicionar M4 como "construir de ponta a ponta" — tudo das Aulas 1-3 culmina aqui. Sessão dupla: sem prova, com trabalho.

<!-- Slide 2: Regra de ouro — sessão dupla -->
# Regra da Sessão Dupla: Teoria Curta + Prática Longa
| Bloco | Horário | Duração | Conteúdo |
|---|---|---|---|
| **Teoria curta** | 19h00–19h40 | 40min | 4 pilares de governança + checklist + pântano + MLOps |
| **Intervalo 1** | 19h40–19h55 | 15min | — |
| **Miniprojeto — Parte 1** | 19h55–20h55 | 60min | Escolha de cenário + requisitos + desenho Bronze/Silver/Gold |
| **Intervalo 2** | 20h55–21h10 | 15min | — |
| **Miniprojeto — Parte 2** | 21h10–22h20 | 70min | Construção no Databricks + análise Gold + pitch 5min/grupo + síntese |

> Hard rule do syllabus mantida: cada aula tem 50% teoria / 50% prática — na sessão dupla, a teoria é concentrada no início e a prática ocupa o restante. Cada intervalo conta para os 15min obrigatórios.

### Notes:
Exibir relógio. Teoria é objetiva: dar o "cinto de segurança" antes de construir. Cobrar entrega parcial ao final.

<!-- Slide 3: Cronograma revisitado -->
# Onde estamos no syllabus
| Aula | Data | Módulo | Foco |
|---|---|---|---|
| 1 | 22-set | M1 — Tipos de dados e Big Data | Visto: OLTP vs OLAP, tipos, 5 Vs, 8 fontes LODLog |
| 2 | 28-set | M2 — Ferramentas distribuídas | Visto: NoSQL, DW/Lake/Lakehouse/Mesh/Fabric, Medallion/Zaloni, RPG |
| 3 | 29-set | M3 — Organização e manuseio | Visto: cloud IaaS/PaaS/SaaS, Hadoop/Spark, ETL/ELT, Lambda/Kappa |
| **4 e 5** | **03-out** | **M4 — Miniprojeto Lakehouse** | **Hoje: governança + construir e avaliar data lake LODLog** |

> Linha narrativa: M1 *quê* (dados) → M2 *onde* (arquiteturas) → M3 *como mover* (pipelines) → **M4 *construir* (lakehouse fim-a-fim)**.

### Notes:
2 min de recapitulação. Perguntar: "quem lembra a diferença ELT vs ETL?" para aquecer.

<!-- Slide 4: Objetivos de aprendizagem Módulo 4 -->
# Objetivos de Aprendizagem — Módulo 4
Ao final da sessão dupla o estudante será capaz de:
1. **Construir** um data lake/lakehouse com camadas Bronze → Silver → Gold no Databricks.
2. **Integrar** dados estruturados (ERP/WMS/TMS) e não/semi-estruturados (IoT JSON, APIs) no mesmo lakehouse.
3. **Conduzir** uma análise sobre a camada Gold e contar a história com dados.
4. **Descrever** as etapas percorridas (requisitos → ingestão → curadoria → consumo).
5. **Avaliar** vantagens, limitações e lições aprendidas do projeto (pós-projeto).
6. **Aplicar** os 4 pilares de governança para evitar o pântano de dados.

Fonte: syllabus Módulo 4 — "Construir um data lake, conduzir análises, resumir lições, avaliar arquitetura".

### Notes:
Ler objetivos em voz alta. Reforçar 70% individual + 30% grupo na avaliação.

<!-- Slide 5: Recapitulação Aulas 1–3 em 90 segundos -->
# Recapitulação Relâmpago — Aulas 1 a 3
- **Aula 1:** OLTP 3FN vs OLAP star · Estruturado/semi/não · 5 Vs (864k IoT/dia, 30s, 3 tipos, Veracidade 4 camadas, Valor R$4,2M multas) · 8 fontes LODLog mapeadas.
- **Aula 2:** Polyglot NoSQL (KV/Doc/Coluna/Grafo) · DW vs Lake vs Lakehouse vs Mesh vs Fabric · Medallion Bronze/Silver/Gold ↔ Zaloni 5 zonas · RPG → porta secreta = contratos + governança federada leve.
- **Aula 3:** IaaS/PaaS/SaaS · Hadoop HDFS/YARN/MR + Hive/HBase/Sqoop/Flume/Oozie · Spark RDD/Catalyst (10–100× MR) · Kafka/Flink/Airflow/dbt/Debezium · Parquet/Delta/Iceberg · 5 padrões ingestão · ETL vs ELT · Lambda/Kappa/híbrido · Pipeline fim-a-fim.
- **Pergunta-ponte:** "Se já sabemos *quê*, *onde* e *como mover* — por que tantos lakes viram pântanos?"

### Notes:
Recapitulação ativa: pedir 1 takeaway por mesa.

<!-- Slide 6: Agenda da noite dupla -->
# Agenda da Noite Dupla (03-out)
**Teoria curta — 40 min (19h00–19h40):**
1. O pântano de dados: por que lakes falham (5 min)
2. Governança em 4 pilares: qualidade, segurança/LGPD, catálogo/linhagem, ciclo de vida (20 min)
3. Feature store + MLOps + papéis + checklist do miniprojeto (15 min)

**Miniprojeto em grupo — 2h20 (19h55–22h20):**
4. Briefing + 4 sub-cenários LODLog (10 min)
5. Mão na massa 1 — requisitos + desenho Bronze/Silver/Gold (40 min)
6. Mão na massa 2 — construção Databricks + análise Gold (50 min)
7. Pitch 5 min/grupo + avaliação pós-projeto + síntese (30 min)

> Entregáveis da noite: diagrama + tabela fonte×camada + 1 análise Gold + pitch. Entrega individual em 15 dias.

### Notes:
Exibir cronômetro visível. Reforçar: não precisa estar perfeito hoje; precisa estar coerente e defensável.

<!-- Slide 7: Divisor Teoria -->
# PARTE 1 — TEORIA CURTA (40 min)
## O cinto de segurança antes de construir

### Notes:
Divisor de seção. 40 min cronometrados — sem estender.

<!-- Slide 8: O pântano de dados -->
# O Pântano de Dados (Data Swamp) — o anti-Lake
- **Definição:** lake sem governança — dados sem catálogo, sem dono, sem qualidade, sem linhagem. Vira lixão caro.
- **Sintomas:** ninguém confia nos números; duplicatas; `select *` varre TBs; reprocessar = reextrair da origem; LGPD exposta; dashboards divergem.
- **Causas (Aula 2→3 revisitadas):** Bronze sem particionamento; Silver sem deduplicação/validação; Gold sem contrato; sem DDL versionado; sem retenção/vacuum; sem.owner por domínio.
- **Custo LODLog:** 26M eventos IoT/mês × 12 meses sem particionamento = scan de 300M linhas por query → US$ 100s por dashboard + multas LGPD.
- **Antídoto:** os 4 pilares a seguir + Medallion disciplinado (Aula 2) + ELT com Bronze imutável (Aula 3).

> "Um data lake sem governança é só um data swamp com marketing." — Bill Inmon (2019)

### Notes:
Mostrar foto swamp vs lake. Conectar com RPG Porta Secreta: governança federada leve evita swamp.

<!-- Slide 9: Governança — visão 4 pilares -->
# Governança do Data Lake — 4 Pilares
| Pilar | Pergunta | Artefato LODLog | Dono |
|---|---|---|---|
| **1. Qualidade** | Posso confiar? | Scorecard DAMA 6 dimensões + contrato Silver/Gold | Data Steward + Eng. Dados |
| **2. Segurança & LGPD** | Quem pode ver/mudar/apagar? | Classificação + anonimização + retenção + direito ao esquecimento | DPO + DBA |
| **3. Catálogo & Linhagem** | Onde está e de onde veio? | Catalog (Hive/Glue/Purview) + lineage Bronze→Gold | Eng. Dados + PO Dados |
| **4. Ciclo de vida & Operação** | Quanto tempo guardar e quanto custa? | Particionamento `ano/mes/dia` + retenção 90d Bronze + vacuum + monitoramento | DBA + FinOps |

> Sem os 4, não há lakehouse — há pântano. O checklist do slide 18 cobra um por um.

### Notes:
Desenhar 4 colunas no quadro. Cada grupo será cobrado em 1 pilar no pitch.

<!-- Slide 10: Pilar 1 — Qualidade (DAMA) -->
# Pilar 1 — Qualidade de Dados (DAMA-DMBOK)
| Dimensão | Definição | Métrica LODLog | Threshold |
|---|---|---|---|
| **Completude** | Campos obrigatórios preenchidos? | % IoT com 11 campos preenchidos | ≥ 98% |
| **Acurácia** | Reflete a realidade? | % GPS dentro do Brasil (-34 a 5 lat) | ≥ 99% |
| **Consistência** | Uniforme entre sistemas? | % pedidos com mesmo status TMS↔WMS | ≥ 97% |
| **Atualidade** | Chega a tempo? | Lag IoT→Silver p50 | ≤ 5 min (streaming) |
| **Unicidade** | Sem duplicatas? | Taxa duplicação Bronze (`veiculo_id+timestamp`) | ≤ 0,1% |
| **Validade** | Formato correto? | % timestamps ISO 8601 + ranges (0–200 km/h, 50–150°C) | ≥ 99,5% |

- **Scorecard:** média ponderada 0–100 por fonte e por pipeline; semáforo 🟢≥90 🟡70–89 🔴<70.
- **Contrato Silver/Gold:** schema-on-write tipado (Parquet/Delta) — rejeita fora do contrato.

### Notes:
Mostrar Lab 4.2: scorecard automatizado em Spark. Conectar com Aula 1 Veracidade 4 camadas.

<!-- Slide 11: Pilar 2 — Segurança e LGPD -->
# Pilar 2 — Segurança, Privacidade e LGPD
- **Classificação:** `publico` / `interno` / `confidencial` / `pessoal (LGPD art.5)`. Ex: `motorista.nome`, `cliente.endereco` = pessoal; `sensor.temperatura` = interno.
- **Anonimização na Gold:** hash/pseudonimização de PII para consumo BI/ML; Bronze mantém original com acesso restrito.
- **Criptografia:** em repouso (S3 SSE, ADLS) + em trânsito (TLS); chaves por domínio.
- **Controle de acesso por camada:** Bronze (só engenharia) → Silver (time dados) → Gold (analistas/ML com RLS por CD/região).
- **Retenção por sensibilidade:** Bronze 90 dias → Silver 1 ano → Gold conforme política (financeiro 5 anos; PII sob consentimento).
- **Direito ao esquecimento:** `DELETE FROM silver WHERE cliente_id = X` + vacuum + propagação para Gold/feature store; log de auditoria.
- **LODLog prático:** motorista pede exclusão → pipeline anonimiza Gold em 72h; relatório de impacto no score.

### Notes:
LGPD não é opcional. Sem anonimização na Gold, BI expõe PII. Demo no Lab 4.2.

<!-- Slide 12: Pilar 3 — Catálogo, Metadados e Linhagem -->
# Pilar 3 — Catálogo, Metadados e Linhagem
- **Catálogo:** Hive Metastore / AWS Glue Catalog / Azure Purview / GCP Data Catalog — registra banco, tabela, colunas, tipos, partições, dono.
- **Metadados técnicos:** `bronze.iot_raw (JSON, 864k/dia, part ano/mes/dia)` → `silver.trusted_frota (Delta, dedup, range-validado)` → `gold.fato_frota_hora (agregada 1h, feature_temperatura_media)`.
- **Metadados de negócio:** dicionário (o que é `indicador_atraso`? 0/1), glossário, dono de domínio (frota/estoque/financeiro).
- **Linhagem (lineage):** `sensor_iot JSON → Bronze raw_iot → Silver trusted_frota → Gold feature_temperatura_media → modelo manutenção preditiva` — rastreável para debug e auditoria.
- **Ferramentas:** OpenLineage + Marquez, DataHub, Atlas (Hadoop), Delta `DESCRIBE HISTORY`.
- **LODLog:** sem catálogo, cada `select *` vira caça ao tesouro; com catálogo, `SHOW TABLES LIKE 'gold.*'` responde em segundos.

### Notes:
Desenhar lineage no quadro. Mostrar `DESCRIBE HISTORY trusted_frota` e `delta.log`.

<!-- Slide 13: Pilar 4 — Ciclo de Vida e Operação -->
# Pilar 4 — Ciclo de Vida, Custos e Operação
- **Particionamento:** sempre `ano/mes/dia` (ou `ano/mes/dia/hora` para streaming); evita full scan; reduz custo 10–100× (S3 select).
- **Retenção:** Bronze 90 dias (raw barato, mas cresce), Silver 1 ano, Gold conforme consumo; política por sensibilidade (financeiro > operacional).
- **Vacuum & Optimize:** `VACUUM gold.fato_entregas RETAIN 168 HOURS` + `OPTIMIZE` (compacta small files — Aula 3 small files problem).
- **Monitoramento:** lag ingestão, taxa duplicação, scorecard diário, drift de schema, custo por domínio (tags FinOps).
- **Idempotência & Retry:** re-rodar DAG não duplica (Delta MERGE + partition overwrite); Airflow retry 2× + alerta SLA.
- **LODLog conta:** S3 1TB Bronze ≈ US$23/mês; EMR/Databricks 10 nós ≈ US$2/h — desligar dev fora do horário economiza 70%.

### Notes:
Conectar com Aula 3 custos/egress/lock-in. Small files → OPTIMIZE é obrigatório.

<!-- Slide 14: Papéis e Responsabilidades -->
# Quem faz o quê? — Papéis no Pipeline
| Papel | Responsabilidade no miniprojeto | Entrega |
|---|---|---|
| **Engenheiro de Dados** | Modelagem, ingestão, Bronze→Silver, qualidade técnica | Pipeline + DDL |
| **Cientista de Dados** | Feature store, modelo, drift, métricas ML | Features Gold + notebook ML |
| **Analista de Negócio** | Requisitos, KPIs, validação, storytelling | Dashboard + narrativa |
| **DBA / Admin** | Performance, backup, segurança, vacuum | Particionamento + retenção |
| **Data Steward** | Qualidade, metadados, dicionário, dono de domínio | Scorecard + catálogo |
| **Product Owner de Dados** | Priorização, valor, backlog, ponte com C-level | Roadmap + ROI |

> No miniprojeto, cada grupo assume todos os papéis — mas deve explicitar quem seria dono de cada decisão na LODLog real.

### Notes:
Cada grupo designa 1 "dono" por pilar para o pitch — facilita Q&A.

<!-- Slide 15: Lakehouse como arquitetura do miniprojeto -->
# Lakehouse LODLog — Posicionando a Solução
| Arquitetura | Quando usar | No miniprojeto |
|---|---|---|
| **Data Warehouse** | Só estruturado, BI tradicional | Não — perderia IoT JSON |
| **Data Lake puro** | Só raw, sem ACID | Não — viraria swamp |
| **Lakehouse (Delta/Iceberg)** | **Unifica lake + warehouse; ACID + ML + BI** | **Sim — Bronze JSON/CSV + Silver/Gold Parquet Delta** |
| **Data Mesh** | Múltiplos domínios autônomos maduros | Futuro: cada CD como domínio |

- **Recomendação syllabus §10.3:** Lakehouse Bronze/Silver/Gold com evolução para Mesh quando a LODLog escalar (450 veículos → 2000).
- **Por que agora:** 26M IoT/mês + 48k WMS/dia + 3k TMS/dia cabem em lakehouse single-workspace Databricks CE sem federar.

### Notes:
Revisitar Aula 2: Mesh é destino, Lakehouse é ponto de partida. Não federar prematuramente.

<!-- Slide 16: Databricks CE + Delta + FinOps prático -->
# Databricks CE + Delta — Stack do Miniprojeto
- **Por que Databricks CE:** gratuito, Spark + Delta nativo, `spark.read.json/csv`, `display()`, `write.format("delta").partitionBy("ano","mes","dia")`, `MERGE`, `time-travel`.
- **Delta essentials:** `CREATE TABLE ... USING DELTA PARTITIONED BY (ano, mes, dia)` · `MERGE INTO silver USING bronze ON ... WHEN MATCHED UPDATE` · `VACUUM` · `DESCRIBE HISTORY`.
- **Alternativas agnósticas:** o mesmo desenho roda em EMR/Glue, Synapse, Dataproc — trocar conector, manter Parquet/Delta.
- **FinOps do miniprojeto:** dados sintéticos (sem egress); `partitionBy` reduz scan; auto-terminate cluster; tag `dominio=frota|estoque|financeiro`.

> Lab 4.1 constrói Bronze→Gold inteiro com dados sintéticos — sem credencial externa, idempotente.

### Notes:
Abrir Databricks CE ao vivo 1 min para mostrar workspace.

<!-- Slide 17: Feature Store + MLOps — Gold que alimenta IA -->
# Feature Store (Gold) + MLOps — Fechando o Loop
```
Bronze/Silver (ELT) → Gold (fato_entregas, fato_frota_hora, dim_*) → Feature Store (ml_feature_store versionada) → Treinamento → Deploy → Monitoramento → Retreinamento
                                       ↓
                              Data drift · Model drift · Qualidade Gold
```
- **Feature store na Gold:** `ml_feature_store` com `distancia_km, peso_carga_kg, hora_saida_seno/cosseno, temp_media_motor_1h, ind_chuva, historico_atrasos_7d, dias_ultima_manutencao` — versionada, documentada, reusável.
- **Retreinamento:** periódico (semanal) ou triggerado por drift (ex: temperatura média subiu 5°C no verão).
- **Linhagem ML:** `feature → modelo → predição → log de predições` para auditoria.
- **Mínimo do miniprojeto:** 1 tabela Gold + 1 query que poderia alimentar 1 dos 3 modelos (atraso / manutenção / demanda).

### Notes:
Mostrar §3.3 do projeto: tabela de features. Não precisa treinar modelo real — basta propor feature store coerente.

<!-- Slide 18: Checklist do Miniprojeto Lakehouse -->
# Checklist do Miniprojeto — 4 Pilares em 10 Itens
| # | Item | Pilar | Feito? |
|---|---|---|---|
| 1 | Bronze imutável, particionado `ano/mes/dia`, JSON/CSV cru preservado | Ciclo de vida | ☐ |
| 2 | Silver deduplicada, range-validada, tipada Parquet/Delta, SCD2 onde precisa | Qualidade | ☐ |
| 3 | Gold agregada + feature store documentada | Qualidade/Linhagem | ☐ |
| 4 | Scorecard DAMA 0–100 por fonte/pipeline | Qualidade | ☐ |
| 5 | Classificação LGPD + anonimização na Gold + retenção por camada | Segurança | ☐ |
| 6 | Catálogo (Metastore/Glue) + dicionário + lineage Bronze→Gold | Catálogo | ☐ |
| 7 | Controle de acesso por camada (Bronze restrito) | Segurança | ☐ |
| 8 | Idempotência (MERGE/overwrite) + retry + vacuum/optimize | Operação | ☐ |
| 9 | Integração ≥1 estruturada (ERP/WMS/TMS) + ≥1 semi/não (IoT/APIs) | Arquitetura | ☐ |
| 10 | Análise Gold + pós-projeto (vantagens/limitações/lições) | Valor | ☐ |

> Use este checklist como Definition of Done do grupo hoje e do trabalho individual em 15 dias.

### Notes:
Imprimir/QR. Cada grupo marca ao final da noite.

<!-- Slide 19: Critérios de Sucesso e Anti-Padrões -->
# Critérios de Sucesso — e Como Falhar
| Sucesso (lake) | Falha (swamp) — anti-padrão |
|---|---|
| Reprocessar = reler Bronze (barato) | Reprocessar = reextrair da origem (caro, lento) |
| Erro isolado por camada, retry por stage | Erro em 1 fonte quebra tudo |
| Linhagem rastreável Bronze→Gold | "De onde veio esse número?" sem resposta |
| Schema-on-write tipado na Silver/Gold | Schema-on-read em todo lugar = caos |
| Acesso por camada + PII anonimizada | Bucket público + chave exposta (vazamento) |
| Particionado + vacuum (scan 100× menor) | Milhões de JSONs pequenos matam NameNode/custo |

- **10 mandamentos (resumo):** 1) Bronze imutável 2) Particione 3) Tipifique Silver 4) Deduplique 5) Valide range 6) Catalogue 7) Anonimize Gold 8) MERGE idempotente 9) Monitore drift 10) Documente lineage.

### Notes:
Ler mandamentos em voz alta. Cada mandamento vira pergunta do pitch.

<!-- Slide 20: Intervalo 1 -->
# Intervalo 1 — 15 min
## 19h40 – 19h55
> Na volta: briefing dos 4 sub-cenários + formação dos grupos. Tragam o checklist impresso.

### Notes:
Pausa. Professor organiza grupos e distribui sub-cenários.

<!-- Slide 21: Divisor Prática -->
# PARTE 2 — MINIPROJETO EM GRUPO (2h20)
## Construindo o lakehouse LODLog

### Notes:
Divisor de seção. A partir daqui é mão na massa — professor circula.

<!-- Slide 22: Briefing do Miniprojeto -->
# Miniprojeto — Briefing
**Objetivo:** cada grupo escolhe 1 sub-cenário LODLog e entrega, ao final da noite, um **lakehouse simplificado** com análise e pós-projeto — base para o trabalho avaliado.

**Entregáveis da noite (grupo, 30% da nota):**
1. Diagrama do lakehouse (fontes → Bronze → Silver → Gold → consumo).
2. Tabela por fonte: formato, tipo, frequência, camada Bronze/Silver, ferramenta, Lambda/Kappa/híbrido.
3. DDL de ≥1 fato + 2 dimensões + 1 query analítica + 1 de qualidade (ou rascunho SQL).
4. Uma análise sobre a Gold + avaliação pós-projeto (vantagens/limitações/lições) + pitch 5 min.

**Entrega individual (70%, 15 dias):** relatório + DDL + 2 queries analíticas + 1 de qualidade + conexão IA (ver rubrica slide 30).

### Notes:
Reforçar: hoje é rascunho avaliado formativamente; entrega individual é somativa.

<!-- Slide 23: Os 4 Sub-Cenários LODLog -->
# Os 4 Sub-Cenários — Escolha 1 por Grupo
| Cenário | Pergunta de negócio | Fontes mínimas (≥1 estruturada + ≥1 semi/não) | Gold alvo |
|---|---|---|---|
| **(A) Rotas de entrega** | Como reduzir atrasos e multas R$4,2M/ano? | IoT (JSON 30s) + TMS (CDC) + Maps API (5min) + INMET (horário) + ERP | `fato_entregas` + `fato_rota_tempo` + feature atraso |
| **(B) Manutenção preditiva** | Como evitar quebras e R$2,1M em reboque? | IoT (temp/RPM/vibração) + WMS (peças) + TMS (hodômetro) + ERP (custos) | `fato_frota_hora` + `feature_saude_frota` + score risco |
| **(C) Estoque e reposição** | Como evitar ruptura e horas extras R$1,8M? | WMS (15min) + TMS (pedidos) + IBGE (CSV mensal) + ANTT (eventos) | `fato_estoque_dia` + `fato_movimentacao` + previsão demanda |
| **(D) Fraude em faturamento** | Como detectar divergências e atrasos de 5 dias nos relatórios? | ERP (financeiro) + TMS (entregas) + WMS (volumes) + IoT (peso) | `fato_faturamento` + `fato_entregas` + regra anomalia |

> Sorteio ou escolha. Cada cenário cabe em Databricks CE com dados sintéticos dos Labs 4.x.

### Notes:
Distribuir 1 cenário por grupo (4–5 grupos). Se 5 grupos, duplicar (A) com variação.

<!-- Slide 24: Requisitos por Cenário — Detalhe -->
# Requisitos por Cenário — O que cada Gold responde
- **(A) Rotas:** SLA por CD/região, custo/km, impacto clima/tráfego; feature `historico_atrasos_7d` para modelo atraso.
- **(B) Manutenção:** temperatura média móvel 1h, RPM, vibração, dias desde última manutenção; alerta `temp >105°C por 2min`; score risco 0–100.
- **(C) Estoque:** nível por SKU/CD, giro, ruptura iminente (`estoque < minimo*1.2`); série temporal por SKU para Prophet/ARIMA.
- **(D) Fraude:** divergência `peso_TMS vs peso_IoT`, `volumes_WMS vs fatura_ERP`, duplicatas `pedido_id`, outliers `custo_combustivel/km`.

Cada grupo escolhe **2 KPIs** e **1 regra de alerta** do seu cenário para implementar na Gold.

### Notes:
KPIs viram queries analíticas do slide 27.

<!-- Slide 25: Passo a Passo do Miniprojeto (100 min) -->
# Passo a Passo — 100 min Hands-On
1. **Escolher cenário + listar 3–5 fontes** (10 min) — formato, tipo, frequência, volume (ex: IoT 864k/dia).
2. **Analisar 5 Vs por fonte** (10 min) — Valor/Veracidade/Variedade/Velocidade/Volume — tabela Lab 4.1.
3. **Desenhar Bronze → Silver → Gold** (15 min) — diagrama + particionamento + ETL vs ELT por fonte (ELT padrão).
4. **Preencher matriz ferramenta×camada** (10 min) — ingestão, armazenamento, processamento, consumo, orquestração.
5. **Construir no Databricks** (30 min) — rodar Labs 4.1/4.2/4.3 e adaptar para seu cenário.
6. **Analisar Gold + pós-projeto** (15 min) — 1 insight + vantagens/limitações/lições.
7. **Preparar pitch 5 min** (10 min) — diagrama + matriz + análise + pós-projeto.

> Template nos slides 26–29. Professor circula a cada 15 min.

### Notes:
Cronometrar cada etapa. Labs são ponto de partida — adaptar, não copiar.

<!-- Slide 26: Matriz Ferramenta × Camada — Template -->
# Template — Matriz Fonte × Camada (entregar preenchida)
| Fonte | Formato | Padrão ingestão | ETL/ELT | Batch/Streaming | Ferramenta ingestão | Bronze | Ferramenta Silver | Gold | Lambda/Kappa |
|---|---|---|---|---|---|---|---|---|---|
| (ex: IoT) | JSON | Streaming | ELT | Streaming | Kafka + Structured Streaming | JSON → Delta `ano/mes/dia` | Spark + Delta MERGE | Parquet Delta particionado | Kappa |
| (ex: ERP) | SQL | Batch diário | ELT | Batch | Airflow + JDBC | Parquet | Spark SQL + dbt | Delta | Batch puro |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

> Critério: coerência (padrão ↔ latência ↔ ferramenta), custo e reprocessamento. Híbrido é default LODLog (Aula 3).

### Notes:
Entregar impressa/QR. Preencher de trás para frente (começar pela latência de consumo).

<!-- Slide 27: DDL e Queries — O que entregar -->
# DDL e Queries — Mínimo Avaliado
**DDL (≥1 fato + 2 dimensões, Delta):**
```sql
CREATE TABLE gold.fato_entregas (sk_entrega BIGINT, sk_data INT, sk_cliente INT, sk_veiculo INT, distancia_km DOUBLE, tempo_real_min INT, indicador_atraso INT) USING DELTA PARTITIONED BY (ano, mes);
CREATE TABLE gold.dim_veiculo (sk_veiculo INT, veiculo_id STRING, tipo STRING, capacidade_kg DOUBLE) USING DELTA;
```

**2 Queries analíticas (exemplos):**
- Eficiência por CD/região (custo/km, SLA).
- Ranking de atraso por cliente/CD com `GROUP BY` + `AVG`.

**1 Query de qualidade:**
- Duplicatas `pedido_id` ou nulos `veiculo_id` — `GROUP BY ... HAVING COUNT(*)>1`.

Ver Lab 4.3 e `Projeto-Eng-Dados-IA §14` para SQL completo (fato, dims, feature store, window 30d).

### Notes:
Não precisa ser sintaxe perfeita hoje — rascunho coerente basta. Individual exige SQL válido.

<!-- Slide 28: Dashboards — Operacional vs Executivo -->
# Dashboards — Quem consome a Gold?
| Painel | Latência | Público | KPIs LODLog | Fonte Gold |
|---|---|---|---|---|
| **Operacional** (15 min) | Streaming/micro-batch | Supervisor frota, CD | Entregas no prazo %, em rota, alertas 🔴🟡, temp motor >105°C | `fato_frota_hora`, `fato_entregas` |
| **Executivo** (diário) | Batch | C-Level | Custo/km por região, SLA 95% vs meta, multas, ROI dados | `fato_entregas` agregada, `fato_faturamento` |

- **Ferramentas:** Power BI / Tableau sobre views Gold, ou `display()` + matplotlib no Databricks.
- **Pergunta de ouro:** "que decisão muda se este número estiver errado?" — se nenhuma, não é KPI.

### Notes:
Mostrar mockups §8 do projeto. Cada grupo escolhe 1 dashboard para esboçar.

<!-- Slide 29: Avaliação Pós-Projeto — Template -->
# Pós-Projeto — Vantagens, Limitações, Lições
| Dimensão | Pergunta | Exemplo LODLog |
|---|---|---|
| **Vantagens** | O que o lakehouse habilitou? | Reprocessar 7 dias sem reextrair; ACID Delta; feature store reusável |
| **Limitações** | O que ainda dói? | Streaming caro para IBGE mensal; small files sem optimize; PII sem steward |
| **Lições** | O que faria diferente? | Particionar desde o dia 1; contrato Silver tipado; catalogar antes de popular |
| **Próximos passos** | Evolução? | CD como domínio Data Mesh; CDC em todo WMS; dbt para Silver→Gold |

> Esta tabela é a seção 10 do relatório individual e o fechamento do pitch em grupo. Seja honesto — banca valoriza autocrítica.

### Notes:
Lições honestas valem mais que "deu tudo certo". Conectar com swamp vs lake.

<!-- Slide 30: Rubrica de Avaliação — 70% + 30% -->
# Como Você Será Avaliado
**Individual — 70% — "Planejando o Pipeline de Dados para IA na LODLog" (15 dias, até 10 páginas):**
| Critério | Peso |
|---|---|
| Clareza do cenário escolhido | 10% |
| Mapeamento de fontes (3–5, internas+externas, Bronze/Silver) | 15% |
| Análise dos 5 Vs por fonte | 20% |
| Arquitetura coerente (Bronze/Silver/Gold, ETL/ELT, batch/streaming) | 15% |
| Qualidade SQL (DDL 3 tabelas + 2 analíticas + 1 qualidade) | 20% |
| Conexão IA / valor negócio (modelo + features Gold) | 15% |
| Apresentação/comunicação | 5% |

**Em grupo — 30% — Apresentação hoje (15 min na prática):**
| Critério | Peso |
|---|---|
| Compreensão do cenário | 10% | Modelagem ER+Star | 20% | Pipeline | 20% | Qualidade+LGPD+Linhagem | 15% | Casos IA | 20% | Apresentação | 10% | Extras (SQL/protótipo) | 5% |

### Notes:
Ler rubrica. Dúvidas sobre entrega individual agora.

<!-- Slide 31: Template do Pitch (5 min) -->
# Pitch do Grupo — 5 min + 2 min Q&A
1. **Cenário + pergunta de negócio** (30s) — "Escolhemos (A) Rotas para reduzir R$4,2M em multas".
2. **Diagrama Bronze→Silver→Gold** (60s) — fontes, particionamento, ETL/ELT, batch/streaming.
3. **Matriz ferramenta×camada** (60s) — 1 linha por fonte, justificativa Lambda/Kappa/híbrido.
4. **Análise Gold** (60s) — 1 insight com número ("CD Campinas 91,8% SLA, Sudeste pior custo/km").
5. **Pós-projeto** (60s) — 1 vantagem, 1 limitação, 1 lição + próximos passos.
6. **Q&A** (120s) — banca pergunta sobre governança do seu pilar sorteado.

> Dica: 1 slide/diagrama + 1 tabela + 1 query bastam. Menos é mais.

### Notes:
Cronometrar rigorosamente. Feedback imediato por grupo.

<!-- Slide 32: Intervalo 2 -->
# Intervalo 2 — 15 min
## 20h55 – 21h10
> Na volta: mão na massa Databricks — Labs 4.1 a 4.3. Abram https://community.cloud.databricks.com

### Notes:
Pausa. Grupos abrem Databricks CE e criam cluster.

<!-- Slide 33: Hands-On 1 — Lakehouse E2E -->
# Hands-On 1 — Lab 4.1: Lakehouse E2E (Bronze → Silver → Gold)
- **Arquivo:** `Labs/lab4-lakehouse-e2e.py` — pipeline completo idempotente, dados sintéticos, sem credencial.
- **O que faz:** gera IoT JSON 864k/dia simulado + ERP/WMS/TMS sintéticos → Bronze Delta particionado → Silver deduplicada/range-validada/enriquecida (join IBGE) → Gold `fato_entregas` + `fato_frota_hora` + `dim_*` → `OPTIMIZE` + `VACUUM` + `DESCRIBE HISTORY`.
- **Como usar:** Databricks CE → `File → Upload` ou copiar célula a célula; `BASE=/tmp/lodlog_lab4`; re-executável (overwrite + MERGE).
- **Adaptação por cenário:** (A) focar `fato_entregas`; (B) focar `fato_frota_hora` + janela 1h; (C) focar WMS+IBGE; (D) focar ERP+TMS divergência.

### Notes:
Demo ao vivo 2 min: mostrar `display(spark.read.format("delta").load(...))`.

<!-- Slide 34: Hands-On 2 — Governança e Qualidade -->
# Hands-On 2 — Lab 4.2: Governança e Qualidade
- **Arquivo:** `Labs/lab4-governanca-qualidade.py` — scorecard DAMA + LGPD + catálogo + linhagem.
- **O que faz:** calcula 6 dimensões (completude, acurácia GPS, consistência TMS↔WMS, atualidade, unicidade, validade) → score 0–100 com semáforo; anonimiza PII na Gold (hash motorista/cliente); cria dicionário e lineage `Bronze→Silver→Gold`; registra catálogo (Metastore) + `DESCRIBE DETAIL`.
- **Como usar:** rodar após Lab 4.1 (depende de Bronze/Silver existentes); ajustar thresholds por cenário.
- **Saída esperada:** `scorecard_por_fonte` + `gold_anonimizada` + `lineage` printado — evidência para pitch e relatório.

### Notes:
Mostrar `scorecard.show()` e `gold.select("motorista_hash").show(3)`.

<!-- Slide 35: Hands-On 3 — Análise Gold e Feature Store -->
# Hands-On 3 — Lab 4.3: Análise Gold + Feature Store
- **Arquivo:** `Labs/lab4-analise-gold.py` — queries analíticas + feature store + pós-projeto.
- **O que faz:** 2 queries analíticas (eficiência por CD/região, SLA por cliente) + 1 de qualidade (duplicatas) + 1 feature store (`ml_feature_store` com window 30d) + mock de dashboard (matplotlib/display) + template pós-projeto.
- **Como usar:** rodar após 4.1/4.2; trocar `WHERE` para seu cenário; exportar resultados para pitch.
- **Conexão IA:** cada feature tem origem Gold + transformação documentada — alimenta XGBoost/Random Forest/Prophet sem reprocessar Bronze.

### Notes:
Mostrar `display(ml_feature_store)` e gráfico de SLA.

<!-- Slide 36: Exemplo Fim-a-Fim — Cenário (A) Rotas -->
# Exemplo Fim-a-Fim — (A) Rotas de Entrega
```
IoT 30s (JSON) ──→ Kafka ──→ Bronze Delta `iot_raw` (ano/mes/dia) ──→ Silver `trusted_frota` (dedup, GPS válido, temp 50–150°C) ─┐
TMS CDC (Debezium→Kafka) ──→ Bronze `tms_raw` ──→ Silver `trusted_pedidos` ────────────────────────────────────────────────┤
Maps API 5min + INMET horário ──→ Airflow ──→ Bronze `maps_raw`/`clima_raw` (JSON) ──→ Silver `trusted_rota_clima` ────────┤→ Gold `fato_entregas` (part ano/mes) + `fato_rota_tempo` → SLA por CD, custo/km, feature atraso
ERP batch diário ──→ Bronze `erp_raw` (Parquet) ──→ Silver `dim_cliente/veiculo` ─────────────────────────────────────────┘
IBGE CSV mensal ──→ Bronze `ibge_raw` ──→ Silver `dim_municipio` (enriquecimento CEP) ────────────────────────────────────┘
```
> Latência: streaming (IoT/TMS) em segundos; batch (ERP/IBGE) diário/mensal. ELT: Bronze cru preservado.

### Notes:
Este diagrama é gabarito parcial de (A). Grupos (B/C/D) trocam o centro.

<!-- Slide 37: Exemplo Fim-a-Fim — Cenário (B) Manutenção -->
# Exemplo Fim-a-Fim — (B) Manutenção Preditiva
```
IoT (temp/RPM/vibração/hodômetro a cada 30s) ──→ Bronze `iot_raw` → Silver `trusted_frota` (média móvel 1h, outlier >105°C flag) ─┐
TMS (hodômetro, alocação) + WMS (peças) ──→ Bronze/Silver ──→ `dim_veiculo` (ano, capacidade, hodômetro) ─────────────────┤→ Gold `fato_frota_hora` (1h, por veículo) → `feature_saude_frota` (temp_media_1h, rpm_medio, dias_ultima_manut, vibracao) → score risco 0–100
ERP (custos manutenção) ──→ Silver `fato_manutencao` ───────────────────────────────────────────────────────────────────┘
```
- **Alerta streaming:** `temp_motor >105°C por >2min` → notificar motorista + OS.
- **Feature store:** `ml_feature_store_manutencao` alimenta Random Forest / Isolation Forest.

### Notes:
Focar em janela 1h e score risco. Mostrar Lab 4.3 window.

<!-- Slide 38: Anti-Padrões e 10 Mandamentos -->
# Anti-Padrões — e os 10 Mandamentos do Lake
| Anti-padrão | Consequência | Mandamento |
|---|---|---|
| Bronze sem partição | Scan de TBs por query | 1. Particione `ano/mes/dia` |
| Silver sem schema | Quebra silenciosa downstream | 2. Tipifique Silver (Delta) |
| Reescrever Bronze destrutivo | Perde reprocessamento | 3. Bronze imutável (append + time-travel) |
| Sem dedup | Duplicatas viram multa | 4. Deduplique por chave natural |
| Sem range check | Sensor com 999°C vira feature | 5. Valide ranges (GPS, temp, vel) |
| Sem catálogo | "Onde está a tabela?" | 6. Catalogue tudo |
| PII na Gold | Vazamento LGPD | 7. Anonimize Gold |
| Overwrite sem MERGE | Duplica ao re-rodar | 8. MERGE idempotente |
| Sem monitoramento drift | Modelo degrada calado | 9. Monitore drift |
| Sem lineage | Debug impossível | 10. Documente lineage |

### Notes:
Ler mandamentos. Cada grupo escolhe 1 para defender no Q&A.

<!-- Slide 39: Roadmap — Lakehouse → Data Mesh -->
# Roadmap — Do Lakehouse ao Data Mesh
| Fase | Arquitetura | Gatilho LODLog | Investimento |
|---|---|---|---|
| **Hoje (M4)** | Lakehouse single-workspace (Databricks CE) | 26M IoT/mês, 1 time dados | Baixo — 1 workspace, 1 catálogo |
| **6–12 meses** | Lakehouse + contratos por domínio | 2+ times (frota, estoque) pedem autonomia | Médio — contratos Silver/Gold + steward por domínio |
| **12–24 meses** | Data Mesh federado leve | 12 CDs como domínios, 2000 veículos | Alto — Bronze descentralizado, Gold federada, mesh governance |

> Não federar prematuramente — mesh sem maturidade vira 12 pântanos. Comece lakehouse, evolua com contratos.

### Notes:
Conectar com RPG Aula 2: mesh é Porta 1, mas só com Porta Secreta (contratos) funciona.

<!-- Slide 40: Cronograma de Entregas -->
# Cronograma — O que Entregar e Quando
| Entrega | Data | Formato | Peso |
|---|---|---|---|
| **Pitch em grupo hoje** | 03-out (hoje) | 5 min + diagrama + matriz + análise | 30% (formativa + somativa) |
| **Relatório individual** | 18-out (15 dias) | Até 10 páginas: cenário, 5 Vs, arquitetura, DDL + 3 queries, IA | 70% |
| **Apresentação individual** | A definir | 5 min síntese | 5% do individual |

- **Título individual:** "Planejando o Pipeline de Dados para IA na LODLog".
- **Checklist individual §16 do projeto:** cenário justificado, 3–5 fontes, 5 Vs, DDL 3 tabelas, 2 analíticas + 1 qualidade, conexão IA.

### Notes:
Reforçar prazo 15 dias. Dúvidas sobre formato agora.

<!-- Slide 41: Dicas para o Relatório Individual Nota 10 -->
# Dicas — Relatório Individual Nota 10
1. **Escolha 1 cenário e defenda** — não tente cobrir os 4; profundidade > largura.
2. **Mapeie 3–5 fontes com tabela** — formato, tipo, frequência, Bronze/Silver, como no slide 26.
3. **Faça 5 Vs honestos** — Veracidade é onde a maioria perde ponto (ex: sensor falha 2%, TMS↔WMS diverge 3%).
4. **Desenhe Bronze→Silver→Gold** — particionado, tipado, com ETL/ELT e batch/streaming justificados.
5. **SQL válido e comentado** — DDL com `PARTITIONED BY`, queries com `GROUP BY` + `HAVING`, 1 de qualidade com duplicatas/nulos.
6. **Conecte Gold ao modelo IA** — "feature X vem de Gold Y, transformação Z, alimenta XGBoost para atraso".
7. **Feche com pós-projeto honesto** — 1 vantagem, 1 limitação, 1 lição (banca valoriza autocrítica).

### Notes:
Mostrar exemplo de 5 Vs bem feito vs genérico.

<!-- Slide 42: Referências Essenciais -->
# Referências — Para o Relatório
- **Serra, J. (2024).** *Deciphering Data Architectures: Choosing between a modern data warehouse, data fabric, data lakehouse, and data mesh.* O'Reilly — base para DW/Lake/Lakehouse/Mesh.
- **Inmon, W. H., Linstedt, D., & Levins, M. (2019).** *Data Architecture: A Primer for the Data Scientist.* Elsevier — pântano vs lake, governança.
- **Kleppmann, M. (2017).** *Designing Data-Intensive Applications.* O'Reilly — partição, replicação, streaming, CDC, exactly-once.
- **DAMA-DMBOK (2017).** Data Management Body of Knowledge — 6 dimensões de qualidade, stewardship, ciclo de vida.
- **Projeto LODLog §14–16:** DDL, queries, checklist e rubricas — use como template, não como cópia.

> Bibliografia completa no syllabus. Cite 2–3 no relatório — mostra leitura.

### Notes:
Indicar que Serra e Kleppmann estão na biblioteca FGV.

<!-- Slide 43: Apêndice — Validação GraphRAG Drift -->
# Apêndice — Validação GraphRAG Drift (a validar antes da aula)
| # | Query drift | Intenção |
|---|---|---|
| 1 | "Explique governança de data lake: qualidade, segurança, catálogo, ciclo de vida e por que lakes viram pântanos sem governança." | Cobrir 4 pilares + swamp |
| 2 | "Explique LGPD em pipelines de dados: classificação, anonimização, retenção e direito ao esquecimento. Como aplicar em Bronze Silver Gold?" | Pilar 2 |
| 3 | "Explique feature store e MLOps em lakehouse: como a camada Gold alimenta modelos de IA, com drift e retreinamento." | Feature store |
| 4 | "Explique como integrar dados estruturados e não estruturados em um lakehouse com Medallion Bronze Silver Gold, com exemplo de IoT e ERP." | Integração |

```bash
set -a; source /workspaces/graphrag/hpc-v100/.env; set +a
graphrag query --root /workspaces/graphrag/hpc-v100 --method drift "Explique governança de data lake: qualidade, segurança, catálogo, ciclo de vida e por que lakes viram pântanos sem governança."
graphrag query --root /workspaces/graphrag/hpc-v100 --method drift "Explique LGPD em pipelines de dados: classificação, anonimização, retenção e direito ao esquecimento. Como aplicar em Bronze Silver Gold?"
graphrag query --root /workspaces/graphrag/hpc-v100 --method drift "Explique feature store e MLOps em lakehouse: como a camada Gold alimenta modelos de IA, com drift e retreinamento."
graphrag query --root /workspaces/graphrag/hpc-v100 --method drift "Explique como integrar dados estruturados e não estruturados em um lakehouse com Medallion Bronze Silver Gold, com exemplo de IoT e ERP."
```

> Índice: `hpc-v100`, 399 entities / 41 comunidades, `agnes-2.5-flash`. Rodar sequencial, timeout 300. Salvar saída em `references/validacao-aula4-5-drift.md`.

### Notes:
4 queries drift para validar antes da aula. Salvar evidências.

<!-- Slide 44: Próximos Passos Imediatos -->
# Próximos Passos — Hoje e nos Próximos 15 Dias
**Hoje (03-out):**
- [ ] Cada grupo entrega diagrama + matriz + análise + pitch 5 min (30% da nota).
- [ ] Professor dá feedback formativo por grupo — anotem para o individual.

**Próximos 15 dias (até 18-out):**
- [ ] Escolher 1 dos 4 cenários (pode ser diferente do grupo).
- [ ] Escrever relatório "Planejando o Pipeline de Dados para IA na LODLog" (≤10 páginas, §13.1 do projeto).
- [ ] Validar DDL + 3 queries no Databricks CE (Labs 4.x como base).
- [ ] Submeter via AVA FGV — rubrica §13.3.

> Dúvidas pós-aula: julio.cesar.chaves@fgv.br + fórum AVA. Labs ficam em `/Aulas/Aula-4-5/Labs/`.

### Notes:
Encerramento prático. Abrir para dúvidas.

<!-- Slide 45: Dúvidas -->
# Dúvidas?
## Arquitetura de Dados e Big Data — Módulo 4
### FGV MBA em IA e Analytics | 03-out-2026
**Professor Júlio César Chaves — julio.cesar.chaves@fgv.br**
> "Medir é saber. Governar é confiar. Construir é entregar."

### Notes:
Slide final. Foto da turma com diagramas.

<!-- Slide 46: Backup — DDL Completo para Consulta -->
# Backup — DDL Completo (para consulta)
```sql
-- Gold: fato + dims particionadas (Delta)
CREATE TABLE gold.fato_entregas (
  sk_entrega BIGINT, sk_data INT, sk_cliente INT, sk_veiculo INT, sk_motorista INT, sk_cd_origem INT,
  pedido_id STRING, distancia_km DOUBLE, peso_total_kg DOUBLE, tempo_estimado_min INT, tempo_real_min INT,
  custo_combustivel DOUBLE, multa_atraso DOUBLE, indicador_atraso INT, ano INT, mes INT
) USING DELTA PARTITIONED BY (ano, mes);

CREATE TABLE gold.dim_veiculo (sk_veiculo INT, veiculo_id STRING, placa STRING, tipo STRING, ano_fabricacao INT, capacidade_kg DOUBLE, hodometro_atual INT) USING DELTA;
CREATE TABLE gold.dim_tempo (sk_data INT, data DATE, dia INT, mes INT, ano INT, dia_semana INT, feriado BOOLEAN) USING DELTA;
CREATE TABLE gold.dim_cliente (sk_cliente INT, cliente_id STRING, segmento STRING, regiao STRING) USING DELTA;
CREATE TABLE gold.dim_centro_distribuicao (sk_cd INT, cd_id STRING, regiao STRING, estado STRING, capacidade_m3 DOUBLE) USING DELTA;
```

### Notes:
Backup — não apresentar, só consultar se pedirem SQL.

<!-- Slide 47: Backup — Queries Analíticas -->
# Backup — Queries Analíticas (para consulta)
```sql
-- Eficiência por CD/região (custo/km, SLA)
SELECT dcd.regiao, COUNT(*) total, ROUND(AVG(fe.distancia_km),2) dist_media,
       ROUND(SUM(fe.multa_atraso),2) multas, ROUND(SUM(fe.custo_combustivel)/SUM(fe.distancia_km),2) custo_km
FROM gold.fato_entregas fe JOIN gold.dim_centro_distribuicao dcd ON fe.sk_cd_origem=dcd.sk_cd
GROUP BY dcd.regiao ORDER BY custo_km;

-- Feature store para ML atraso (window 30d)
SELECT fe.sk_entrega, fe.distancia_km, fe.peso_total_kg, dt.dia_semana, dt.feriado,
       COALESCE(hist.atrasos_30d,0) historico_atrasos_30d, fe.indicador_atraso AS target
FROM gold.fato_entregas fe JOIN gold.dim_tempo dt ON fe.sk_data=dt.sk_data
LEFT JOIN (SELECT sk_cliente, SUM(indicador_atraso) atrasos_30d FROM gold.fato_entregas WHERE sk_data BETWEEN 20250601 AND 20250630 GROUP BY sk_cliente) hist
ON fe.sk_cliente=hist.sk_cliente WHERE fe.ano=2025 AND fe.mes=7;
```

### Notes:
Backup — mostrar se tempo sobrar.

<!-- Slide 48: Backup — Scorecard Template -->
# Backup — Scorecard DAMA Template (para consulta)
| Fonte | Completude | Acurácia | Consistência | Atualidade | Unicidade | Validade | Score |
|---|---|---|---|---|---|---|---|
| IoT | 98,2% | 99,1% | — | 2,1 min | 99,9% | 99,4% | 92 🟢 |
| ERP | 99,5% | 98,8% | 97,3% | 4h | 99,8% | 99,7% | 94 🟢 |
| WMS | 97,8% | 99,0% | 97,3% | 8 min | 99,7% | 98,9% | 89 🟡 |

> Fórmula: score = média ponderada (pesos iguais por default; ajuste por criticidade). Lab 4.2 automatiza.

### Notes:
Backup — entregar como handout.

