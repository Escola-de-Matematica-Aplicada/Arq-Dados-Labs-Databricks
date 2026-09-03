# Arquitetura de Dados e Big Data
Aula 3 — 29 de setembro de 2026
Módulo 3 — Organização e Manuseio de Dados em Bases Distribuídas

### Notes:
Turma MBA em Inteligência Artificial e Analytics Aplicados a Negócios
Professor: Júlio César Chaves — julio.cesar.chaves@fgv.br
Horário: 19h00 às 22h20 (intervalo 15min: 20h40–20h55) — Teoria 1h40 | Prática 1h40

<!-- Slide 1: Capa -->
# Arquitetura de Dados e Big Data
## Aula 3 — Módulo 3: Organização e Manuseio de Dados em Bases Distribuídas
### 29 de setembro de 2026 | 19h00–22h20 | FGV MBA em IA e Analytics
**Cloud (IaaS/PaaS/SaaS) · Hadoop e Ecossistema · Spark/Hive · Pipelines · ETL vs ELT · Lambda e Kappa**
**Arquitetura em Camadas: Ingestão → Processamento → Consumo**
> Validado via GraphRAG drift — root `/workspaces/graphrag/hpc-v100` — modelo `agnes-2.5-flash` — a validar 4 queries drift

### Notes:
Capa. Recapitular Aulas 1–2 e posicionar Módulo 3 como "como mover e transformar" antes do Módulo 4 "construir".

<!-- Slide 2: Regra de ouro -->
# Regra da Aula: Metade Teoria, Metade Prática
| Bloco | Horário | Duração | Conteúdo |
|---|---|---|---|
| **Teoria** | 19h00–20h40 | 1h40 | Cloud, Hadoop/Spark/Hive, ETL vs ELT, Lambda/Kappa, camadas |
| **Intervalo** | 20h40–20h55 | 15min | — |
| **Prática** | 20h55–22h20 | 1h40 (70min pipelines + 30min síntese/apresentação) | Desenho de pipelines LODLog + Labs Databricks |

> Cada aula atende obrigatoriamente à regra de 50% teoria / 50% prática (syllabus § Hard rules).

### Notes:
Reforçar relógio visível. Prática tem entrega parcial (pipeline desenhado).

<!-- Slide 3: Cronograma revisitado -->
# Onde estamos no syllabus
| Aula | Data | Módulo | Foco |
|---|---|---|---|
| 1 | 22-set | M1 — Tipos de dados e Big Data | Visto: OLTP vs OLAP, 5 Vs, 8 fontes LODLog |
| 2 | 28-set | M2 — Ferramentas distribuídas | Visto: NoSQL, DW/Lake/Lakehouse/Mesh, Medallion/Zaloni |
| **3** | **29-set** | **M3 — Organização e manuseio** | **Hoje: cloud, Hadoop/Spark, pipelines, ETL/ELT, Lambda/Kappa** |
| 4 e 5 | 03-out | M4 — Miniprojeto Lakehouse | Governança + construção e avaliação do data lake LODLog |

> Aula 3 conecta o "onde guardar" (Aula 2) ao "como mover e transformar" (pipelines), antes do "construir de ponta a ponta" (M4).

### Notes:
Narrativa: M1=quê, M2=onde, M3=como move, M4=construir.

<!-- Slide 4: Objetivos de aprendizagem Módulo 3 -->
# Objetivos de Aprendizagem — Módulo 3
Ao final da aula o estudante será capaz de:
1. **Descrever** as principais ferramentas por camada (ingestão, armazenamento, processamento, consumo).
2. **Compreender** a lógica de arquiteturas distribuídas (scale-out, CAP, particionamento).
3. **Identificar** ferramentas adequadas por cenário (Hadoop vs Spark vs Hive vs Kafka/Flink).
4. **Distinguir** IaaS / PaaS / SaaS e posicionar ofertas AWS/Azure/GCP por camada.
5. **Decidir** entre ETL vs ELT e batch vs streaming (Lambda/Kappa/híbrido) para cada fonte LODLog.
6. **Desenhar** um pipeline conceitual ingestão → processamento → consumo para as 8 fontes LODLog.

Fonte: syllabus Módulo 3 — validado via drift.

### Notes:
Ler objetivos em voz alta. 2 min.

<!-- Slide 5: Recapitulação Aulas 1–2 -->
# Recapitulação Relâmpago — Aulas 1 e 2
- **Aula 1:** OLTP (3FN, ACID) vs OLAP (star) · Tipos (estruturado/semi/não) · 5 Vs (Volume 864k IoT/dia, Velocity 30s, Variety 3 tipos, Veracidade 4 camadas, Valor R$4.2M multas) · 8 fontes LODLog.
- **Aula 2:** NoSQL polyglot (Redis KV, Mongo Doc, Cassandra Coluna, Neo4j Grafo) · DW vs Lake vs Lakehouse vs Mesh vs Fabric · Medallion Bronze/Silver/Gold ↔ Zaloni 5 zonas · RPG "Cinco Torres" → porta secreta = contratos + governança federada leve.
- **Pergunta de ponte:** "Já sabemos *o quê* (dados) e *onde* (arquiteturas). Agora: *como* os dados saem da origem e chegam confiáveis ao consumo, em escala, sem virar pântano?"

