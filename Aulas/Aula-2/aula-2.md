# Arquitetura de Dados e Big Data
Aula 2 — 28 de setembro de 2026
Módulo 2 — Ferramentas para Gerenciamento de Dados Distribuídos

### Notes:
Turma MBA em Inteligência Artificial e Analytics Aplicados a Negócios
Professor: Júlio César Chaves — julio.cesar.chaves@fgv.br
Horário: 19h00 às 22h20 (intervalo 15min: 20h40–20h55) — Teoria 1h40 | Prática 1h40

<!-- Slide 1: Capa -->
# Arquitetura de Dados e Big Data
## Aula 2 — Módulo 2: Ferramentas para Gerenciamento de Dados Distribuídos
### 28 de setembro de 2026 | 19h00–22h20 | FGV MBA em IA e Analytics
**Bancos não relacionais · Data Warehouse · Data Lake · Lakehouse · Data Mesh · Data Fabric**
**Medallion (Bronze/Silver/Gold) · Zonas Zaloni · RPG As Cinco Torres Isoladas**
> Validado via GraphRAG drift — root `/workspaces/graphrag/hpc-v100` — modelo `agnes-2.5-flash` — 4 queries drift (28/08/2026)

### Notes:
Capa. Mencionar validação GraphRAG drift e regra metade teórica / metade prática.

<!-- Slide 2: Regra de ouro da aula -->
# Regra da Aula: Metade Teoria, Metade Prática
| Bloco | Horário | Duração | Conteúdo |
|---|---|---|---|
| **Teoria** | 19h00–20h40 | 1h40 | DW x Lake x Lakehouse x Mesh x Fabric + Medallion/Zaloni + NoSQL |
| **Intervalo** | 20h40–20h55 | 15min | — |
| **Prática** | 20h55–22h20 | 1h40 (85min RPG + 20min síntese) | RPG "As Cinco Torres Isoladas" + Lab Medallion no Databricks |

> Cada aula desta disciplina atende obrigatoriamente à regra de 50% teoria / 50% prática (syllabus § Hard rules).
> Validado via drift: escolha arquitetural depende de contexto organizacional — não há "bala de prata". [DRIFT-01]

### Notes:
Reforçar que teoria e prática têm peso idêntico. Citar syllabus.

<!-- Slide 3: Cronograma do curso revisitado -->
# Onde estamos no syllabus
| Aula | Data | Módulo | Foco |
|---|---|---|---|
| 1 | 22-set | M1 — Tipos de dados e Big Data | Visto: OLTP vs OLAP, 5 Vs, LODLog 8 fontes |
| **2** | **28-set** | **M2 — Ferramentas distribuídas** | **Hoje: NoSQL, DW/Lake/Lakehouse/Mesh/Fabric, Medallion/Zaloni** |
| 3 | 29-set | M3 — Cloud e pipelines | IaaS/PaaS/SaaS, Hadoop/Spark/Hive, ETL vs ELT, Lambda/Kappa |
| 4 e 5 | 03-out | M4 — Miniprojeto Lakehouse | Governança + construção e avaliação do data lake LODLog |

> Aula 2 conecta o "quê" (tipos de dados, Aula 1) ao "onde e como guardar" (arquiteturas, Aula 2), antes do "como mover" (pipelines, Aula 3) e do "construir" (M4).

### Notes:
Transição narrativa M1→M2→M3→M4.

<!-- Slide 4: Objetivos de aprendizagem Módulo 2 -->
# Objetivos de Aprendizagem — Módulo 2
Ao final da aula o estudante será capaz de:
1. **Descrever** os componentes e requisitos das modernas arquiteturas computacionais (distribuídas vs centralizadas).
2. **Descrever** os diversos fluxos de dados existentes nas organizações data-driven (batch/streaming/CDC/event-driven).
3. **Compreender** os principais conceitos de arquitetura moderna de dados: DW, Lake, Lakehouse, Data Mesh, Data Fabric.
4. **Avaliar armadilhas** de cada escolha arquitetural usando critérios de Resiliência, Visão e Influência (RPG).
5. **Conectar** princípios de governança (contratos de dados + federada leve) à implementação prática.
6. **Mapear** fontes LODLog para camadas Medallion (Bronze/Silver/Gold) e zonas Zaloni.

Fonte: syllabus Módulo 2 — Objetivos de aprendizagem (validado via drift).

### Notes:
Ler objetivos em voz alta. 2 minutos.

<!-- Slide 5: Recapitulação Aula 1 (ponte) -->
# Recapitulação Relâmpago — Aula 1
- **OLTP (ACID, 3FN)** vs **OLAP (star/snowflake)** — Inmon top-down vs Kimball bottom-up → híbrido real.
- **ETL** (transform antes do load, on-prem) → **ELT** (load direto + dbt na cloud) — validado [DRIFT-01/Aula1].
- **Tipos de dados:** estruturado (Parquet schema-on-write tipado) vs semi (JSON/XML schema-on-read) vs não estruturado (NLP/CV/OCR). 80% global não estruturado.
- **5 Vs:** Volume 864k eventos IoT/dia · Velocity 30s streaming · Variety 3 tipos · **Veracidade 4 camadas** (edge/stream/cross/trust) · Valor R$4.2M multas + R$2.1M downtime.
- **LODLog:** 450 veículos, 12 CDs, 3.200 clientes, ~18k entregas/mês, R$380M — 8 fontes, padrão híbrido Medallion.

> Pergunta de ponte: "Se já sabemos *quais* dados temos (Aula 1), *onde* vamos guardá-los para que sejam confiáveis, escaláveis e governáveis?"

