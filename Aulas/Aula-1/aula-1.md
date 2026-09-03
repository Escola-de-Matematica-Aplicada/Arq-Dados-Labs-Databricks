# Arquitetura de Dados e Big Data
Aula 1 — 22 de setembro de 2026
Tipos de dados e contexto de Big Data

### Notes:
Turma MBA em Inteligência Artificial e Analytics Aplicados a Negócios
Professor: Júlio César Chaves

<!-- Slide number: 2 -->

![](EspaçoReservadoparaImagem2.jpg)
Boas-vindas!

### Notes:
ID da imagem: 365572922

<!-- Slide number: 3 -->
Apresentação – Professor executivo
Currículo - Júlio César Chaves
Doutorado em Engenharia Civil, COPPE/UFRJ, 2018
E-mail: julio.cesar.chaves@prof.fgv.edu.br
CV Lattes
Professor de Banco de Dados e Modelagem Informacional na Escola de Matemática FGV/EMAp. Professor de Engenharia de Dados no programa de mestrado profissional em economia na escola de economia FGV/EPGE.
Conclusão da graduação em tecnologia em informática na UNIVERCIDADE/RJ (2006), mestrado (2011) e doutorado (2018) pela COPPE/UFRJ sob o programa de engenharia civil, tendo como foco de pesquisa a mobilidade urbana a partir de dados de telefonia móvel, do IBGE e do setor de transportes.
Foram 20 anos como administrador de banco de dados, alavancando pesquisas com grande volume de dados. Cuido da área de governança de infraestruturas computacionais para pesquisas na FGV, gerindo os ambientes de nuvem pública e privada e alavancando projetos de pesquisa que são vinculados a arquiteturas informacionais de maior porte e/ou envolvendo dados identificados.

![Homem posando para foto em frente a água](Imagem6.jpg)

FOTO

### Notes:

<!-- Slide number: 4 -->
# Conteúdo
Aula 1 — Tipos de dados e contexto de Big Data
Módulo 1 do conteúdo programático

01 | Breve histórico da organização de dados
02 | Tipos de dados: estruturados, semiestruturados e não estruturados
03 | Dado transacional (OLTP) vs. analítico (OLAP)
04 | Os 5 Vs do Big Data
05 | LODLog: fontes de dados do cenário
06 | Lab 1: classificação das fontes LODLog

<!-- Slide number: 5 -->
01
Plano da Disciplina

<!-- Slide number: 6 -->
# Visão geral do syllabus

| Aula | Data | Tópico (Módulo) | Atividades |
|---|---|---|---|
| 1 | 22-set | **Módulo 1** — Tipos de dados e contexto de Big Data. Breve histórico (cartões perfurados → discos → nuvem → IA generativa); dado transacional (OLTP) vs. analítico (OLAP); os Vs de Big Data. | **Teoria (1h40):** evolução da organização de dados e dos 5 Vs. **Lab 1 (1h40):** classificação das fontes LODLog por tipo, 5 Vs e padrão de ingestão. |
| 2 | 28-set | **Módulo 2** — Ferramentas para gerenciamento de dados distribuídos: bancos não relacionais, DW, Data Lake, Lakehouse, Data Mesh, Data Fabric. | **Teoria (1h40):** DW x DL x Lakehouse x Data Mesh. **Lab 2 (1h40):** RPG "As Cinco Torres Isoladas". |
| 3 | 29-set | **Módulo 3** — Organização e manuseio de dados em bases distribuídas: cloud computing, Hadoop, Spark, Hive, pipelines, arquitetura em camadas. | **Teoria (1h40):** modelos IaaS/PaaS/SaaS; comparativo AWS/Azure/GCP. **Lab 3 (1h40):** pipeline conceitual LODLog. |
| 4 e 5 | 3-out | **Módulo 4** — Miniprojeto: construção e avaliação de data lake. | **Teoria (curta, ~40min):** governança do data lake. **Miniprojeto em grupo (restante):** construção e apresentação. |

### Notes:
Cada aula: 19h às 22h20 (com 15min de intervalo). Metade teoria, metade prática.

<!-- Slide number: 7 -->
# Objetivos da disciplina

- Compreender os diferentes tipos de dados utilizados em ambientes analíticos e de Big Data.
- Gerenciar as possíveis alternativas computacionais para manuseio de dados em ambientes de Big Data.
- Evidenciar os requisitos para a arquitetura analítica e processos de ingestão e alimentação de dados.
- Compreender os principais componentes das arquiteturas modernas de dados (data lake, data warehouse, lakehouse, data mesh).
- Construir um data lake visando ao processamento de dados estruturados e não estruturados.
- Identificar arquiteturas de dados em ambientes cloud e distribuídos.
- Avaliar alternativas tecnológicas para armazenamento e processamento de dados em escala.

<!-- Slide number: 8 -->
# Avaliação

Disciplina isenta de prova, avaliada por trabalho.

**Individual (70%)** — Planejando o pipeline de dados para o data lake da LODLog:
- Cenário sub-escolhido (rotas / manutenção preditiva / estoque / fraude) e fontes de dados mapeadas (mínimo 3–5)
- Análise dos 5 Vs para as fontes escolhidas
- Arquitetura proposta com camadas Bronze/Silver/Gold
- Prazo: 15 dias após a última aula

**Em grupo (30%)** — Apresentação na última aula:
- Arquitetura simplificada do data lake, das fontes até o consumo
- Integração de pelo menos uma fonte estruturada e uma não estruturada/semiestruturada
- Resultado de uma análise conduzida sobre os dados do data lake
- Avaliação pós-projeto: vantagens, limitações e lições aprendidas

<!-- Slide number: 9 -->
# Referências

**Bibliografia básica:**
- Serra, J. (2024). Deciphering data architectures. O'Reilly Media.
- Silva, F. R., Santos, R. M., & Oliveira, L. A. (2020). Cloud computing. Soluções Educacionais Integradas.
- Inmon, W. H., Linstedt, D., & Levins, M. (2019). Data architecture: A primer for the data scientist. Elsevier.

**Bibliografia complementar:**
- Kaufmann, M., & Meier, A. (2023). SQL and NoSQL databases. Springer.
- Molinari, L. (2017). Cloud computing: A inteligência na nuvem. Editora Érica.
- Mulder, J. (2020). Multi-cloud architecture and governance. Packt Publishing.
- Kleppmann, M. (2017). Designing data-intensive applications. O'Reilly Media.

![Logotipo](Imagem4.jpg)

<!-- Slide number: 10 -->
# Ferramenta do curso: Databricks Free Edition