### Notes:
5 min de recapitulação ativa.

<!-- Slide 6: Agenda detalhada -->
# Agenda da Noite
**Teoria (19h00–20h40):**
1. Arquitetura em 3 camadas: ingestão → processamento → consumo (5 min)
2. Cloud: IaaS/PaaS/SaaS + responsabilidade compartilhada + comparativo AWS/Azure/GCP (20 min)
3. Hadoop e ecossistema: HDFS/YARN/MapReduce + Hive/Pig/HBase + limites (15 min)
4. Spark (e por que superou MapReduce) + Hive vs Spark SQL + Kafka/Flink/Airflow/dbt (20 min)
5. Formatos de armazenamento: CSV/JSON/Avro/Parquet/ORC/Delta (10 min)
6. ETL vs ELT + Batch vs Streaming + Lambda vs Kappa vs híbrido (20 min)
7. Pipeline fim-a-fim LODLog amarrando tudo (10 min)

**Prática (20h55–22h20):**
8. Lab 3: desenhar pipelines por fonte + escolher ferramentas por camada + Labs Databricks

### Notes:
Exibir cronômetro.

<!-- Slide 7: Seção Teoria -->
# PARTE 1 — TEORIA (1h40)
## Do armazenamento ao movimento

### Notes:
Divisor de seção.

<!-- Slide 8: Arquitetura em camadas — visão -->
# Arquitetura em Camadas: Ingestão → Processamento → Consumo
- **Ingestão:** trazer dados para dentro (batch, streaming, CDC, API pull/push, file drop). Decisão por Velocidade e Veracidade.
- **Armazenamento/Processamento:** limpar, padronizar, enriquecer, agregar (Bronze→Silver→Gold). Decisão por Variedade e Volume.
- **Consumo:** servir BI, ML, APIs, alertas. Decisão por Valor (latência e formato certos).
- **Orquestração transversal:** DAGs (Airflow), retry, linhagem, monitoramento — sem ela, pipeline é coleção de scripts frágeis.
- **Analogia restaurante:** ingestão = recebimento de ingredientes · armazenamento = despensa/câmara fria · processamento = cozinha (receitas/ETL) · consumo = salão (cardápio/BI) · orquestração = chef expedidor.

> Medallion (Aula 2) é a instanciação mais comum dessas camadas no Lakehouse.

### Notes:
Desenhar no quadro as 3 camadas + orquestração lateral.

<!-- Slide 9: Por que camadas? -->
# Por que separar em camadas?
| Sem camadas (acoplado) | Com camadas (desacoplado) |
|---|---|
| Reprocessar = reextrair da origem (cara, lento) | Reprocessar = reler Bronze barata (Parquet/Delta) |
| Erro em 1 fonte quebra tudo | Falha isolada por camada; retry por stage |
| Sem linhagem; debug é caça ao tesouro | Linhagem Bronze→Silver→Gold rastreável |
| Schema-on-read em todo lugar = caos | Bronze schema-on-read, Silver/Gold schema-on-write tipado |

> Princípio: "store raw first, curate later" — Bronze nunca é reescrito destrutivamente.

### Notes:
Conectar com 4 camadas de Veracidade da Aula 1.

<!-- Slide 10: Cloud — IaaS/PaaS/SaaS -->
# Cloud Computing: IaaS / PaaS / SaaS
| Modelo | Você gerencia | Provedor gerencia | Analogia | Exemplo LODLog |
|---|---|---|---|---|
| **IaaS** | App, runtime, dados | Hardware, rede, hipervisor | Alugar terreno + construir | EC2/VMs para Hadoop on-prem na nuvem |
| **PaaS** | App + dados | Runtime, SO, escala, patch | Apartamento mobiliado | Databricks, EMR, Dataproc, Synapse Spark |
| **SaaS** | Só os dados/parâmetros | Tudo (infra + app) | Hotel | Snowflake, BigQuery, Power BI, Fivetran |

> Tendência: IaaS → PaaS → SaaS conforme maturidade; pagar por uso vs pagar por ociosidade.

### Notes:
Pizza-as-a-Service é alternativa lúdica se sobrar tempo.

<!-- Slide 11: Responsabilidade compartilhada -->
# Responsabilidade Compartilhada na Nuvem
- **On-prem:** você cuida de tudo (energia, rack, SO, patch, backup).
- **IaaS:** provedor cuida do data center; você ainda patch de SO, rede, IAM.
- **PaaS:** provedor cuida de SO/escala/patch; você cuida de dados, lógica, acesso.
- **SaaS:** provedor cuida de quase tudo; você cuida de classificação, LGPD, quem vê o quê.
- **Pegadinha:** "está na nuvem, está seguro" é falso — vazamentos vêm de bucket público, chave exposta e falta de criptografia, não do data center.
- **LODLog:** motoristas (LGPD) e contratos (sigilo) exigem criptografia em repouso + em trânsito + controle de acesso por camada (Bronze restrito).

### Notes:
Mostrar diagrama clássico de responsabilidade.