### Notes:
5 minutos de recapitulação ativa (perguntas à turma).

<!-- Slide 6: Agenda detalhada -->
# Agenda da Noite
**Teoria (19h00–20h40):**
1. Por que distribuído? Limites do monolito (5 min)
2. NoSQL em 20 min: KV, Documento, Coluna, Grafo — quando usar vs relacional [DRIFT-02]
3. DW → Lake → Lakehouse: evolução e trade-offs [DRIFT-01]
4. Data Mesh vs Data Fabric: quem é dono vs como governa [DRIFT-01/04]
5. Quando usar cada um: matriz decisória [DRIFT-01]
6. Medallion Bronze/Silver/Gold + Zaloni (5 zonas) + mapeamento LODLog [DRIFT-03]

**Prática (20h55–22h20):**
7. RPG "As Cinco Torres Isoladas" — 5 portas + porta secreta (contratos) [DRIFT-04]
8. Lab 2 no Databricks CE: Bronze→Silver→Gold na prática (ELT com Delta Lake)

### Notes:
Exibir cronômetro.

<!-- Slide 7: Seção Teoria -->
# PARTE 1 — TEORIA (1h40)
## Das ferramentas ao desenho arquitetural

### Notes:
Divisor de seção.

<!-- Slide 8: Por que distribuído? -->
# Por que dados distribuídos?
- **Lei de Moore desacelerando** + volume/velocidade explodindo: scale-up (máquina maior) tem teto físico e custo exponencial.
- **Scale-out (horizontal):** dividir dados e computação em nós commodity — tolerância a falhas + elasticidade.
- **Teorema CAP:** em presença de partição (P), escolher entre Consistência (C) e Disponibilidade (A). NoSQL sacrifica C forte por A e partição; DW relacional prioriza C.
- **Consequência:** não há arquitetura única que otimize volume+velocidade+variedade+veracidade+valor simultaneamente — trade-off é inevitável (eco da Aula 1: 5 Vs).

> Validado drift: lakes centralizados = simples de governar, gargalo em escala; mesh federado = escala, exige maturidade e contratos. [DRIFT-04]

### Notes:
Introduzir CAP brevemente, sem aprofundar prova.

<!-- Slide 9: NoSQL visão geral -->
# Bancos Não Relacionais — Visão Geral
**NoSQL = "Not Only SQL"** — surgem para **escalabilidade horizontal** e **schema flexível** onde o relacional trava.

| Critério | Relacional (SQL) | NoSQL |
|---|---|---|
| Escala de escrita | Vertical (scale-up), ACID forte | Horizontal (sharding nativo), BASE eventual |
| Schema | Rígido, estável | Dinâmico, variável |
| Padrão de acesso | JOINs, integridade referencial | Cache, séries temporais, grafos, documentos |
| Quando manter SQL | Transações financeiras, integridade crítica | — |

> Validado via drift: Redis O(1) para KV, MongoDB para documentos heterogêneos, Cassandra para séries temporais apêndices, Neo4j para relacionamentos. [DRIFT-02]

### Notes:
Quadro comparativo. Não demonizar SQL — complementar.

<!-- Slide 10: NoSQL KV -->
# NoSQL — Chave-Valor (KV)
- **Modelo:** par simples `chave → valor` com acesso **O(1)**.
- **Exemplos:** **Redis**, Amazon DynamoDB, RocksDB, Memcached. [DRIFT-02]
- **Quando usar vs relacional:** cache, sessões, filas, configurações em tempo real — latência sub-milissegundo.
- **LODLog:** telemetria IoT em tempo real (sensor_id → última leitura), cache de rota Google Maps (origem:destino → distância/tempo), flag de bloqueio ANTT.
- **Trade-off:** sem queries por conteúdo; sem JOINs; sem schema.

> Validado drift: ideal para telemetria onde cada sensor tem ID e payload simples. [DRIFT-02]

### Notes:
Exemplo: Redis `SET trk:0342:temp 94.2 EX 60`.

<!-- Slide 11: NoSQL Documento -->
# NoSQL — Documento
- **Modelo:** JSON/BSON aninhado, **schema flexível**, índices em campos aninhados.
- **Exemplos:** **MongoDB**, Couchbase, Firestore, Cosmos DB. [DRIFT-02]
- **Quando usar vs relacional:** payload variável/aninhado, dispositivos heterogêneos (campos diferentes sem migração), logs com formato mutável.
- **LODLog:** eventos IoT heterogêneos (nem todo veículo envia todos os campos), payloads de APIs (Maps/INMET/ANTT com estruturas diferentes), logs de entrega com anexos.
- **Trade-off:** JOINs caros; consistência eventual em escala; governança de schema exige JSON Schema/Avro.

> Validado drift: MongoDB suporta queries em campos aninhados — útil para frota heterogênea. [DRIFT-02]

### Notes:
Mostrar JSON IoT da Aula 1 como exemplo de documento.

<!-- Slide 12: NoSQL Coluna -->
# NoSQL — Coluna / Wide-Column
- **Modelo:** *column families*, **writes sequenciais apend-only**, compressão por coluna, partição por tempo.
- **Exemplos:** **Apache Cassandra**, **HBase**, ScyllaDB, Google Bigtable. [DRIFT-02]
- **Quando usar vs relacional:** séries temporais massivas, logs distribuídos, ingestão de milhões de eventos/s com leitura por janela temporal.
- **LODLog:** série temporal IoT de longa duração (864k/dia → 26M/mês por frota), logs de WMS/TMS particionados por `ano/mes/dia`, histórico de multas ANTT.
- **Alternativas dedicadas:** InfluxDB, TimescaleDB (extensão Postgres) para time-series SQL-like.