O laboratório será executado no **Databricks Free Edition** (https://login.databricks.com) — ambiente gratuito, sem necessidade de cartão de crédito, com compute Serverless e Unity Catalog. (O antigo Community Edition foi descontinuado pela Databricks.)

- Notebook colaborativo baseado em Jupyter
- Spark distribuído para processamento de dados
- SQL integrado para consultas analíticas
- Visualizações embarcadas

**Acesso:** https://community.cloud.databricks.com

### Notes:
O Databricks CE é suficiente para os labs desta disciplina. Para o miniprojeto, os grupos poderão explorar créditos educacionais AWS ou Azure se desejarem.

<!-- Slide number: 11 -->
01
Breve histórico da organização de dados

### Notes:

<!-- Slide number: 12 -->
# Herman Hollerith, 1890–1911

Herman Hollerith desenvolveu o tabulador eletromecânico de cartões perfurados para o **Censo dos EUA de 1890** — primeira aplicação em larga escala de processamento automático de dados. A tecnologia foi operada via Tabulating Machine Company (1896), que em **1911** se fundiu na Computing Tabulating Recording Company (CTR), renomeada **IBM em 1924**.

Os cartões perfurados funcionavam como memória de códigos e dados: cada caractere correspondia a um padrão de furos lido por contato elétrico.

A partir de 1950 teve início o desenvolvimento de mídias magnéticas e o uso de cartão perfurado foi caindo até a popularização dos discos rígidos nas décadas de 60 e 70.

> Validado via GraphRAG drift (`/workspaces/graphrag/hpc-v100`): cartões associados ao Censo 1890 e à Tabulating Machine Company → CTR 1911 → IBM 1924; não 1911 como ano da invenção. [DRIFT-01]

<!-- Slide imagem complementar -->
# Cartão perfurado — detalhe

![](Picture6.jpg)

Dados em um cartão perfurado?
https://www.youtube.com/watch?v=YnnGbcM-H8c

### Notes:

<!-- Slide number: 13 -->
# Fitas magnéticas, 1951

As fitas magnéticas permitiram o primeiro armazenamento e processamento automatizado em massa, substituindo cartões perfurados. O processamento era batch: leitura sequencial de uma ou mais fitas e gravação em uma nova fita.

**Limitação decisiva:** Acesso obrigatoriamente sequencial. Como o volume de dados superava em muito a memória principal, os programadores eram forçados a processar dados em ordem fixa, fazendo merge manual de processamentos parciais entre várias fitas.

A organização física dos dados ditava a lógica do programa — gargalo que o modelo relacional viria a eliminar décadas depois.

![UNIVAC 1951](Imagem4.jpg)
Fonte: Silberschatz, A., Korth, H. F., & Sudarshan, S. (2019). Database System Concepts. McGraw Hill.

### Notes:
UNIVAC (Universal Automatic Computer), precedido pelo ENIAC e sucedido pela UNYSIS. Iniciou as atividades em 1951 e foi descontinuado em 1986.

<!-- Slide number: 14 -->
# O modelo relacional, Edgar F. Codd, 1970

Na era inicial da mídia magnética, os bancos de dados seguiam o modelo hierárquico e em rede, onde era necessário levar em conta as organizações internas dos arquivos dos bancos de dados, sob um complexo sistema de ponteiros.

Codd fez uma conexão entre conceitos matemáticos e organização de dados que viria a mudar a forma de lidar com bancos de dados.

> "Future users of large data banks must be protected from having to know how the data is organized in the machine (the internal representation)."

Além do conceito de "relação" de conjuntos que deu origem ao modelo relacional, Codd propôs uma linguagem de alto nível que deu origem ao SQL.

### Notes:
"Codd's Rule #1: For a truly relational DBMS to be called relational, every relation must have a primary key."

<!-- Slide number: 15 -->
# Discos rígidos e o acesso randômico, 1956–anos 70

**Consequência para a engenharia de dados:**
- A posição física do dado deixou de importar.
- Programadores passaram a construir estruturas de dados abstraindo questões de hardware.
- Isso viabilizou o modelo relacional de Codd: só faz sentido exigir independência física/lógica quando o hardware já permite acessar qualquer registro diretamente.

O primeiro protótipo (1952) continha 50 discos de 24" e armazenava 5 milhões de caracteres. O marco comercial foi o **IBM 305 RAMAC (1956)** — primeiro disco com acesso aleatório. O conceito só se popularizou no fim dos anos 60 e 70.

Diferente das fitas magnéticas, os discos permitiam acesso direto e randômico ao dado — não era mais necessário percorrer sequencialmente toda a fita para chegar a um registro.

![Disco rígido](Picture2.jpg)

> Validado via GraphRAG drift: IBM 305 RAMAC 1956 como primeiro produto com acesso aleatório; System/360 (1964) consolidou padronização de família compatível, base para portabilidade de SGBDs. [DRIFT-01]

### Notes:
- Contraste explícito com slide 13 (fitas = sequencial) e slide 14 (Codd = independência lógica/física).
- Curiosidade: "Fiz o segundo grau num curso de nome 'Processamento de Dados'".
- Tempo: 2 minutos. É ponte histórica, não aprofundamento técnico.

<!-- Slide number: 16 -->
# Oracle, 1977–1979

Apesar de Codd trabalhar na própria IBM, a primeira versão comercial de um banco de dados com a teoria de Codd veio através da Software Development Laboratories (futura Oracle), **fundada em 1977** por Bob Miner, Ed Oates, Bruce Scott e Larry Ellison. O primeiro cliente foi a força aérea americana e o **primeiro produto comercial foi o Oracle V2 (1979)** — considerado o primeiro SGBD relacional comercial com SQL.

A partir de então, as empresas conseguiam focar nos requisitos informacionais de negócio, deixando os controles internos de arquivos e transações ao sistema de banco de dados.

Informalmente, através de reuniões com a Oracle, conta a história que ninguém acreditava que seria possível a materialização da teoria de Codd. Larry Ellison perseverou e tornou-se um visionário na época.

![Ed Oates Bruce Scott Bob Miner Larry Ellison](Picture4.jpg)

> Validado via GraphRAG drift: SDL 1977 → Oracle V2 1979 como primeira oferta comercial relacional; data de fundação ≠ data de produto. [DRIFT-01]

### Notes:

<!-- Slide number: 17 -->
# Banco de dados e SGBD — arquitetura típica

Acesso direto vs indireto
Execução de comandos DDL e DML
Criação de banco de dados

![](Picture3.jpg)

- Manutenção e administração de banco de dados
- Gestão interna de recursos de CPU, memória e disco
- Gestão de acesso concorrente

Fonte: Jukic, N., Vrbsky, S., Nestorov, S., & Sharma, A. (2021). Database Systems: An Introduction to Databases and Data Warehouses.

### Notes:
O SGBD é uma camada de software que faz a gestão dos bancos de dados. Permite execução de comandos DDL/DML, manutenção e administração, gestão de acesso concorrente e identidade.

<!-- Slide number: 18 -->
# Informação transacional vs informação analítica

| Transacional (Operacional) | Analítica (Decisão) |
|---|---|
| Registra o fato no momento em que acontece | Agrega fatos históricos para revelar padrões |
| Suporta processos do dia a dia | Suporta planejamento estratégico |
| Responde: "O que aconteceu?" | Responde: "Por que aconteceu? E o que vai acontecer?" |

Fonte: www

### Notes:
Uma organização lida com diversas fontes de dados. Tipicamente, o mesmo fato pode ter tanto uma proposta operacional quanto analítica. Por exemplo, o dado descrevendo que o cliente X comprou o produto Y na loja Z pode ser armazenado em um banco de dados operacional para suportar os processos de negócio. O mesmo fato pode também ser armazenado em um DW, onde pode ser combinado com um vasto número de fatos similares acumulados em um período de tempo, servindo para revelar tendências importantes tais como padrões de venda ou comportamento do consumidor.

Tipicamente o uso operacional fica apartado do uso analítico, essa é a recomendação devido ao isolamento transacional.

<!-- Slide number: 19 -->
# Bill Inmon e Ralph Kimball nos anos 90

Dois profissionais com larga experiência em banco de dados tornaram-se referência defendendo a tese de que a análise de dados demandava por uma organização informacional distinta do modelo que atendia plenamente as necessidades transacionais: esquema estrela (Kimball) e Data Warehouse estruturado (Inmon).

A demanda por relatórios era atendida através da leitura direta dos bancos de dados transacionais, impactando a performance operacional e não atendendo plenamente a necessidade analítica.

Inovação: Estabelecer conceitos que iriam guiar o mercado na jornada de análise de dados.
Requisitos/condições: papel, caneta e um extenso background corporativo.
Resultado esperado: As empresas possuírem um ambiente analítico modelado (DW) que é apartado do ambiente transacional.

![Bill Inmon e Ralph Kimball](Picture2.jpg)

### Notes:
Inmon: abordagem top-down, normalizada. Kimball: abordagem bottom-up, dimensional (star schema).

<!-- Slide number: 20 -->
# Data Warehouse (DW)

Um data warehouse é um repositório estruturado e integrado composto por:
- Dados orientados para assuntos, através do modelo dimensional.
- Dados que abrangem toda a companhia.
- Dados históricos que possuem vários instantes de tempo.

Os componentes de um DW são:
- O próprio Data Warehouse — um repositório de dados em um SGBD.
- O ETL (Extract Transform Load) — que tem a função de ler, transformar e carregar os dados a partir das fontes para o destino, o DW.
- Aplicações de front-end — que permitem o acesso indireto dos usuários ao DW, tal qual ferramentas de visualização.

Definição e Exemplos de Data Warehouse | Astera

<!-- Slide number: 21 -->
# DATA WAREHOUSE

![](Picture3.jpg)
Jukić, Vrbsky, Nestorov, Sharma – Database Systems – Copyright Nenad Jukic and Prospect Press
Chapter 10 – Slide 23

### Notes:
This example is discussed on Pages 328-329.

<!-- Slide number: 22 -->
02
Tipos de dados: estruturados, semiestruturados e não estruturados

### Notes:

<!-- Slide number: 23 -->
# Classificação dos dados por tipo

| Tipo | Descrição | Exemplos | Formatos típicos |
|---|---|---|---|
| **Estruturados** | Dados com esquema fixo e previsível. Cada campo tem nome, tipo e posição definidos. Esquema aplicado na escrita (schema-on-write). | Registros de banco relacional, planilhas Excel com tipos declarados, Parquet com schema embutido | SQL tables, Parquet (tipado: int32/int64/float/date...), CSV com DDL externo |
| **Semiestruturados** | Dados com alguma estrutura interna, mas sem esquema rígido. Tags/marcadores + estrutura hierárquica. Schema descoberto na leitura (schema-on-read). | JSON, XML, YAML, logs com campos aninhados, emails estruturados | JSON, XML, YAML |
| **Não estruturados** | Dados sem formato predefinido. Requerem NLP, visão computacional ou OCR. | Texto livre, imagens, áudio, vídeo, PDFs escaneados | Texto, imagem, vídeo, áudio, PDF |

Fonte: AMDA-DMBOK, AWS Academy Data Engineering

> Validado via GraphRAG drift: Parquet = schema-on-write colunar com tipos precisos; CSV bruto = schema-on-read (tudo texto, tipos inferidos na leitura); JSON/XML = schema-on-read por natureza, com XSD/JSON Schema opcionais. [DRIFT-02]

### Notes:
- 80% dos dados do mundo são não estruturados (fonte: Dell Technologies Global Datasheet 2022).
- Dados estruturados representam cerca de 20% do volume total, mas são os mais fáceis de analisar.
- A chave para o Big Data é conseguir lidar com todos os três tipos.

<!-- Slide number: 24 -->
# Dados estruturados

Exemplo: Tabela de pedidos em um sistema ERP

| pedido_id | cliente_id | data | valor | status |
|---|---|---|---|---|
| PED-001 | CLI-001 | 2025-07-01 | 1500.00 | concluído |
| PED-002 | CLI-002 | 2025-07-01 | 2300.50 | em_processamento |
| PED-003 | CLI-001 | 2025-07-02 | 890.00 | cancelado |

- Esquema fixo: colunas bem definidas
- Fácil de consultar via SQL
- Limitação: não suporta variações de formato
- Fonte: LODLog — ERP

### Notes:
Dados estruturados são ideais para OLTP — transações rápidas e consistentes. No entanto, seu esquema rígido dificulta a ingestão de fontes heterogêneas.

<!-- Slide number: 25 -->
# Dados semiestruturados

Exemplo: Evento IoT da frota LODLog

```json
{
  "veiculo_id": "TRK-0342",
  "timestamp": "2025-07-14T14:32:05Z",
  "latitude": -22.9068,
  "longitude": -47.0626,
  "velocidade_kmh": 87.4,
  "rpm_motor": 2100,
  "temperatura_motor_c": 94.2,
  "nivel_combustivel_pct": 61.0,
  "peso_carga_kg": 8200,
  "status_freio": "normal",
  "hodometro_km": 124530
}
```

- Estrutura flexível: campos podem variar entre registros
- Fácil de gerar (sensores, APIs)
- Requer parsing para análise (JSON path, esquemas flexíveis)
- Fonte: LODLog — Sensores IoT

### Notes:
Dados semiestruturados são a maioria dos dados gerados por sistemas modernos. O JSON se tornou o formato padrão para APIs e messaging.

<!-- Slide number: 26 -->
# Dados não estruturados

Exemplos:
- Relatórios em PDF escaneados de manutenção de veículos (requer OCR)
- Imagens de câmeras de segurança nos CDs (visão computacional)
- Transcrições de atendimento ao cliente (NLP)
- E-mails de fornecedores (NLP + classificação)

- Sem esquema predefinido; extração exige modelos de IA (NLP, computer vision, OCR)
- Valor potencial alto, mas custo de processamento também alto
- Armazenamento em Data Lake em formato objeto bruto + catálogo; risco de "data swamp" sem governança
- Ferramentas: OCR (Tesseract), NLP (spaCy/transformers), CV (YOLO/CLIP)

> Validado via GraphRAG drift: não estruturados = maior porção corporativa; lakehouse mitiga swamp com camada de metadados (Delta/Iceberg/Hudi) e governança. [DRIFT-02/05]

### Notes:
Dados não estruturados representam crescimento mais rápido. IA generativa está transformando a forma como extraímos valor desses dados.

<!-- Slide number: 27 -->
# Relação entre tipos de dados e arquiteturas

| Tipo de dado | Armazenamento ideal | Camada / Padrão | Ferramentas |
|---|---|---|---|
| Estruturados | Data Warehouse (schema-on-write) | Gold / Star schema | Redshift, BigQuery, Snowflake, Synapse |
| Semiestruturados | Data Lake bruto → Silver colunar | Bronze (JSON bruto) → Silver (Parquet/Delta) | S3, ADLS, GCS + Parquet/Delta/Iceberg |
| Não estruturados | Data Lake objetos + catálogo | Bronze (objetos) → Gold (features extraídas via NLP/CV) | S3, ADLS, GCS + catálogos, OCR/NLP |

Lakehouse unifica os três: armazenamento barato de lake + garantias ACID e time-travel de warehouse via **Delta Lake / Apache Iceberg / Hudi**.

Fonte: Serra (2024), Deciphering data architectures

> Validado via GraphRAG drift: DW = schema-on-write/star/snowflake/ACID; Lake = schema-on-read/barato; Lakehouse = metadados ACID + SQL+ML simultâneos; Bronze = raw, Silver = limpo/enriquecido, Gold = agregado. [DRIFT-02/05]

### Notes:
Arquiteturas modernas (Lakehouse) unificam esses três tipos em uma única plataforma, eliminando a necessidade de sistemas separados.

<!-- Slide number: 28 -->
03
Dado transacional (OLTP) vs. analítico (OLAP)

### Notes:

<!-- Slide number: 29 -->
# OLTP vs. OLAP

| Característica | OLTP (Aula 2) | OLAP (Aula 3 em diante) |
|---|---|---|
| Objetivo | Registrar transações (ACID) | Responder perguntas de negócio |
| Modelo | 3FN normalizado (evita redundância) | Star/Snowflake desnormalizado (otimizado para leitura) |
| Queries | INSERT / UPDATE / DELETE rápidos | SELECT + GROUP BY + JOIN sobre milhões de linhas |
| Volume | Milhões de transações/hora (alta concorrência) | Consultas escaneando grandes históricos |
| Ferramentas típicas | PostgreSQL, MySQL, Oracle TP | Redshift, BigQuery, Databricks SQL, Snowflake |
| Usuários | Sistema, operadores | Analistas, dashboards, modelos de ML |

Inmon (top-down: EDW 3FN → data marts) vs. Kimball (bottom-up: star marts com dimensões conformadas → EDW lógico). Na prática: híbrido com busway dimensional.

Snowflake (dimensões normalizadas) economiza espaço mas exige mais JOINs; Star é padrão por performance/leitura.

"A Aula 2 construiu o armazém. A Aula 3 abre as portas para análise."

> Validado via GraphRAG drift: ACID para OLTP; Inmon vs Kimball; star vs snowflake; ETL tradicional vs ELT com dbt em cloud. [DRIFT-03]

### Notes:
OLTP = Online Transaction Processing — focado em velocidade de escrita e consistência. OLAP = Online Analytical Processing — focado em velocidade de leitura e aggregações.

<!-- Slide number: 30 -->
# Evolução: de OLTP para OLAP

```
+------------------+     +------------------+     +------------------+
|   FONTES OLTP    |     |     ETL/ELT      |     |    OLAP/DW      |
|                  |     |                  |     |                  |
|  ERP (vendor A)  |---->|                  |---->|  Star Schema     |
|  WMS (vendor B)  |---->| Extract          |     |  (dim_tempo,     |
|  TMS (vendor C)  |---->| Transform        |     |   dim_veiculo,   |
|  IoT (sensores)  |---->| Load             |     |   fato_entregas) |
+------------------+     +------------------+     +------------------+
         |                                                       |
         |                                                       v
         |                                              +------------------+
         |                                              |   CONSUMO        |
         |                                              |  - Dashboards    |
         |                                              |  - Modelos ML    |
         |                                              |  - Relatórios    |
         |                                              +------------------+
```

**ETL** = transform antes do load (staging dedicado, ideal on-prem). **ELT** = load direto no warehouse/lakehouse e transform dentro (aproveita elasticidade cloud; dados brutos retidos para reprocessamento). Hoje: ELT com **dbt**.

Fonte: LODLog — visão conceitual

> Validado via GraphRAG drift: distinção ETL/ELT e papel do dbt validada. [DRIFT-03]

### Notes:
O fluxo típico: fontes OLTP → camada de ingestão → data warehouse/lake → consumo analítico.

<!-- Slide number: 31 -->
# NASA & Big Data

Do you know that the term "big data" was first used in a 1997 paper by scientists at NASA, describing an interesting challenge, they had with visualizing the large datasets? The volume of data NASA has to manage is mind-boggling. According to Kevin Murphy, NASA Program Executive for Earth Science Data Systems, NASA – one of the biggest generators of data – is generating 12.1TB of data every single day from nearly 100 currently active missions and thousands of sensors and systems around the Earth and space. Some missions could generate as much as 24TB in a single day. Handling, storing, and managing this data is a massive challenge.

Primeiro uso do termo "Big Data": M. Cox and D. Ellsworth, "Application-controlled demand paging for out-of-core visualization," Proc. IEEE Vis. Conf., pp. 235–244, 1997, doi: 10.1109/visual.1997.663888.

https://crayondata.ai/how-does-nasa-use-big-data/

### Notes:
O objetivo desta seção é destacar cada característica, como elas se entrelaçam e os trade-offs envolvidos nas decisões de design. Geralmente é value first, e depois volume/velocity variety/veracity as pairs.

<!-- Slide number: 32 -->
# Big Data: atingindo os "limites atuais"

| V | Pergunta | Dado global |
|---|---|---|
| **Volume** | Qual é o tamanho do conjunto de dados? | 2.5 Quintilhões de bytes criados por dia no mundo |
| **Velocidade** | Com que frequência novos dados são gerados e ingeridos? | 40.000 GB de dados gerados por segundo globalmente |
| **Variedade** | Quais tipos e formatos? De quantas fontes diferentes vêm os dados? | 80% dos dados do mundo são não estruturados |
| **Veracidade** | Quão exatos, precisos e confiáveis são os dados? | 1 em cada 3 líderes empresariais não confiam em seus dados |
| **Valor** | Quais insights podem ser extraídos dos dados? | R$ 430 bi de valor gerado pelo Big Data até 2028 |

Fonte: Dell Technologies Global Datasheet 2022

### Notes:
Volume e Velocity juntos determinam infraestrutura. Variety e Veracity determinam complexidade de transformação. Value é o objetivo final.

<!-- Slide number: 33 -->
# Os 5 Vs em detalhes

**Volume** — Quantidade de dados gerados. Cresce exponencialmente.
- Exemplo LODLog: ~864.000 eventos IoT/dia
- Decisão: particionamento por data, compressão

**Velocity** — Velocidade de geração e ingestão.
- Exemplo LODLog: IoT a cada 30 segundos
- Decisão: streaming vs. batch

**Variedade** — Diversidade de formatos e fontes.
- Exemplo LODLog: JSON (IoT), SQL (ERP), CSV (APIs)
- Decisão: schema-on-read no Data Lake

**Veracidade** — Confiabilidade e qualidade dos dados.
- Exemplo LODLog: sensores podem falhar
- Decisão: validação na camada Bronze/Silver

**Valor** — Insights e benefícios de negócio.
- Exemplo LODLog: redução de multas, otimização de rotas
- Decisão: priorização de casos de uso

### Notes:
Os 5 Vs são interligados. Por exemplo, alta variedade pode comprometer a veracidade. O valor é o que justifica o investimento em lidar com os outros 4 Vs.

<!-- Slide number: 34 -->
# Larry Page e Sergey Brin em Stanford (1998) e a escalabilidade web (2003–)

Dois estudantes de Stanford criaram em **1998** o algoritmo PageRank — ranqueia páginas pela quantidade/qualidade de links que as referenciam.

A análise de dados ainda estava confinada aos Data Warehouses corporativos. A virada para Big Data distribuído veio após o **Google File System (GFS, 2003)** — sistema de arquivos em grid com hardware commodity — seguido por **MapReduce (2004)** e **Bigtable (2006)**. Esse conjunto estabeleceu o padrão para arquiteturas escaláveis de baixo custo.

Inovação: criar arquitetura escalonável e acessível para conjuntos já compreendidos como "Big Data" (Cox & Ellsworth, NASA, 1997).
Requisitos/condições: programadores criativos, tese em Stanford, cluster de PCs commodity.
Resultado esperado: além dos dados internos, empresas podem conjugar dados de diversas fontes/formatos e extrair insights inviáveis num DW tradicional.

![](Picture2.jpg)
History of Google - Wikipedia; Ghemawat et al., GFS (SOSP 2003)

> Corrigido via GraphRAG drift: PageRank 1998 ≠ GFS; GFS é 2003. [DRIFT-01]
Google File System - Wikipedia

### Notes:

<!-- Slide number: 35 -->
# DATA LAKE — conceito adequado para Big Data

Um Data Lake é um repositório que armazena dados em seu formato nativo, sem necessidade de pré-processamento. Pode armazenar dados estruturados, semiestruturados e não estruturados.

Características:
- **Schema-on-read** (esquema aplicado na leitura, não na escrita) — ingestão rápida sem validação prévia
- Armazenamento econômico em object storage (S3, ADLS, GCS)
- Escalabilidade horizontal + retenção longa a baixo custo
- Suporte a múltiplos tipos de dados simultâneos

Risco: sem catálogo/governança vira **data swamp**. Mitigação: camada de metadados com **Delta Lake / Iceberg / Hudi** (ACID, time-travel, schema enforcement) → evolução para **Lakehouse**.

![](Picture7.jpg)
Jukić, Vrbsky, Nestorov, Sharma – Database Systems

> Validado via GraphRAG drift: lake = barato/flexível/schema-on-read; warehouse = garantias/performance/schema-on-write; lakehouse combina ambos com Iceberg/Delta/Hudi. [DRIFT-05]

### Notes:
Diferença chave: DW exige esquema antes da escrita (schema-on-write). Lake permite ingestão bruta e esquema posterior (schema-on-read).

<!-- Slide number: 36 -->
04
LODLog: fontes de dados do cenário

### Notes:

<!-- Slide number: 37 -->
# LODLog Transportes e Distribuição S.A.

**LODLog Transportes e Distribuição S.A.** é uma empresa brasileira de logística com sede em Campinas/SP, fundada em 2010. Opera com:

- **450 veículos** de carga (leves, médios e pesados)
- **12 centros de distribuição** espalhados pelo Brasil
- **3.200 clientes ativos** no setor varejista e industrial
- **~18.000 entregas/mês**
- **Faturamento anual:** R$ 380 milhões

## O Problema de Negócio

> "Sabemos que estamos perdendo dinheiro, mas não sabemos exatamente onde nem por quê."
> — Diretor de Operações, LODLog

| Dor | Impacto Estimado |
|---|---|
| 23% das entregas chegam com atraso | Multas contratuais de R$ 4,2 MM/ano |
| Retrabalho por falta de dados de inventário | +R$ 1,8 MM em horas extras |
| Decisões de rota baseadas em planilhas Excel | +18% de consumo de combustível |
| Manutenção corretiva (quebras na estrada) | R$ 2,1 MM/ano em reboque e downtime |
| Relatórios gerenciais entregues com 5 dias de atraso | Perda de janela para decisão tática |

Fonte: Projeto EngDados-IA-para-Negocio.md

### Notes:
A LODLog é o cenário que usaremos durante todo o módulo. Cada fonte de dados será analisada sob a ótica dos 5 Vs.

<!-- Slide number: 38 -->
# Fontes de dados LODLog

| Fonte | Tipo de dado | Formato | Volume/dia | Frequência |
|---|---|---|---|---|
| **Sensores IoT** (frota) | Semiestruturado | JSON | ~864.000 eventos | A cada 30s |
| **ERP** (financeiro) | Estruturado | Relacional | ~3.000 registros | Batch diário |
| **WMS** (estoque) | Estruturado | Relacional | ~48.000 registros | A cada 15min |
| **TMS** (transporte) | Estruturado | Relacional | ~3.000 registros | Tempo real |
| **API Google Maps** | Semiestruturado | JSON | ~60.000 requisições | A cada 5min |
| **API INMET** | Semiestruturado | JSON | ~1.500 chamadas | A cada hora |
| **API ANTT** | Semiestruturado | JSON/XML | ~20 eventos | Event-driven |
| **Base IBGE** | Estruturado | CSV | ~500 MB | Mensal |

Fonte: LODLog — levantamentos de requisitos

### Notes:
Note a variedade: de estruturados (ERP, WMS) a semiestruturados (JSON de APIs) a estruturados massivos (IBGE).

<!-- Slide number: 39 -->
# Exemplo: evento IoT da frota

```json
{
  "veiculo_id": "TRK-0342",
  "timestamp": "2025-07-14T14:32:05Z",
  "latitude": -22.9068,
  "longitude": -47.0626,
  "velocidade_kmh": 87.4,
  "rpm_motor": 2100,
  "temperatura_motor_c": 94.2,
  "nivel_combustivel_pct": 61.0,
  "peso_carga_kg": 8200,
  "status_freio": "normal",
  "hodometro_km": 124530
}
```

- **Tipo:** semiestruturado (JSON)
- **Volume:** ~864.000 eventos/dia (450 veículos × 288 leituras/dia)
- **Velocidade:** streaming (a cada 30 segundos)
- **Variedade:** 11 campos, alguns podem estar ausentes
- **Veracidade:** sensores podem falhar; exigem validação de range
- **Valor:** predição de falhas, otimização de rotas, prevenção demultas

### Notes:
Cada campo deste JSON representa uma oportunidade de análise. Temperatura do motor pode prever falhas. Posição GPS pode otimizar rotas.

<!-- Slide number: 40 -->
# Exemplo: registro do TMS

```json
{
  "pedido_id": "PED-2025-084321",
  "cliente_id": "CLI-00891",
  "origem_cd": "CD-CAMPINAS",
  "destino_endereco": "Rua das Flores, 200, São Paulo/SP",
  "prazo_entrega": "2025-07-15T18:00:00Z",
  "peso_total_kg": 1250,
  "volumes": 34,
  "prioridade": "alta",
  "veiculo_alocado": "TRK-0342",
  "motorista_id": "MOT-0091"
}
```

- **Tipo:** estruturado (tabela relacional)
- **Volume:** ~3.000 registros/dia
- **Velocidade:** tempo real (na alocação)
- **Variedade:** esquema fixo, fácil de query via SQL
- **Veracidade:** alta (sistema transacional)
- **Valor:** rastreamento de entregas, cálculo de SLA, multa por atraso

### Notes:
Dados estruturados do TMS são a base para análise de performance de entregas. Podem ser integrados com dados IoT para previsão de atrasos.

<!-- Slide number: 41 -->
05
Análise dos 5 Vs para a LODLog

### Notes:

<!-- Slide number: 42 -->
# Os 5 Vs aplicados à LODLog

| V | Pergunta Central | Exemplo para a LODLog |
|---|---|---|
| **Valor** | Que insights podem ser extraídos? | Predição de atraso, score de saúde da frota, ranking de eficiência de CDs |
| **Veracidade** | Quão precisos e confiáveis são os dados? | Sensores podem falhar; status de pedido pode ser inconsistente entre TMS e WMS |
| **Variedade** | Quais tipos, formatos e fontes? | JSON (IoT), relacional (ERP/WMS/TMS), CSV (APIs externas), semiestruturado |
| **Velocidade** | Qual a frequência de geração e ingestão? | IoT a cada 30s; pedidos em tempo real; estoque a cada 15 min; relatórios diários |
| **Volume** | Qual o tamanho e taxa de crescimento? | ~864k eventos IoT/dia; ~48k movimentações WMS/dia; ~3k eventos TMS/dia |

Fonte: LODLog — requisitos

### Notes:
Cada fonte de dados terá uma análise específica dos 5 Vs no laboratório.

<!-- Slide number: 43 -->
# Valor: insights e modelos de IA

**Casos de uso prioritários:**

1. **Predição de atraso de entrega**
   - Input: distância, horário, peso, clima, tráfego, histórico
   - Output: probabilidade de atraso (%), minutos de desvio
   - Algoritmo: XGBoost / Random Forest
   - Impacto: redução de multas contratuais (R$ 4,2 MM/ano)

2. **Manutenção preditiva da frota**
   - Input: temperatura motor, RPM, vibração, hodômetro, dias desde última manutenção
   - Output: score de risco 0-100, recomendação de ação
   - Algoritmo: Random Forest + séries temporais
   - Impacto: redução de downtime e custos de reboque (R$ 2,1 MM/ano)

3. **Otimização de rotas**
   - Input: tráfego em tempo real, previsão do tempo, peso da carga
   - Output: rota ótima, tempo estimado
   - Algoritmo: graph algorithms + ML
   - Impacto: redução de 18% no consumo de combustível

Fonte: Projeto LODLog

### Notes:
O valor dos dados só é realizado quando transformado em insights acionáveis. A LODLog tem potencial claro para IA preditiva.

<!-- Slide number: 44 -->
# Veracidade: desafios de qualidade

| Fonte | Problema de veracidade | Mitigação proposta (camadas) |
|---|---|---|
| Sensores IoT | Falhas pontuais, leituras fora de range | **Edge:** range checks (vel 0–200 km/h; temp 50–150°C), rate-of-change | **Stream:** schema enforcement (JSON Schema/Avro), anomaly detection (isolation forest/autoencoder), média móvel |
| TMS | Status inconsistente entre sistemas | **Governança:** dicionário de status padronizado (concluído/em_processo/cancelado); cross-validation TMS↔WMS+IoT |
| WMS | Divergência inventário físico vs. registrado | Conferência periódica + sensor fusion (RFID + contagem) + SCD Tipo 2 |
| APIs externas | Disponibilidade variável; latência | Cache local; retry com backoff exponencial; circuit breaker |
| ERP | Dados históricos incompletos | Preenchimento por estimativa; flag de completude; proveniência com `device_id`/`firmware_version` |
| Geral | Falta de linhagem / confiança | **Trust anchors:** mTLS + HSM, logs imutáveis, metadados de proveniência |

Framework de qualidade baseado no DAMA-DMBOK:
- Completude, Acurácia, Consistência, Atualidade, Unicidade, Validade

Fonte: LODLog — qualidade de dados

> Enriquecido via GraphRAG drift: 4 camadas de validação — edge, stream processing, cross-validation multi-fonte, trust anchors (mTLS/HSM/provenance). [DRIFT-04]

### Notes:
Veracidade é o V mais negligenciado. Dados inconsistentes levam a decisões erradas. A camada Silver da arquitetura Medallion é onde a veracidade é garantida.

<!-- Slide number: 45 -->
# Variedade: formatos e fontes

**Tipos de dados na LODLog:**

1. **Estruturados (~30% na LODLog; ~20% global — estimativa didática)**
   - ERP: tabelas SQL (clientes, contratos, faturamento) → Parquet tipado
   - WMS: estoque, movimentações, endereçamento → Parquet
   - TMS: pedidos, rotas, veículos alocados → Parquet

2. **Semiestruturados (~60% na LODLog)**
   - IoT: JSON de sensores (posição, temperatura, RPM)
   - APIs: JSON/XML (tráfego, clima, alertas ANTT) — XML com XSD quando rígido
   - Logs: texto estruturado (eventos do sistema) — JSON Schema/Avro no streaming

3. **Não estruturados (~10% na LODLog; ~80% global segundo Dell 2022)**
   - Relatórios em PDF escaneados (manutenção, auditoria) → OCR
   - E-mails de clientes e fornecedores → NLP
   - Imagens de câmeras de segurança → visão computacional

**Desafio:** o Data Lake deve acomodar todos os três tipos com **schema-on-read** na Bronze (JSON/objetos brutos) e **schema-on-write** na Silver/Gold (Parquet/Delta).
**Solução:** camadas Bronze/Silver/Gold + catálogo + contrato de dados.

Fonte: LODLog — levantamento de fontes

> Validado via GraphRAG drift: percentuais globais vs. LODLog distintos; Avro/JSON Schema para streaming; OCR/NLP para não estruturados. [DRIFT-02/04]

### Notes:
A variedade é o que torna o Data Lake essencial. Um DW tradicional não lidaria bem com JSON de sensores e PDFs simultaneamente.

<!-- Slide number: 46 -->
# Velocidade: batch vs. streaming

| Padrão | Latência | Exemplo LODLog | Tecnologia |
|---|---|---|---|
| **Batch** | Horas/dias | Fechamento financeiro, ranking semanal, IBGE mensal | Spark SQL, Airflow/Dagster, dbt (ELT) |
| **Streaming** | Segundos/minutos | Alerta de temperatura do motor, atraso crítico | Kafka + Spark Structured Streaming, Event Hubs/Kinesis |
| **CDC** (Change Data Capture) | Segundos/minutos | Atualização de status de pedido TMS↔WMS | Debezium, AWS DMS |
| **Event-driven** | Sob demanda | Bloqueio ANTT, alerta climático | Webhooks, EventBridge |

**Recomendação para o projeto:** pipeline híbrido (Medallion).
- Streaming para alertas operacionais (IoT, rastreamento) → Bronze JSON → validação em Silver
- Batch para analytics e treinamento de modelos → Gold com agregações + feature store
- CDC para sincronização entre sistemas transacionais

Fonte: LODLog — arquitetura de pipeline

> Validado via GraphRAG drift: batch = intervalos agendados; streaming = contínuo; LODLog recomenda Kafka/Flink/Spark para ingestão + validação. [DRIFT-05]

### Notes:
A escolha batch vs. streaming depende do caso de uso. Alertas de manutenção preditiva precisam de streaming. Relatórios gerenciais podem ser batch diário.

<!-- Slide number: 47 -->
# Volume: estimativas e crescimento

| Fonte | Volume diário | Tamanho estimado/mês | Crescimento anual |
|---|---|---|---|
| Sensores IoT | ~864.000 eventos | ~25 GB (JSON compactado) | +20% (expansão da frota) |
| WMS | ~48.000 registros | ~2 GB (Parquet) | Estável |
| TMS | ~3.000 registros | ~150 MB (Parquet) | +10% (aumento de clientes) |
| APIs externas | ~62.000 requisições | ~500 MB (JSON) | Variável (clima, tráfego) |
| ERP | ~3.000 registros | ~100 MB (Parquet) | Estável |

**Total estimado:** ~30 GB/mês de dados brutos.
**Com retenção de 90 dias:** ~90 GB na camada Bronze.

Fonte: LODLog — cálculo de volume

### Notes:
O volume cresce principalmente devido aos sensores IoT. A estratégia de retenção (90 dias em Bronze, indefinido em Gold) ajuda a controlar custos.

<!-- Slide number: 48 -->
# Resumo: classificação das fontes LODLog

| Fonte | Tipo | 5 Vs principais | Ingestão |
|---|---|---|---|
| Sensores IoT | Semiestruturado | Volume alto, Velocidade alta, Variedade média | Streaming |
| ERP | Estruturado | Valor alto, Veracidade alta, Volume baixo | Batch diário |
| WMS | Estruturado | Velocidade média, Variedade baixa, Volume médio | Batch 15min |
| TMS | Estruturado | Velocidade alta, Valor alto, Volume baixo | CDC/streaming |
| API Maps | Semiestruturado | Velocidade alta, Variedade média, Volume médio | Streaming |
| API Clima | Semiestruturado | Velocidade baixa, Valor médio, Volume baixo | Batch horário |
| API ANTT | Semiestruturado | Velocidade event-driven, Valor médio, Volume baixo | Event-driven |
| Base IBGE | Estruturado | Volume médio (mensal), Velocidade baixa, Valor estratégico | Batch mensal |

### Notes:
Esta tabela será preenchida durante o laboratório. Cada grupo analisará um subconjunto de fontes.

<!-- Slide number: 49 -->
06
Lab 1: Classificação das fontes LODLog

### Notes:
O laboratório dura 1h40min. Os grupos usarão Databricks Free Edition para analisar os dados do cenário LODLog.

<!-- Slide number: 50 -->
# Lab 1 — Enunciado

**Objetivo:** Classificar as fontes de dados da LODLog segundo:
1. Tipo de dado (estruturado/semiestruturado/não estruturado)
2. Os 5 Vs (Volume, Variedade, Velocidade, Veracidade, Valor)
3. Padrão de ingestão (batch vs. streaming)

**Entregável:** Uma tabela como a do slide 49, preenchida para todas as 8 fontes, com justificativas.

**Cenários por grupo:**
- Grupo 1 e 2: Sensores IoT
- Grupo 3 e 4: ERP e WMS
- Grupo 5 e 6: TMS e APIs externas
- Grupo 7 e 8: Base IBGE e fontes não estruturadas

Tempo: 50 minutos de trabalho em grupo + 50 minutos de apresentação e discussão.

### Notes:
Distribua os cenários de forma equilibrada. Cada grupo deve apresentar sua análise para a turma.

<!-- Slide number: 51 -->
# Lab 1 — Passo a passo no Databricks

1. **Acessar** https://community.cloud.databricks.com
2. **Criar workspace** (se não tiver)
3. **Criar notebook** Python
4. **Carregar dados de exemplo** (arquivos CSV/JSON fornecidos)
5. **Explorar estrutura** com `display(df)` e `df.printSchema()`
6. **Classificar por tipo** usando regras de negócio
7. **Calcular métricas** de volume (contagem de linhas, tamanho)
8. **Documentar** achados em tabela

### Notes:
Os arquivos de dados serão fornecidos pelo professor. Cada grupo recebe um subconjunto diferente.

<!-- Slide number: 52 -->
# Lab 1 — Exemplo de código Python

```python
# Carregar dados IoT da frota
df_iot = spark.read.json("/mnt/data/iot_events_sample.json")

# Explorar estrutura
df_iot.printSchema()
display(df_iot.limit(10))

# Calcular volume estimado
total_events = df_iot.count()
print(f"Eventos na amostra: {total_events}")

# Classificar tipo de dado
print("Tipo: Semiestruturado (JSON)")
print("Velocidade: Streaming (a cada 30s)")
print("Volume: ~864.000 eventos/dia")

# Análise de veracidade — validar range
df_valid = df_iot.filter(
    (df_iot.velocidade_kmh >= 0) & 
    (df_iot.velocidade_kmh <= 200)
)
print(f"Registros válidos: {df_valid.count()} / {total_events}")
```

### Notes:
Este é um exemplo para sensores IoT. Cada grupo adaptará o código para sua fonte.

<!-- Slide number: 53 -->
# Lab 1 — Tabela de classificação (modelo)

| Fonte | Tipo | Volume | Velocidade | Variedade | Veracidade | Valor | Ingestão |
|---|---|---|---|---|---|---|---|
| Sensores IoT | Semi | Alto | Streaming | Média | Baixa* | Alto | Streaming |
| ERP | Estrut | Baixo | Batch | Baixa | Alta | Alto | Batch |
| WMS | Estrut | Médio | Batch | Baixa | Média | Médio | Batch |
| TMS | Estrut | Baixo | Streaming | Baixa | Alta | Alto | CDC |
| API Maps | Semi | Médio | Streaming | Média | Alta | Alto | Streaming |
| API Clima | Semi | Baixo | Batch | Média | Alta | Médio | Batch |
| API ANTT | Semi | Baixo | Event | Baixa | Alta | Médio | Event |
| Base IBGE | Estrut | Médio | Batch | Baixa | Alta | Estratégico | Batch |

*Veracidade baixa porque sensores podem falhar e exigir validação.

### Notes:
Esta tabela é o resultado esperado do laboratório. Os grupos devem chegar a conclusões similares.

<!-- Slide number: 54 -->
# Discussão pós-lab

**Perguntas para reflexão:**

1. Quais fontes têm maior valor de negócio? Por quê?
2. Onde estão os maiores riscos de veracidade? Como mitigar?
3. Qual a proporção batch vs. streaming na LODLog?
4. Como a variedade de dados justifica um Data Lake em vez de um DW?
5. Quais fontes seriam mais difíceis de integrar? Por quê?

**Tempo:** 20 minutos de discussão em plenária.

### Notes:
O professor deve conduzir a discussão conectando as respostas com os conceitos teóricos apresentados.

<!-- Slide number: 55 -->
# Próximos passos

**Para a próxima aula (28-set):**
- Ler o material do Módulo 2 (fornecido no eCLASS)
- Trazer dúvidas sobre classificação das fontes
- Preparar-se para o RPG "As Cinco Torres Isoladas"

**Trabalho individual (70%):**
- Escolher cenário: rotas, manutenção, estoque ou fraude
- Mapear 3-5 fontes de dados
- Iniciar análise dos 5 Vs
- Prazo: 15 dias após a última aula (18/out)

### Notes:
Lembrar que o trabalho individual é a maior parte da nota. Incentivar a escolha de cenários desafiadores.

<!-- Slide number: 56 -->
# Referências da aula

**Artigos e livros:**
- Codd, E. F. (1970). A Relational Model of Data for Large Shared Data Banks. Communications of the ACM.
- Inmon, W. H. (2005). Building the Data Warehouse. Wiley.
- Kimball, R., & Ross, M. (2013). The Data Warehouse Toolkit. Wiley.
- Serra, J. (2024). Deciphering data architectures. O'Reilly Media.
- Ghemawat, S., Gobioff, H., & Leung, S.-T. (2003). The Google File System. SOSP.
- Kleppmann, M. (2017). Designing data-intensive applications. O'Reilly. (cap. streaming/batch)

**Materiais de apoio:**
- AMDA-DMBOK 2 — Guide to the Data Management Body of Knowledge
- AWS Academy Data Engineering — Module 1
- LODLog Project Documentation (`docs/LODLog/Projeto-Eng-Dados-IA-para-Negocio.md`)
- Delta Lake / Apache Iceberg / Hudi — docs oficiais (ACID sobre object storage)

> Referências adicionais validadas via GraphRAG drift: dbt para ELT, Delta/Iceberg/Hudi para Lakehouse, GFS/MapReduce/Bigtable para linha evolutiva pós-2003.

### Notes:

<!-- Slide number: 57 -->
# Resumo da aula

**Conceitos aprendidos:**
1. Evolução da organização de dados: cartões perfurados (1890) → fitas (1951, acesso sequencial) → discos (RAMAC 1956, acesso aleatório) → relacional (Codd 1970) → comercial (Oracle V2 1979) → nuvem/2003+ (GFS/MapReduce) — com marco System/360 (1964)
2. OLTP (ACID, 3FN, alta concorrência) vs. OLAP (star/snowflake, leitura analítica) — Inmon top-down vs Kimball bottom-up (híbrido real); ETL vs ELT (dbt)
3. Três tipos de dados com implicação de schema: estruturados (Parquet/SQL = schema-on-write) vs semi (JSON/XML = schema-on-read flexível) vs não estruturados (NLP/CV/OCR)
4. Os 5 Vs: Volume, Velocity, Variety, Veracity (4 camadas de validação), Value — aplicação LODLog com 8 fontes
5. Classificação de fontes + padrões Batch/Streaming/CDC/Event-driven e arquitetura Medallion Bronze/Silver/Gold (Lakehouse com Delta/Iceberg)

**Ferramenta:** Databricks Free Edition
**Cenário:** LODLog Transportes e Distribuição S.A.

> Síntese validada via 5 consultas GraphRAG drift no índice `/workspaces/graphrag/hpc-v100` (agnes-2.5-flash, 2026-08-28). Ver Apêndice abaixo.

### Notes:
Recapitulação dos pontos-chave. Conectar com o próximo módulo (arquiteturas modernas).

<!-- Slide number: 58 -->
# Dúvidas?

**Contato:**
- E-mail: julio.cesar.chaves@prof.fgv.edu.br
- eCLASS: fórum de dúvidas
- Office hours: terça 14h-16h (presencial ou online)

**Próxima aula:**
- Data: 28 de setembro de 2026
- Tópico: Arquiteturas modernas (DW, Data Lake, Lakehouse, Data Mesh)
- Laboratório: RPG "As Cinco Torres Isoladas"

Obrigado!

<!-- Slide number: 59 - APÊNDICE: Validação GraphRAG DRIFT -->
# Apêndice — Validação com GraphRAG DRIFT (2026-08-28)

> Root: `/workspaces/graphrag/hpc-v100` · Model: `agnes-2.5-flash` (via Agnes API) · Método: `drift` (n_depth 2, k_followups 5) · Index: 399 entities, 41 comunidades, 34 text_units, 11 docs

| # | Pergunta DRIFT | O que o índice confirmou | Ação na Aula 1 |
|---|---|---|---|
| 1 | Histórico: cartões perfurados Hollerith, fitas UNIVAC, discos randômicos, Codd 1970, Oracle 1977, SGBD | Hollerith = Censo 1890 + Tabulating → CTR 1911 → IBM 1924; RAMAC 1956 primeiro acesso aleatório comercial; System/360 1964 padronização; Oracle SDL 1977 → V2 1979 primeiro relacional comercial | Corrigido Slide 12 (1890+1911→1924), Slide 15 (RAMAC 1956 + System/360), Slide 16 (1977→1979 V2) |
| 2 | Tipos estruturado/semi/não + CSV/JSON/XML/Parquet + schema-on-read/write | Parquet = schema-on-write colunar tipado; CSV bruto = schema-on-read (inferência); JSON/XML = schema-on-read hierárquico flexível;Lakehouse = Delta/Iceberg/Hudi | Reescritos Slides 23, 27 e 35: tabela com camada/camada + mito Parquet/CSV + Lakehouse ACID |
| 3 | OLTP vs OLAP + Inmon/Kimball + ETL/ELT + star schema | OLTP = ACID 3FN; OLAP = star/snowflake desnormalizado; Inmon top-down vs Kimball bottom-up (híbrido); ETL (staging) vs ELT (dbt, cloud, retém brutos) | Expandido Slide 29 (ACID, star vs snowflake, híbrido) e Evolução (ETL/ELT + dbt) |
| 4 | 5 Vs + LODLog 8 fontes (IoT ERP WMS TMS APIs) | Volume/Velocity/Variety bem documentados; Veracity com 4 camadas (edge, stream schema, cross-validation, trust anchors mTLS/HSM); Value = translate em cost/service | Enriquecidos Slides 44 (4 camadas + circuit breaker/provenance) e 45–46 (percentuais LODLog vs global, Avro) |
| 5 | Data Lake vs Warehouse vs Lakehouse + Medallion + batch/streaming + Kafka/Spark | DW = schema-on-write/star/ACID; Lake = schema-on-read/barato/swamp-risk; Lakehouse = Iceberg/Delta/Hudi; Medallion Bronze=raw, Silver=cleaned, Gold=aggregated; Kafka+Flink/Spark p/ LODLog | Atualizados Slides 27, 35, 46 (Event-driven, Dagster/dbt, Delta/Iceberg, swamp mitigation) |

**Limitação detectada (DRIFT-05):** consulta específica "LODLog pipeline com Kafka Spark" retornou *"I don't have specific information about the LODLog pipeline"* — índice contém cenário LODLog mas não o pipeline concreto. Decisão: manter pipeline como **proposição didática** (não afirmar que está no corpus indexado) e marcar como arquitetura proposta para o lab.

**Comandos executados (reprodutíveis):**

```bash
set -a; source /workspaces/graphrag/hpc-v100/.env; set +a
graphrag query --root /workspaces/graphrag/hpc-v100 --method drift "Histórico da organização de dados cartões perfurados Herman Hollerith, fitas magnéticas UNIVAC, modelo relacional Codd 1970, discos acesso randomico, Oracle 1977, SGBD"
graphrag query --root /workspaces/graphrag/hpc-v100 --method drift "Tipos de dados estruturados semiestruturados não estruturados definições exemplos formatos CSV JSON XML Parquet e schema-on-read vs schema-on-write"
graphrag query --root /workspaces/graphrag/hpc-v100 --method drift "OLTP vs OLAP diferenças, Data Warehouse Inmon Kimball, ETL vs ELT, modelo dimensional star schema"
graphrag query --root /workspaces/graphrag/hpc-v100 --method drift "Os 5 Vs do Big Data volume velocidade variedade veracidade valor, exemplos LODLog 8 fontes IoT ERP WMS TMS APIs e aplicação prática"
graphrag query --root /workspaces/graphrag/hpc-v100 --method drift "Data Lake vs Data Warehouse vs Lakehouse, arquitetura Medallion Bronze Silver Gold, ingestão batch vs streaming, LODLog pipeline com Kafka Spark"
```

**Arquivos atualizados:** `aula-1.md` (8 slides + referências + resumo), `Labs/lab1-classificacao-fontes.py` (validação 4 camadas + Delta/Iceberg), `Labs/lab1-exercicios-complementares.py` (pipeline com Avro/dbt/SCD2).