<!-- Slide 12: Comparativo AWS / Azure / GCP por camada -->
# AWS vs Azure vs GCP — por camada do pipeline
| Camada | AWS | Azure | GCP | Hadoop/Spark local |
|---|---|---|---|---|
| **Ingestão batch** | S3 + DMS / Transfer | Data Factory + ADLS | Cloud Storage + Transfer | HDFS + Sqoop/Flume |
| **Ingestão streaming** | Kinesis / MSK (Kafka) | Event Hubs | Pub/Sub + Dataflow | Kafka |
| **Armazenamento** | S3 (Delta/Parquet) | ADLS Gen2 | GCS | HDFS |
| **Processamento batch** | EMR (Spark), Glue (ETL) | Synapse Spark, HDInsight | Dataproc, Dataflow | Spark on YARN |
| **Processamento streaming** | Kinesis Analytics, MSK | Stream Analytics | Dataflow (Flink/Beam) | Spark Structured Streaming, Flink |
| **Warehouse/Serving** | Redshift, Athena | Synapse DW, Fabric | BigQuery | Hive / Presto |
| **Orquestração** | Step Functions, MWAA (Airflow) | Data Factory | Composer (Airflow), Workflows | Airflow, Oozie |
| **Governança** | Glue Catalog, Lake Formation | Purview | Data Catalog | Hive Metastore, Atlas |

> Databricks (multi-cloud) abstrai AWS/Azure/GCP — por isso é o PaaS do Lab.

### Notes:
Não precisa decorar serviços; entender a correspondência por camada.

<!-- Slide 13: Custos e armadilhas da nuvem -->
# Custos e Armadilhas da Nuvem
- **Egress (saída de dados):** barata para entrar, cara para sair — desenhar pipelines minimizando cross-region/cross-cloud.
- **Storage barato, computação cara:** guardar Bronze em S3/GCS é centavos; deixar cluster Spark ligado 24×7 sem auto-terminate é que dói.
- **Lock-in sutil:** Glue Catalog, BigQuery ML, Synapse pipelines prendem mais que VM; preferir formatos abertos (Parquet, Delta, Iceberg) + Airflow/dbt portáveis.
- **LODLog:** 864k eventos IoT/dia × 30 dias ≈ 26M linhas/mês — particionar por `ano/mes/dia` reduz scan e custo em 10–100×.
- **FinOps:** tags por domínio (frota/operação/estoque), budgets e alertas; desligar dev fora do horário.

### Notes:
Mostrar conta rápida: S3 Standard 1TB ≈ US$23/mês vs EMR 10 nós ≈ US$2/h.

<!-- Slide 14: Hadoop — história e porquê -->
# Hadoop — História e Porquê
- **2003:** Google publica GFS (arquivo distribuído) e MapReduce — inspira Doug Cutting & Mike Cafarella (Nutch).
- **2006:** Hadoop nasce (HDFS + MapReduce) no Yahoo! — processar web crawl em commodity hardware.
- **Ideia central:** "leve a computação até o dado" — dividir arquivo em blocos (128MB), replicar 3×, processar onde o bloco está.
- **HDFS:** NameNode (metadados) + DataNodes (blocos) — alta vazão, falha é normal (replica).
- **YARN (2012):** separa gerência de recursos do MapReduce — permite Spark, Hive, Flink no mesmo cluster.
- **MapReduce:** `map()` → shuffle → `reduce()` — simples, mas escreve em disco a cada etapa (lento para iterativo/ML).

### Notes:
Linha do tempo: GFS 2003 → Hadoop 2006 → YARN 2012 → Spark 2014 supera MR.

<!-- Slide 15: Ecossistema Hadoop -->
# Ecossistema Hadoop (além do HDFS + MapReduce)
| Ferramenta | Papel | Analogia LODLog |
|---|---|---|
| **Hive** | SQL sobre HDFS (HiveQL → MapReduce/Tez/Spark) | Analista consulta `trusted_frota` sem escrever MR |
| **Pig** | Linguagem procedural sobre MR | Obsoleto — substituído por Spark |
| **HBase** | NoSQL coluna sobre HDFS (random read/write) | Série temporal IoT com acesso por chave (alternativa a Cassandra) |
| **Sqoop** | Importa/exporta RDBMS ↔ HDFS em batch | ERP/WMS/TMS → Bronze (hoje: CDC/Kafka) |
| **Flume** | Coleta streaming de logs | Logs de telemetria → HDFS (hoje: Kafka) |
| **Oozie** | Orquestrador de workflows Hadoop | Antecessor do Airflow |

> Muitas ferramentas foram substituídas (Sqoop→Debezium, Flume→Kafka, Pig→Spark, Oozie→Airflow) — mas o padrão arquitetural permanece.

### Notes:
Mostrar stack: HDFS na base, YARN no meio, Hive/Spark/HBase no topo.

<!-- Slide 16: Limites do Hadoop clássico -->
# Limites do Hadoop Clássico — por que Spark venceu
- **MapReduce escreve em disco a cada etapa:** iterativo (ML, graph) fica 10–100× mais lento que em memória.
- **Latência de minutos/horas:** não serve para streaming sub-segundo (alertas de temperatura motor).
- **NameNode é SPOF** (em HA melhora, mas continua gargalo de metadados em escala extrema).
- **Small files problem:** milhões de JSONs pequenos matam o NameNode — compactar em Parquet resolve.
- **Operação pesada:** cluster Hadoop on-prem exige time dedicado; cloud PaaS (EMR/Dataproc) reduz dor.
- **Transição LODLog:** começar em PaaS Spark (Databricks) é mais barato que montar Hadoop do zero para 26M linhas/mês.