> Validado drift: excelente para Cassandra/HBase — escrita sequencial rápida + escala linear. [DRIFT-02]

### Notes:
Mencionar que Parquet colunar herda ideia de coluna para analytics.

<!-- Slide 13: NoSQL Grafo -->
# NoSQL — Grafo
- **Modelo:** nós + arestas com propriedades, **pergunta está nos relacionamentos**.
- **Exemplos:** **Neo4j**, Amazon Neptune, ArangoDB, JanusGraph. [DRIFT-02]
- **Quando usar vs relacional:** topologia de rede, cadeia de suprimentos, dependência entre sensores, detecção de fraude/anomalias em grafos.
- **LODLog:** "quais dispositivos estão conectados a este gateway e falharam nos últimos 5 min?" — milissegundos vs JOIN proibitivo em SQL; otimização de malha de CDs (caminho mínimo).
- **Trade-off:** escrita mais cara; modelagem exige pensar em arestas; overkill para dados tabulares simples.

> Validado drift: grafos respondem queries de conectividade onde relacional faria múltiplos JOINs caros. [DRIFT-02]

### Notes:
Exemplo visual: grafo CD → veículo → entrega → cliente.

<!-- Slide 14: NoSQLResumo prático LODLog -->
# NoSQL na Prática — Arquitetura Híbrida LODLog
- Na vida real, **combina-se múltiplos bancos** (polyglot persistence):

| Camada LODLog | Banco | Motivo |
|---|---|---|
| Cache tempo real (IoT, Maps) | **Redis (KV)** | O(1), TTL, sub-ms |
| Eventos IoT heterogêneos | **MongoDB (Doc)** | schema flexível |
| Série temporal longa | **Cassandra (Coluna)** | apêndice, partição temporal |
| Topologia CDs/Rotas | **Neo4j (Grafo)** | caminho mínimo |
| Analytics (Silver/Gold) | **Parquet/Delta (Lakehouse)** | colunar + ACID |

> Validado drift: arquiteturas IoT maduras combinam Redis + Cassandra + grafo conforme workload. [DRIFT-02]
> Relação com pipeline: NoSQL é camada de **ingestão/armazenamento operacional**; Lakehouse é camada **analítica** — não são excludentes.

### Notes:
Reforçar poliglota: não escolher um, escolher o certo por workload.

<!-- Slide 15: Evolução DW → Lake → Lakehouse (linha do tempo) -->
# Evolução: Data Warehouse → Data Lake → Lakehouse
- **DW (anos 90, Inmon/Kimball):** repositório estruturado, schema-on-write (star/snowflake), ETL, governado — ótimo para BI, caro para dados semi/não estruturados.
- **Data Lake (2011, Hadoop/S3):** dados em formato nativo, schema-on-read, barato, multi-formato — ótimo para ML/exploração, risco de **data swamp** sem catálogo. [DRIFT-01]
- **Lakehouse (2020+, Delta/Iceberg/Hudi):** **híbrido** — escalabilidade do lake + governança/performance do warehouse, ACID + time-travel sobre object storage (S3/ADLS/GCS). [DRIFT-01]
- Engines: Spark, Databricks SQL, Trino sobre formatos abertos.

> Validado drift: Lakehouse unifica pipelines e elimina dualidade lake vs warehouse. [DRIFT-01]

### Notes:
Linha do tempo 1990→2011→2020. Citar Serra (2024).

<!-- Slide 16: Data Warehouse aprofundado -->
# Data Warehouse — Aprofundamento
- **Definição:** repositório centralizado, histórico, schema pré-definido (star/snowflake), ETL antes do load, otimizado para OLAP/BI. [DRIFT-01]
- **Inmon vs Kimball (revisão Aula 1):** Inmon top-down (EDW 3FN → marts) vs Kimball bottom-up (star marts + dimensões conformadas → EDW lógico) → **híbrido com busway** é prática real.
- **Quando usar:** BI estruturado, relatórios regulares, OLAP, requisitos rigorosos de governança e SQL complexo. [DRIFT-01]
- **Limitação:** schema rígido → ingestão de JSON/XML variável é cara; escalar storage/compute juntos é caro.
- **Exemplos:** Snowflake, Redshift, BigQuery, Synapse.

> Validado drift: DW = schema-on-write rígido, fortemente governado, equipe central. [DRIFT-01]

### Notes:
Conectar com ETL→ELT da Aula 1.

<!-- Slide 17: Data Lake aprofundado -->
# Data Lake — Aprofundamento
- **Definição:** repositório de **dados brutos** (estruturado + semi + não) sem schema prévio, object storage barato, retenção longa. [DRIFT-01]
- **Características:** schema-on-read (ingestão rápida), multi-formato simultâneo, escalável horizontalmente.
- **Quando usar:** exploração, ML, volumes heterogêneos (logs, imagens, textos) onde requisitos ainda não claros. [DRIFT-01]
- **Risco:** sem catálogo/governança → **data swamp** (dado existe mas ninguém encontra/confia). Mitigação: catálogo + lineage (LODLog) + camada de metadados Lakehouse.
- **Exemplos:** S3, ADLS Gen2, GCS.

> Validado drift: Lake careceu historicamente de governança e evoluiu para swamp. [DRIFT-01]

### Notes:
Mostrar foto S3 bucket com pastas desorganizadas vs organizadas.