### Notes:
Gráfico: MR vs Spark — 100× em benchmark WordCount iterativo (Berkeley 2014).

<!-- Slide 17: Apache Spark -->
# Apache Spark — Motor Unificado
- **Nascimento:** 2009 UC Berkeley AMPLab (Matei Zaharia), 2014 supera MapReduce em sort benchmark.
- **Core:** **RDD** (resilient distributed dataset) em memória + linhagem para recomputação — tolerância sem replicação custosa.
- **DataFrame/Dataset + Catalyst Optimizer:** API declarativa (SQL-like) com otimização de plano (predicate pushdown, column pruning).
- **Bibliotecas acopladas:** Spark SQL, Structured Streaming, MLlib, GraphX — um motor para batch + streaming + ML.
- **Execução:** driver (plano) → executors (tarefas) → shuffle só quando necessário; cache em memória para iterativo.
- **LODLog:** `spark.read.json("bronze/iot/ano=2025/mes=07/dia=14/*.json")` → `filter(temperatura > 105)` → `write.format("delta").partitionBy("data")`

### Notes:
Demo mental: Catalyst reordena filter antes de join automaticamente.

<!-- Slide 18: Spark vs MapReduce e Hive vs Spark SQL -->
# Spark vs MapReduce · Hive vs Spark SQL
| Comparativo | Detalhe |
|---|---|
| **MR vs Spark** | MR: disco a cada etapa; Spark: memória + linhagem → 10–100× em iterativo |
| **Hive (MR/Tez)** | SQL → MapReduce; estável, mas lento; ainda usado como metastore/catalog |
| **Hive on Spark** | HiveQL rodando sobre Spark — ponte de migração |
| **Spark SQL** | DataFrame + Catalyst + Tungsten (off-heap) — padrão atual no Lakehouse |
| **Escolha prática** | Novo projeto → Spark SQL direto; legado Hive → migrar gradualmente, manter Metastore |

> No Databricks CE, você já usa Spark SQL sem perceber: `%sql` roda sobre Spark.

### Notes:
Hive Metastore ainda é o catálogo mais comum (mesmo com Spark).

<!-- Slide 19: Outras ferramentas Apache e modernas -->
# Outras Ferramentas: Kafka, Flink, Airflow, dbt, NiFi
| Ferramenta | Camada | Quando usar | LODLog |
|---|---|---|---|
| **Kafka** | Ingestão streaming (log distribuído) | 100k+ eventos/s, replay, desacoplamento | IoT 30s, Maps 5min, CDC TMS |
| **Flink** | Streaming com estado (stateful) | Janelas, exactly-once, baixa latência | Janela 5min de temperatura motor >105C |
| **Airflow** | Orquestração (DAGs) | Dependências, retry, SLA, sensores | Bronze→Silver→Gold diário + hourly IoT |
| **dbt** | Transformação ELT (SQL) | Versionar transforms no warehouse/lakehouse | Silver→Gold como `select` versionado |
| **NiFi** | Ingestão visual / data flow | Prototipar ingestão sem código | Carga inicial IBGE CSV mensal |
| **Debezium** | CDC (change data capture) | Capturar binlog sem batch | TMS tempo real sem polling |

> Kafka + Flink/Spark Streaming + Airflow + dbt é o quarteto mais comum em produção hoje.

### Notes:
Mostrar pipeline: Debezium → Kafka → Spark Streaming → Delta → dbt → Gold.

<!-- Slide 20: Formatos de armazenamento -->
# Formatos de Armazenamento: do cru ao analítico
| Formato | Tipo | Schema | Compressão | Quando usar |
|---|---|---|---|---|
| **CSV** | Texto, linha | Schema-on-read, frágil | Baixa | IBGE mensal, legado ERP (evitar se possível) |
| **JSON** | Texto, linha | Schema-on-read flexível | Baixa | Bronze IoT/API cru; humano-legível |
| **Avro** | Binário, linha | Schema-on-write com evolução | Média | Kafka/Silver com schema registry |
| **Parquet** | Binário, coluna | Schema-on-write tipado | Alta (snappy/zstd) | Silver/Gold analítico — padrão Lakehouse |
| **ORC** | Binário, coluna | Schema-on-write | Alta | Hive/ORC legado (similar a Parquet) |
| **Delta / Iceberg / Hudi** | Parquet + log transacional | ACID, time-travel, upsert | Alta | Lakehouse: ACID sobre object storage |

> Regra: Bronze = JSON/CSV cru (fidelidade) → Silver/Gold = Parquet/Delta (performance + ACID).

### Notes:
Parquet colunar = ler 1 coluna de 50 = 50× menos I/O que CSV.

<!-- Slide 21: Ingestão — padrões -->
# Ingestão: Padrões e Escolha
| Padrão | Latência | Como funciona | Prós | Contras |
|---|---|---|---|---|
| **Batch (file/ETL)** | Horas/dias | Job lê tabela/arquivo inteiro periodicamente | Simples, barato | Atraso; reprocessa tudo |
| **Micro-batch** | Minutos | Batch pequeno frequente (Spark 1–5 min) | Quase streaming com simplicidade batch | Latência não é sub-segundo |
| **Streaming (Kafka)** | Segundos | Produtor → log → consumidor contínuo | Tempo real, replay | Complexo (ordem, exactly-once) |
| **CDC (Debezium)** | Segundos | Lê binlog/WAL do RDBMS sem `SELECT *` | Sem impacto no OLTP; tempo real | Setup, schema evolution |
| **API pull/push** | Variável | Polling ou webhook | Integra SaaS externo | Rate limit, paginação, idempotência |

> LODLog usa os 5 padrões — não há um único.

### Notes:
Desenhar espectro batch → micro-batch → streaming.

<!-- Slide 22: Ingestão LODLog por fonte -->
# Ingestão LODLog — 8 fontes, 5 padrões
| Fonte | Formato | Frequência | Padrão recomendado | Ferramenta |
|---|---|---|---|---|
| **IoT sensores** | JSON | 30s streaming | Streaming (Kafka → Spark Streaming) | Kafka + Structured Streaming → Bronze Delta |
| **ERP** | SQL relacional | Batch diário | Batch (ou CDC se tempo real) | Sqoop/Glue/Debezium → Bronze Parquet |
| **WMS** | SQL | 15 min | Micro-batch / CDC | Debezium/Kafka ou Airflow 15min |
| **TMS** | SQL | Tempo real | CDC | Debezium → Kafka → Silver em segundos |
| **Google Maps API** | JSON | 5 min (veículos em rota) | API pull streaming | NiFi/Airflow + `requests` → Bronze JSON |
| **INMET API** | JSON | Horário | API pull batch | Airflow hourly → Bronze JSON |
| **ANTT API** | JSON/XML | Event-driven | Webhook/poll event | Kafka/event bridge → Bronze |
| **IBGE** | CSV | Mensal | File batch | Airflow monthly + `spark.read.csv` |

> Mapear cada fonte ao padrão correto é metade do Lab 3.

### Notes:
Entregar tabela impressa/QR para o Lab.

<!-- Slide 23: ETL vs ELT -->
# ETL vs ELT — Onde transformar?
- **ETL (tradicional, on-prem):** **Extract → Transform → Load** — transforma antes de carregar no DW (staging on-prem, caro escalar).
  - Prós: DW limpo, governança pré-carga. Contras: perde dado cru; não escala para semi/não estruturado; ETL server é gargalo.
- **ELT (moderno, cloud/lakehouse):** **Extract → Load → Transform** — carrega cru no Lake (Bronze) e transforma dentro do Lakehouse (Spark/dbt).
  - Prós: preserva Bronze para reprocessamento; escala elástica; suporta JSON/variação; dbt versiona transforms como SQL.
  - Contras: exige disciplina (Bronze→Silver→Gold) senão vira pântano; custo de computação se sem particionamento.
- **LODLog:** Bronze IoT JSON cru (ELT) → Silver Parquet tipado + Gold agregada; ERP batch pode ser ETL leve se volume pequeno, mas ELT é padrão Lakehouse.

### Notes:
Diagrama: ETL funil estreito vs ELT lago largo.

<!-- Slide 24: ETL vs ELT — decisão -->
# ETL vs ELT — Matriz de Decisão
| Critério | Prefira ETL | Prefira ELT |
|---|---|---|
| Volume | Pequeno, estável | Grande, crescente (IoT 26M/mês) |
| Variedade | Só estruturado tipado | Semi/não estruturado (JSON IoT, APIs) |
| Latência | Batch diário tolerável | Streaming/micro-batch |
| Reprocessamento | Raro | Frequente (novas regras Silver) |
| Time | ETL developers + DW time | Analytics engineers (SQL/dbt) + Spark |
| Custo | Licença ETL + DW fixo | Storage barato + compute sob demanda |
| Governança | Pré-carga rígida | Bronze cru + contratos Silver/Gold |

> No Módulo 4 (miniprojeto), o ELT Lakehouse será a arquitetura avaliada — por isso o Lab 3 já pratica ELT no Databricks.

### Notes:
Conectar com Aula 2: Medallion é ELT por definição.

<!-- Slide 25: Batch vs Streaming -->
# Batch vs Streaming — Comparativo Direto
| Característica | Batch | Streaming |
|---|---|---|
| **Latência** | Minutos a dias | Milissegundos a segundos |
| **Custo** | Menor (cluster efêmero) | Maior (sempre ligado) |
| **Complexidade** | Baixa (retry simples) | Alta (ordem, late data, exactly-once) |
| **Exemplo LODLog** | Fechamento financeiro diário; ranking semanal CDs | Alerta motor >105C por 2min; atraso crítico >60min |
| **Tecnologia** | Spark SQL, dbt, Airflow diário | Kafka + Spark Streaming / Flink |
| **Quando escolher** | Analytics, retreinamento ML | Alertas operacionais, SLA 실시간 |

> Recomendação LODLog: **híbrido** — streaming para alertas, batch para analytics/ML. Nem tudo precisa ser real-time.

### Notes:
Perguntar: "quais fontes da LODLog precisam de streaming e quais toleram batch?"