<!-- Slide 18: Lakehouse aprofundado -->
# Lakehouse — Aprofundamento
- **Definição:** **escalabilidade do Lake + governança do Warehouse** no mesmo repositório. [DRIFT-01]
- **Como:** formatos abertos **Delta Lake / Apache Iceberg / Apache Hudi** adicionam **ACID, time-travel, schema enforcement/evolution** sobre object storage.
- **Quando usar:** quer performance de warehouse sem abrir mão de存储 barato + quer **unificar pipelines** (mesmo dado serve BI + ML) e reduzir complexidade de manter dois sistemas. [DRIFT-01]
- **Benefícios:** Bronze/Silver/Gold coexistem sem mover dados; Spark/Trino/Databricks SQL nativos; reprocessamento barato (Bronze retido).
- **Exemplos:** Databricks Lakehouse, Dremio, Apache Iceberg + Spark.

> Validado drift: Lakehouse = metadados ACID + SQL+ML simultâneos; Bronze=raw, Silver=limpo/enriquecido, Gold=agregado. [DRIFT-01/Aula1-DRIFT-02/05]
> Relação Medallion: **Lakehouse = infraestrutura; Medallion = padrão organizacional** sobre ela. [DRIFT-03]

### Notes:
Diagrama Lakehouse com Delta log.

<!-- Slide 19: Comparativo DW vs Lake vs Lakehouse -->
# DW vs Lake vs Lakehouse — Comparativo
| Critério | Data Warehouse | Data Lake | Lakehouse |
|---|---|---|---|
| Schema | schema-on-write, star | schema-on-read, raw | ambos: raw na Bronze, enforce na Silver/Gold |
| Dados | só estruturado | todos os tipos, bruto | todos os tipos, com governança |
| Custo | alto (storage+compute acoplados) | baixo (object storage) | baixo storage + performance warehouse |
| Governança | forte (central) | fraca (risco swamp) | forte (Delta/Iceberg/Hudi) |
| Workload | BI/SQL | ML/exploração | BI + ML unificados |
| Exemplo LODLog | faturamento ERP em star Gold | IoT JSON bruto em Bronze | pipeline completo IoT Bronze→Silver→Gold |

> Validado drift: escolha depende de dados bem compreendidos (DW) vs big data/ML (Lake) vs melhor dos dois (Lakehouse). [DRIFT-01]

### Notes:
Tabela decisória rápida.

<!-- Slide 20: Data Mesh -->
# Data Mesh — O Paradigma Descentralizado
- **Autor:** Zhamak Dehghani (2019) — resposta a gargalos do modelo centralizado em orgs grandes.
- **4 Princípios:**
  1. **Propriedade descentralizada orientada a domínios** — cada domínio (frota, estoque, financeiro) é dono do seu dado.
  2. **Dados como produto** — servidos com SLA, documentação, qualidade (product thinking).
  3. **Plataforma autoatendimento** — infra self-service para domínios publicarem/consumirem.
  4. **Governança computacional federada** — padrões mínimos globais, liberdade local. [DRIFT-01]

- **Quando usar:** orgs grandes/complexas com múltiplas unidades independentes que precisam de **agilidade + autonomia sem perder interoperabilidade**. [DRIFT-01]
- **LODLog:** domínios frota/IoT, operação/TMS, estoque/WMS, financeiro/ERP — cada um como produto de dados.

> Validado drift: Mesh responde **"quem produz e é dono dos dados?"** [DRIFT-01]

### Notes:
Desenhar domínios LODLog como quadrantes.

<!-- Slide 21: Data Fabric -->
# Data Fabric — O Tecido Conectivo
- **Definição:** camada **abstrata de integração e governança** que conecta fontes distribuídas, com metadados automatizados e inteligência em tempo real — "tecido" entre arquiteturas. [DRIFT-01]
- **Como:** framework **metadata-driven** que orquestra políticas de segurança/compliance, descoberta e qualidade de forma centralizada.
- **Quando usar:** ambientes **híbridos/multi-cloud** onde descoberta, qualidade, segurança e governança são críticas e há fontes heterogêneas. [DRIFT-01]
- **Exemplos:** IBM Data Fabric, Talend, Informatica, Microsoft Fabric.

> Validado drift: **Mesh e Fabric são complementares, não competitivos.** Mesh = quem é dono; Fabric = como dados fluem e são governados. Juntos escalam decisão sem sacrificar controle. [DRIFT-01]
> Silva et al. (2020) + Serra (2024): Fabric automatiza o que Mesh distribui.

### Notes:
Venn Mesh vs Fabric. Complementaridade é ponto-chave.

<!-- Slide 22: Matriz Quando Usar Cada Um -->
# Quando Usar Cada Um — Matriz Decisória
| Arquitetura | Quando usar (validado drift) | LODLog |
|---|---|---|
| **Data Warehouse** | BI estruturado, relatórios regulares, OLAP, governança rigorosa | Gold financeiro (ERP) para diretoria |
| **Data Lake** | Exploração, ML, heterogêneos onde análise ainda não clara | Bronze IoT bruto para data science explorar |
| **Lakehouse** | Escalabilidade do lake + governança do warehouse, unificar BI+ML, reduzir dois sistemas | **Recomendado para LODLog (ver M4): Lakehouse Delta** |
| **Data Mesh** | Org grande, domínios independentes, precisa agilidade + interoperabilidade | Se LODLog crescer para 30 CDs/domínios autônomos |
| **Data Fabric** | Híbrido/multi-cloud, descoberta/qualidade/segurança críticas, fontes heterogêneas | Integrar IoT+ERP+WMS+TMS+APIs com catálogo único |

> Validado drift: tabela intenção→estratégia confirma — não há arquitetura universal; escolha = contexto organizacional. [DRIFT-01/04]

### Notes:
Reforçar que LODLog hoje = Lakehouse centralizado; Mesh é futuro se escalar domínios.

<!-- Slide 23: Medallion Bronze Silver Gold -->
# Arquitetura Medallion — Bronze / Silver / Gold
**Padrão de organização em 3 camadas de refinamento** (analogia à purificação do ouro) sobre Data Lake/Lakehouse. [DRIFT-03]

- **Bronze (Raw):** dados **brutos sem transformação**, forma original (JSON, CSV, logs). Auditoria e reprocessamento. [DRIFT-03]
- **Silver (Cleansed/Trusted):** dados **limpos, deduplicados, schema aplicado**, nulos tratados, enriquecidos parcialmente — zona "confiável", qualidade validada. [DRIFT-03]
- **Gold (Curated/Refined):** dados **agregados, modelados dimensionalmente** (star), otimizados para negócio — dashboards, relatórios, ML. [DRIFT-03]

> Lakehouse = infra (onde/como armazena); Medallion = padrão organizacional (como organiza em camadas de confiança). [DRIFT-03]
> Formatos: Delta/Iceberg/Hudi → ACID + time-travel + schema evolution.

### Notes:
Diagrama funil Bronze→Silver→Gold com setas.

<!-- Slide 24: Zonas Zaloni -->
# Zonas de Refinamento — Zaloni (5 zonas)
Mapeamento direto às camadas Medallion: [DRIFT-03]

| Zona Zaloni | Equivalente Medallion | Papel |
|---|---|---|
| **Transiente (Transient)** | — | transformações temporárias, explorações |
| **Bruta (Raw)** | **Bronze** | recebe dados como chegam |
| **Confiável (Trusted)** | **Silver** | validado, deduplicado, qualidade garantida |
| **Refinada (Refined)** | **Gold** | pronto para consumo analítico/executivo |
| **Sandbox** | — | POCs, ciência de dados, prototipagem sem impacto em produção |

> Validado drift: Zaloni adiciona Transiente e Sandbox às 3 camadas Medallion — úteis para experimentação e reprocessamento. [DRIFT-03]
> LODLog lineage (mesmo nome "LODLog" do corpus, mas aqui como conceito de lineage/logging) registra transformações em cada zona. [DRIFT-03]

### Notes:
Tabela Zaloni ↔ Medallion. Explicar que Transiente/Sandbox são "auxiliares".

<!-- Slide 25: Mapeamento LODLog → Medallion -->
# LODLog → Medallion na Prática
| Fonte LODLog | Bronze (raw) | Silver (trusted) | Gold (refined) |
|---|---|---|---|
| **IoT 864k/d JSON** | JSON bruto S3 `bronze/iot/YYYY/MM/DD/` | Delta validado, deduplicado, `vel 0-200, temp 50-150` + média móvel | `fato_iot_hora` + `dim_veiculo` — avg temp/vel por veículo/hora |
| **ERP 3k/d** | CSV diário bruto | Parquet tipado, FKs validadas | `fato_faturamento` + `dim_cliente` — receita por cliente/região |
| **WMS 48k/d** | CSV 15min bruto | DeltaCDC, SCD2 | `fato_estoque` — ruptura, giro |
| **TMS real-time** | JSON CDC bruto | Delta com SLA calculado | `fato_entregas` + `dim_tempo` — % atraso, multas |
| **Maps/INMET/ANTT** | JSON/XML bruto + cache | enriquecimento | features para predição de atraso |

> Validado drift: Bronze retém brutos para reprocessamento; Silver garante veracidade; Gold dimensional para consumo. [DRIFT-03]

### Notes:
Exemplo concreto para cada fonte. Conectar com 5 Vs da Aula 1.

<!-- Slide 26: Intervalo -->
# ☕ INTERVALO — 15 minutos
## 20h40–20h55

> Retornamos com o RPG "As Cinco Torres Isoladas" — tragam a decisão mais difícil que já viram em arquitetura de dados!

### Notes:
Slide de intervalo.

<!-- Slide 27: Seção Prática -->
# PARTE 2 — PRÁTICA (1h40)
## RPG "As Cinco Torres Isoladas" + Lab Medallion ao Vivo

### Notes:
Divisor prática.

<!-- Slide 28: RPG Intro — Narrativa -->
# RPG "As Cinco Torres Isoladas" — O Enunciado
**Cenário fictício LODGov** (rede global de serviços profissionais, análoga à LODLog em escala maior):
- Silos entre RH, CRM, ERP e legados — 5 torres isoladas que não se falam.
- **C-Levels em conflito** (falas no roteiro `As cinco torres isoladas.md`):
  - **CMO:** "Preciso de visão 360 do cliente ontem!"
  - **CDO:** "Sem governança, tudo vira pântano!"
  - **CIO:** "Não podemos parar a operação para reescrever tudo!"
  - **CHRO:** "Cada área precisa de autonomia!"
  - **CEO:** "Quanto custa e quando entrega valor?"
- **Vocês são o CTO.** Escolham uma das **5 portas** arquiteturais — todas têm armadilhas — e defendam.

> Validado drift: integração incremental = validação contínua + rollback pontual (adequada para sistema grande/complexo); big bang = só para escopo pequeno/bem delimitado. [DRIFT-04]