<!-- Slide 26: Arquitetura Lambda -->
# Arquitetura Lambda — Batch + Speed + Serving
- **Batch layer:** reprocessa todo o histórico (preciso, lento) — Hadoop/Spark batch → batch views.
- **Speed layer:** processa só o recente em streaming (rápido, aproximado) — Storm/Flink/Spark Streaming → real-time views.
- **Serving layer:** une batch + speed para consulta (merge).
- **Prós:** tolera reprocessamento completo; baixa latência para o recente.
- **Contras:** **duplicação de código** (lógica batch em MR/Spark batch + lógica streaming em Storm/Flink) — bug em um ≠ outro; operar 2 pipelines.
- **LODLog Lambda:** batch diário recalcula `fato_entregas` histórico; speed layer alerta temperatura em segundos; serving junta para dashboard.

### Notes:
Desenhar Lambda: fontes → batch & speed → serving → consulta.

<!-- Slide 27: Arquitetura Kappa -->
# Arquitetura Kappa — Só Streaming (log único)
- **Ideia (Jay Kreps, LinkedIn, 2014):** se o log (Kafka) retém histórico suficiente, **um único pipeline streaming** serve para tudo — reprocessar é replay do log.
- **Componentes:** Kafka (log durável) → Spark Structured Streaming / Flink (único código) → Delta/Iceberg (tabela) → consumo.
- **Prós:** código único; sem divergência batch/streaming; mais simples de operar.
- **Contras:** replay de meses de log pode ser caro/lento; nem todo workload precisa de streaming (batch puro é mais barato); requer retenção longa no Kafka.
- **LODLog Kappa:** IoT 30s + TMS CDC já são log; replay de 7 dias para corrigir regra Silver sem job batch separado.

### Notes:
Kappa não é "Lambda sem batch" — é filosofia de log único.

<!-- Slide 28: Lambda vs Kappa vs Híbrido -->
# Lambda vs Kappa — Como escolher?
| Critério | Lambda | Kappa | Híbrido (recomendado LODLog) |
|---|---|---|---|
| Código | Duplicado (batch + streaming) | Único (streaming) | Único streaming para crítico; batch para resto |
| Reprocessamento | Batch reprocessa tudo | Replay do log | Replay curto (Kappa) + batch diário barato |
| Custo | Alto (2 pipelines) | Médio (log retido) | Otimizado por workload |
| Complexidade operacional | Alta | Média | Baixa (time foca onde importa) |
| Exemplo | Histórico financeiro + alerta IoT | Plataforma 100% streaming | **LODLog: IoT/TMS em Kappa; ERP/WMS/IBGE em batch** |

> Para a LODLog (26M IoT/mês + ERP diário), híbrido vence: não pague streaming onde batch resolve.

### Notes:
Matriz para o Lab: grupos escolhem Lambda/Kappa/híbrido por domínio.

<!-- Slide 29: Orquestração — Airflow e DAGs -->
# Orquestração: Airflow e DAGs
- **Por que orquestrar:** dependências (`Silver só após Bronze`), retry, SLA, backfill, sensores, linhagem.
- **Airflow:** DAG = grafo acíclico de tasks; scheduler + workers + metastore; operadores (PythonOperator, SparkSubmit, HttpSensor).
- **Padrão LODLog:**
  - `dag_erp_diario`: `extract_erp >> bronze_erp >> silver_erp >> gold_fato >> dbt_gold` (diário 02h, retry 2×).
  - `dag_iot_streaming`: Structured Streaming contínuo + checkpoint em Delta (sem DAG, job sempre ligado).
  - `dag_apis_hourly`: `fetch_inmet >> bronze_clima >> silver_clima`.
- **Alternativas:** Oozie (legado Hadoop), Step Functions, Data Factory, Prefect, Dagster.
- **Dica:** idempotência (re-rodar não duplica) + `partitionBy("data")` + Delta `MERGE` são obrigatórios.

### Notes:
Mostrar DAG simples no quadro.

<!-- Slide 30: Pipeline fim-a-fim LODLog -->
# Pipeline Fim-a-Fim LODLog — Amarrando Tudo
```
IoT 30s ──→ Kafka ──→ Spark Structured Streaming ──→ Bronze Delta (JSON→Parquet) ──→ Silver (trusted_frota, deduplicada, range-validada) ──→ Gold (fato_frota_hora, feature_temperatura_media) ──→ Alerta >105C / ML manutenção
ERP diário ──→ Airflow batch ──→ Bronze Parquet ──→ Silver (dim_cliente, dim_produto) ──→ Gold (fato_entregas) ──→ Dashboard SLA / BI
TMS real-time ──→ Debezium CDC ──→ Kafka ──→ Silver/Gold em segundos ──→ Rota otimizada
Maps 5min / INMET horário / ANTT evento / IBGE mensal ──→ Airflow/NiFi ──→ Bronze JSON/CSV ──→ Silver enriquecida (CEP→IBGE) ──→ Gold
                                    ↓
                            Orquestração: Airflow + Delta time-travel + linhagem
                            Formatos: Bronze JSON/CSV cru · Silver/Gold Parquet/Delta (ACID, particionado)
                            ELT: load cru primeiro, transform depois (dbt/Spark SQL)
```

### Notes:
Este diagrama é a cola do Lab 3.

<!-- Slide 31: Intervalo -->
# Intervalo — 15 min
## 20h40 – 20h55
> Na volta: Lab 3 — cada grupo desenha o pipeline de um domínio LODLog e justifica ETL/ELT + batch/streaming/Lambda/Kappa.