### Notes:
Ler falas com vozes. 5 minutos.

<!-- Slide 29: As 5 portas — Visão geral -->
# As 5 Portas — Escolha seu veneno
| Porta | Nome no RPG | Arquitetura | Ideia central | Armadilha oculta |
|---|---|---|---|---|
| **1** | Conselho Federado dos Domínios | **Data Mesh puro** | autonomia total por domínio | coordenação cara, padrões divergem, sem contratos vira caos |
| **2** | Lago Único do Conhecimento | **Lake/Lakehouse centralizado** | tudo num só lago governado | gargalo central, fila de TI, domínios perdem agilidade |
| **3** | Colheita Silenciosa | **Integração incremental sem blueprint** | quick wins, sem plano mestre | dívida técnica, silos reconectados de forma frágil |
| **4** | Grande Ressaca | **Big bang / rip-and-replace** | reescrever tudo de uma vez | risco operacional, custo, paralisação — só para escopo pequeno |
| **5** | Tribunal das Leis | **Governança antes da tecnologia** | governança perfeita primeiro | paralisia por análise, resistência, sem entrega tangível |

> Validado drift: incremental é preferível para maioria das orgs **se** houver decomposição por domínios; big bang só quando custo/tempo do incremental não se justifica. [DRIFT-04]
> Todas as 5 têm score negativo em pelo menos um eixo — alunos escolhem a "menos pior".

### Notes:
Não revelar scores ainda. Deixar escolherem.

<!-- Slide 30: Pontuação — 3 eixos -->
# Como pontuamos — Resiliência / Visão / Influência (-4 a +4)
- **Resiliência (Vigor):** o sistema aguenta falhas, reprocessamento, escala sem quebrar?
- **Visão (Astúcia):** a escolha antecipa futuro, evita débito, permite evolução?
- **Influência (Presença):** a escolha ganha aliados, entrega valor visível, sustenta patrocínio?

Cada porta é pontuada nos 3 eixos (ex.: Mesh +3 Visão, -2 Resiliência se sem contratos). Detalhes em `portas-e-scores.md`.
> Validado drift: governança federada leve + contratos = piso mínimo obrigatório definido federativamente, liberdade local no teto. [DRIFT-04]

### Notes:
Explicar que scores são narrativa, não matemática exata.

<!-- Slide 31: Porta secreta — Ponte dos Contratos -->
# A Porta Secreta — "Ponte dos Contratos"
**Não está na lista. Vocês precisam deduzi-la.**

> **Síntese de maior pontuação:** **Contratos de dados + domain ownership com padrões mínimos + governança federada leve + Bronze descentralizado / Silver-Gold centralizado.**

- **Contratos de dados:** acordo formal produtor↔consumidor — schema, qualidade, SLAs, responsabilidades, versionamento semântico (backward/forward/full). [DRIFT-04]
- **Governança federada leve:** **subsidiariedade** — decide no nível mais próximo do dado; central só quando impacto sistêmico; **monitora, não controla** (métricas/alertas). [DRIFT-04]
- **Implementação LODLog:** Bronze descentralizado (cada domínio ingere seu raw), Silver/Gold centralizado com Delta + catálogo + registry com descoberta automática. [DRIFT-04]
- **Começar pelo essencial:** schema + qualidade mínima + lineage + segurança; detalhes ficam no domínio.

> Validado drift: registry de produtos de dado com descoberta automática é camada de descoberta que permite consumo por contrato. [DRIFT-04]

### Notes:
Revelar após discussão. Conectar com Medallion.

<!-- Slide 32: Dinâmica da noite -->
# Dinâmica — Como vamos jogar (85 min)
1. **Formem 5 grupos** (um por porta) — 5 min
2. **Leiam a porta** + discutam armadilhas — 15 min
3. **Apresentem defesa** (2 min por grupo) + **recebam consequências narradas** — 15 min
4. **Pistas progressivas** do professor até alguém propor a porta secreta — 15 min
5. **Votação final** — qual porta escolheriam agora? — 5 min
6. **Síntese técnica:** mapear domínios LODLog (frota/IoT, operação/TMS, estoque/WMS, financeiro/ERP) para Bronze/Silver/Gold com contratos — 30 min

> Alternativa/reforço (syllabus): se o RPG for abertura de 30-40 min, o restante é o lab técnico de mapeamento para Medallion — ambos válidos.

### Notes:
Cronometrar.

<!-- Slide 33: Exercício técnico pós-RPG -->
# Exercício Técnico — Mapear LODLog para Medallion com Contratos
**Para cada domínio LODLog, decidam:**

| Domínio | Fontes | Arquitetura recomendada | Bronze | Silver (contrato) | Gold |
|---|---|---|---|---|---|
| **Frota/IoT** | IoT JSON 30s + ANTT | Lakehouse + Cassandra (série temporal) | JSON raw S3 | Delta validado: `vel 0-200, temp 50-150, dedup 30s, lineage` | `fato_frota_hora` |
| **Operação/TMS** | TMS CDC | Lakehouse CDC + KV cache Maps | JSON CDC | Delta SLA + `atraso_min` | `fato_entregas` |
| **Estoque/WMS** | WMS 15min | Lakehouse batch | CSV raw | Delta SCD2 | `fato_estoque` |
| **Financeiro** | ERP + IBGE | Warehouse/Lakehouse | CSV raw | Parquet tipado | `fato_faturamento` + enrich IBGE |

Entregável: 1 slide por grupo com justificativa batch/streaming + contrato mínimo.

### Notes:
Exercício conecta RPG + Medallion + LODLog.

<!-- Slide 34: Lab Databricks — Visão geral -->
# Lab 2 ao Vivo — Medallion no Databricks CE
**Objetivo:** implementar **Bronze → Silver → Gold** com **Delta Lake** (ELT) sobre dados LODLog simulados.

- **Plataforma:** **Databricks Community Edition** (https://community.cloud.databricks.com) — gratuito, sem cartão, Spark + Delta nativo. [Aula 1]
- **Scripts em `/Aulas/Aula-2/Labs/`:**
  - `lab2-medallion-bronze-silver-gold.py` — pipeline completo IoT (bronze JSON → silver validado → gold agregado)
  - `lab2-nosql-simulation.py` — simulação KV/Documento/Coluna/Grafo com PySpark + Delta
  - `lab2-rpg-exercicio.py` — template para o exercício de mapeamento de domínios

> Validado drift: formatos abertos Delta/Iceberg/Hudi + engines Spark/Trino/Databricks SQL executam processamento distribuído nas camadas Silver/Gold. [DRIFT-03]

### Notes:
Mostrar Databricks CE na tela.

<!-- Slide 35: Lab passo a passo -->
# Lab 2 — Passo a Passo no Databricks CE
1. **Acessar** https://community.cloud.databricks.com → criar workspace → novo notebook Python.
2. **Upload** dos arquivos de exemplo para `FileStore` ou `/mnt/data` (ou gerar sintéticos com o script — funciona offline).
3. **Bronze:** `spark.read.json(".../bronze/iot/*.json")` — schema-on-read, `printSchema()`, `display(limit 10)`, `count()` → ~864k/dia validado Aula 1.
4. **Silver:** validar 4 camadas Veracidade — `filter((vel>=0)&(vel<=200)&(temp>=50)&(temp<=150))` + dedup + `withColumn("data", to_date(...))` → escrever Delta `.../silver/iot/` com `mode("append")` + `option("mergeSchema", "true")`.
5. **Gold:** `groupBy("veiculo_id", "data").agg(avg("temperatura"), avg("velocidade"))` → `fato_frota_hora` Delta + `display()` + gráfico.
6. **Time-travel:** `SELECT * FROM delta.`/silver/iot` VERSION AS OF 1` — auditoria.

### Notes:
Guia prático para alunos executarem em sala ou casa.

<!-- Slide 36: Lab snippet -->
# Lab 2 — Snippet Validado (drift)
```python
# Bronze: ingestão raw schema-on-read
df_bronze = spark.read.json("/FileStore/bronze/iot/*.json")
df_bronze.printSchema()
display(df_bronze.limit(10))
print(f"Bronze count: {df_bronze.count():,}")  # 450 x 288/dia = pipeline real

# Silver: 4 camadas de validação (edge range + dedup + provenance)
from pyspark.sql.functions import col, to_date
df_silver = df_bronze.filter(
    (col("velocidade_kmh") >= 0) & (col("velocidade_kmh") <= 200) &
    (col("temperatura_motor_c") >= 50) & (col("temperatura_motor_c") <= 150)
).dropDuplicates(["veiculo_id", "timestamp"]) \
 .withColumn("data", to_date(col("timestamp")))

df_silver.write.format("delta").mode("append") \
  .option("mergeSchema", "true").save("/FileStore/silver/iot")
```

> Mitiga swamp: catálogo + Delta ACID + lineage em cada zona (Trusted/Refined). [DRIFT-03]

### Notes:
Copiar e colar no notebook.

<!-- Slide 37: Discussão pós-lab -->
# Discussão Pós-Lab (20 min)
1. Qual arquitetura (DW/Lake/Lakehouse/Mesh/Fabric) vocês escolheriam para a **LODLog hoje** vs **LODLog com 30 CDs**? Por quê? (Matriz DRIFT-01)
2. Onde **NoSQL** entra e onde **Delta Lakehouse** resolve melhor? (KV para cache vs Silver Gold colunar)
3. Qual **contrato mínimo** vocês exigiriam na Silver da frota? (schema + qualidade + SLA + lineage)
4. Como **Zaloni Transiente/Sandbox** ajudaria a testar novo modelo de predição de atraso sem impactar produção?
5. Que **risco de veracidade** das 4 camadas (edge/stream/cross/trust) é mais crítico na LODLog e por quê?

### Notes:
Perguntas conectam drift + LODLog + governança.

<!-- Slide 38: Resumo da aula -->
# Resumo — O que levamos hoje
1. **NoSQL:** KV (Redis O(1)), Documento (MongoDB flex), Coluna (Cassandra série temporal), Grafo (Neo4j relacionamentos) — polyglot, não "um vence todos". [DRIFT-02]
2. **Evolução:** DW (schema-on-write, BI) → Lake (schema-on-read, barato, risco swamp) → **Lakehouse (Delta/Iceberg/Hudi, ACID + time-travel, unifica BI+ML)**. [DRIFT-01]
3. **Mesh vs Fabric:** Mesh = quem é dono (4 princípios Dehghani); Fabric = como governa/flui (metadata-driven); **complementares**. [DRIFT-01/04]
4. **Quando usar:** matriz decisória — LODLog hoje = Lakehouse centralizado; Mesh quando escalar domínios. [DRIFT-01]
5. **Medallion + Zaloni:** Bronze=Raw, Silver=Trusted, Gold=Refined (+ Transiente/Sandbox); **Lakehouse=infra, Medallion=padrão**. [DRIFT-03]
6. **Porta secreta:** contratos + federada leve + Bronze descentralizado / Silver-Gold centralizado. [DRIFT-04]
7. **Prática:** RPG 5 portas + pipeline Bronze→Silver→Gold em Delta no Databricks CE.

### Notes:
Recapitulação de 3 minutos.

<!-- Slide 39: Próximos passos e avaliação -->
# Próximos Passos
- **29-set (M3):** Cloud (IaaS/PaaS/SaaS), Hadoop/Spark/Hive, ETL vs ELT, Lambda/Kappa — tragam dúvidas do RPG!
- **Trabalho individual 70% (18/out):** cenário LODLog (rotas/manutenção/estoque/fraude) + 3-5 fontes + **5 Vs com 4 camadas Veracidade** + **Bronze/Silver/Gold com Delta/Iceberg + contrato mínimo**.
- **Trabalho em grupo 30% (03/out):** arquitetura simplificada + integração estruturada + semi/não + análise + lições.
- **Dica:** escolham **Lakehouse Delta** e definam contrato Silver já — evita swamp e impressiona na banca.

> Leitura: Serra (2024) cap. 3-5; Silberschatz cap. 10; DAMA-DMBOK 2 — Arquitetura de Dados; Ghemawat GFS (2003).

### Notes:
Reforçar peso do trabalho e prazo.

<!-- Slide 40: Referências -->
# Referências
- Serra, J. (2024). *Deciphering Data Architectures: Choosing between a modern data warehouse, data fabric, data lakehouse, and data mesh.* O'Reilly Media.
- Silva, F. R., Santos, R. M., & Oliveira, L. A. (2020). *Cloud computing.* Soluções Educacionais Integradas.
- Inmon, W. H., Linstedt, D., & Levins, M. (2019). *Data Architecture: A Primer for the Data Scientist.* Elsevier.
- Dehghani, Z. (2022). *Data Mesh: Delivering Data-Driven Value at Scale.* O'Reilly.
- Kleppmann, M. (2017). *Designing Data-Intensive Applications.* O'Reilly — Cap. 2-3 (NoSQL, particionamento).
- Ghemawat, S. et al. (2003). *The Google File System.* SOSP.
- Delta Lake, Apache Iceberg, Apache Hudi — docs oficiais (ACID sobre object storage).
- DAMA-DMBOK 2 (2017) — Arquitetura de Dados, Governança.
- LODLog — *Projeto Eng. Dados IA para Negócio* (cenário da disciplina).

### Notes:
Bibliografia básica + complementar do syllabus (validada).

<!-- Slide 41: Apêndice — Validação GraphRAG drift -->
# Apêndice — Validação GraphRAG DRIFT (28/08/2026)
**Root:** `/workspaces/graphrag/hpc-v100` · **Modelo:** `agnes-2.5-flash` · **drift:** `n_depth 2, k_followups 5, primer_folds 2` · **Index:** 399 entities / 41 comunidades / LanceDB bge-m3 1024.

**4 queries reprodutíveis (slide por slide):**
1. `graphrag query --root /workspaces/graphrag/hpc-v100 --method drift "Defina Data Warehouse, Data Lake, Lakehouse, Data Mesh e Data Fabric. Quando usar cada um?"` → definições + quando usar + complementaridade Mesh/Fabric. [DRIFT-01, slides 15-22]
2. `graphrag query --root /workspaces/graphrag/hpc-v100 --method drift "Explique bancos de dados NoSQL: tipos chave-valor, documento, coluna e grafo. Quando usar cada um em vez de relacional? Relacione com ingestão de dados IoT e logs."` → 4 tipos + exemplos Redis/Mongo/Cassandra/Neo4j + polyglot. [DRIFT-02, slides 9-14]
3. `graphrag query --root /workspaces/graphrag/hpc-v100 --method drift "Explique a arquitetura Medallion Bronze Silver Gold e as zonas de refinamento Zaloni transiente bruta confiável refinada sandbox. Como se relacionam com Data Lakehouse e com a LODLog?"` → Medallion 3 camadas + Zaloni 5 zonas + Lakehouse=infra vs Medallion=padrão. [DRIFT-03, slides 23-25]
4. `graphrag query --root /workspaces/graphrag/hpc-v100 --method drift "Quais são os trade-offs entre Data Mesh federado, Data Lake centralizado, integração incremental, big bang e governança antes da tecnologia? Como escolher contratos de dados e governança federada leve?"` → trade-offs 5 portas + contratos + federada leve + registry. [DRIFT-04, slides 28-33]

**Limitação do corpus:** LODLog como "sistema de linhagem" no drift-03 é inferência do modelo sobre o termo, não fato do cenário (LODLog é empresa fictícia de logística) — mantido como proposição didática com nota de transparência, como na Aula 1.

**Comandos:** ver acima. Cada query custa LLM sem cache — não repetir sem necessidade. Módulo MCP usado para validar complementaridade Fabric/Mesh e exemplos NoSQL.

### Notes:
Transparência metodológica — como na Aula 1 (DRIFT-01..05). Informar custo de query.

<!-- Slide 42: Dúvidas -->
# Dúvidas?
## Prof. Júlio César Chaves
julio.cesar.chaves@fgv.br — eCLASS: fórum de dúvidas — Office hours: terça 14h–16h

**Próxima aula: 29-set — Cloud e Pipelines (Hadoop/Spark/Hive, ETL→ELT, Lambda/Kappa)**

> Traga seu notebook com Databricks CE logado — vamos desenhar pipelines LODLog ao vivo!

### Notes:
Encerramento.