### Notes:
Pausa.

<!-- Slide 32: Seção Prática -->
# PARTE 2 — PRÁTICA (1h40)
## Desenhando pipelines — da ingestão ao consumo

### Notes:
Divisor de seção.

<!-- Slide 33: Lab 3 — briefing -->
# Lab 3 — Briefing (Módulo 3)
**Objetivo:** desenhar o pipeline conceitual **ingestão → processamento → consumo** para as 8 fontes LODLog, justificando cada escolha.

**Entregáveis por grupo (1 por domínio):**
1. Diagrama do pipeline (ingestão, armazenamento, processamento, consumo, orquestração).
2. Tabela por fonte: padrão (batch/micro-batch/streaming/CDC/API), ETL vs ELT, ferramenta por camada, formato.
3. Decisão Lambda vs Kappa vs híbrido + justificativa de custo/latência.
4. Posicionamento cloud: AWS/Azure/GCP **ou** Hadoop local — por quê?

**Domínios sorteados:** Frota/IoT · Operação/TMS · Estoque/WMS · Financeiro/ERP · Externo (Maps/Clima/ANTT/IBGE)

**Tempo:** 70 min desenho + 30 min apresentação relâmpago (5 min/grupo) + síntese do professor.

### Notes:
Formar 5 grupos.

<!-- Slide 34: Exercício guiado -->
# Lab 3 — Passo a Passo (70 min)
1. **Mapear fontes do seu domínio** (10 min) — liste formatos, frequências e Volumes (ex: IoT 864k/dia).
2. **Escolher padrão de ingestão por fonte** (15 min) — batch/CDC/streaming/API. Use tabela do slide 22.
3. **Escolher ETL vs ELT** (10 min) — ELT se semi/não estruturado ou reprocessamento frequente.
4. **Escolher Lambda/Kappa/híbrido** (10 min) — streaming só onde latência < minutos justifica custo.
5. **Preencher matriz ferramenta×camada** (15 min) — AWS/Azure/GCP ou Hadoop; Kafka/Flink/Spark/Hive/dbt/Airflow.
6. **Desenhar diagrama + preparar pitch 5 min** (10 min) — ingestão→Bronze→Silver→Gold→consumo + orquestração.

> Template e gabarito parcial nos Labs: `lab3-lambda-kappa-exercicio.py` e `lab3-pipeline-ingestao.py`.

### Notes:
Circular entre grupos.

<!-- Slide 35: Matriz de decisão para o Lab -->
# Lab 3 — Matriz de Decisão (entregar preenchida)
| Fonte do seu domínio | Padrão ingestão | ETL ou ELT | Batch/Streaming | Ferramenta ingestão | Formato Bronze | Ferramenta processamento | Formato Silver/Gold | Latência alvo | Lambda/Kappa/Híbrido |
|---|---|---|---|---|---|---|---|---|---|
| (ex: IoT) | Streaming Kafka | ELT | Streaming | Kafka + Spark Streaming | JSON → Delta | Spark + Delta MERGE | Parquet/Delta particionado | Segundos | Kappa |
| (ex: ERP) | Batch diário | ELT | Batch | Airflow + JDBC | Parquet | Spark SQL + dbt | Parquet/Delta | Horas | Batch puro |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

> Critério de avaliação: coerência (padrão ↔ latência ↔ ferramenta), custo e reprocessamento.

### Notes:
Imprimir/QR.

<!-- Slide 36: Template pipeline por camada -->
# Lab 3 — Template: Ferramenta por Camada
| Camada | Pergunta | Opções |
|---|---|---|
| **Ingestão** | Qual padrão? Qual ferramenta? | Kafka / Debezium CDC / Airflow batch / NiFi / API pull |
| **Armazenamento Bronze** | Formato cru? Particionamento? | JSON/CSV em S3/ADLS/GCS/HDFS, `ano/mes/dia` |
| **Processamento Silver** | ETL ou ELT? Engine? | Spark Structured Streaming / Spark SQL / Flink / dbt |
| **Armazenamento Gold** | Formato analítico? ACID? | Parquet/Delta/Iceberg, `MERGE`, time-travel |
| **Consumo** | Quem consome? Latência? | BI (Power BI), ML feature store, API, alerta |
| **Orquestração** | DAG ou contínuo? | Airflow DAG (batch) vs job streaming contínuo |

> Dica: comece pela latência de consumo e volte para trás.

### Notes:
Preencher de trás para frente ajuda.

<!-- Slide 37: Apresentação e discussão -->
# Lab 3 — Apresentação Relâmpago + Discussão (30 min)
- **5 min por grupo:** pitch do pipeline + 2 perguntas da turma.
- **Perguntas-guia do professor:**
  - Onde está o gargalo de Veracidade? (ex: sensor falha → validação de range em Silver)
  - Onde o egress/lock-in dói? (ex: Maps API 60k req/dia → cache Redis antes do Lake)
  - O que reprocessar se a regra Silver mudar? (ex: Bronze Delta permite replay sem re-extrair)
  - Quando o streaming não vale o custo? (ex: IBGE mensal → batch puro)
- **Síntese:** não existe pipeline único — híbrido por domínio, formatos abertos e Bronze imutável são invariantes.

### Notes:
Fechar com ponte para M4: "no miniprojeto vocês vão construir um desses pipelines de verdade".

<!-- Slide 38: Resumo da aula -->
# Resumo — O que levamos da Aula 3
- **3 camadas** (ingestão → processamento → consumo) + orquestração são o esqueleto de qualquer pipeline — Medallion é sua instância Lakehouse.
- **Cloud:** IaaS vs PaaS vs SaaS + responsabilidade compartilhada; AWS/Azure/GCP têm correspondentes por camada — prefira PaaS (Databricks/EMR) e formatos abertos.
- **Hadoop** trouxe HDFS/YARN/MR e o ecossistema (Hive/HBase/Sqoop) mas MR em disco perdeu para **Spark** em memória (10–100× em iterativo).
- **Formatos:** Bronze cru (JSON/CSV) → Silver/Gold colunar (Parquet/Delta) com ACID e time-travel.
- **ETL vs ELT:** ELT (Lakehouse) preserva Bronze e escala; ETL só onde volume pequeno e governança pré-carga.
- **Batch vs Streaming:** híbrido vence — streaming para alertas, batch para analytics; **Lambda** (2 códigos) vs **Kappa** (log único) vs **híbrido LODLog** (Kappa para IoT/TMS, batch para ERP/IBGE).

### Notes:
Revisar objetivos do slide 4 — todos cobertos.

<!-- Slide 39: Próximos passos — Módulo 4 -->
# Próximos Passos — Módulo 4 (03-out, aula dupla)
- **Teoria curta (40 min):** 4 pilares de governança do data lake (qualidade, segurança, padrões, ciclo de vida) + checklist de projeto + risco do "pântano de dados".
- **Miniprojeto em grupo (restante):** cada grupo escolhe sub-cenário LODLog (rotas / manutenção preditiva / estoque / fraude), define requisitos do data lake, constrói/alimenta com estruturado + não estruturado, conduz análise e apresenta avaliação pós-projeto.
- **Avaliação:** individual 70% (pipeline planejado, 5 Vs, Bronze/Silver/Gold, batch vs streaming) + grupo 30% (arquitetura + integração + análise + lições) — ver syllabus § Avaliação.
- **Preparem:** tragam o pipeline desenhado hoje — ele vira base do miniprojeto.

### Notes:
Motivar: "o pipeline de hoje é o rascunho do trabalho final".

<!-- Slide 40: Referências -->
# Referências
- Kleppmann, M. (2017). *Designing Data-Intensive Applications.* O'Reilly — caps. 3 (armazenamento), 11 (streaming), 12 (futuro).
- Serra, J. (2024). *Deciphering Data Architectures.* O'Reilly — cloud e Lakehouse.
- Zaharia, M. et al. (2016). Spark: The Definitive Guide. O'Reilly — RDD/DataFrame/Catalyst.
- White, T. (2015). *Hadoop: The Definitive Guide.* O'Reilly — HDFS/YARN/MR.
- Kreps, J. (2014). Questioning the Lambda Architecture. O'Reilly Radar — origem do Kappa.
- Delta Lake / Apache Iceberg / Apache Hudi — docs: formatos transacionais sobre Parquet.
- Databricks Free Edition — https://www.databricks.com/learn/free-edition (login: https://login.databricks.com)
- LODLog: `docs/LODLog/Projeto-Eng-Dados-IA-para-Negocio.md` + `docs/ementa/syllabus.md` Módulo 3.

### Notes:
Deixar QR para Databricks CE.

<!-- Slide 41: Apêndice — validação GraphRAG drift -->
# Apêndice — Validação GraphRAG Drift (a validar)
> Rodar antes da aula com `.env` do hpc-v100:

```bash
set -a; source /workspaces/graphrag/hpc-v100/.env; set +a
graphrag query --root /workspaces/graphrag/hpc-v100 --method drift "Explique IaaS PaaS SaaS e responsabilidade compartilhada na nuvem. Compare AWS Azure e GCP por camada de ingestão armazenamento e processamento."
graphrag query --root /workspaces/graphrag/hpc-v100 --method drift "Explique Hadoop HDFS YARN MapReduce e o ecossistema Hive HBase Sqoop Flume Oozie. Por que Spark superou MapReduce? Compare Hive e Spark SQL."
graphrag query --root /workspaces/graphrag/hpc-v100 --method drift "Explique ETL versus ELT, formatos CSV JSON Avro Parquet ORC Delta Iceberg e arquitetura em camadas ingestão processamento consumo. Quando usar cada formato?"
graphrag query --root /workspaces/graphrag/hpc-v100 --method drift "Explique batch versus streaming e arquiteturas Lambda e Kappa. Quando usar cada uma? Como escolher para ingestão IoT CDC e APIs na LODLog?"
```

> 399 entities / 41 comunidades — índice hpc-v100 — aguardar validação e ajustar slides se drift divergir.

### Notes:
Apêndice não apresentado — backup de validação.

<!-- Slide 42: Dúvidas -->
# Dúvidas?
## Obrigado!
### Próxima aula: 03-out — Miniprojeto Lakehouse (aula dupla)
**Júlio César Chaves — julio.cesar.chaves@fgv.br**
*FGV MBA em IA e Analytics — Arquitetura de Dados e Big Data*

### Notes:
Encerramento.
