<!-- Slide number: 1 -->
# Arquitetura de Dados e Big Data
Aula 1
Tipos de dados e contexto de Big Data

### Notes:
Turma ONL023Z8-LTDLV2331

<!-- Slide number: 2 -->

![](EspaçoReservadoparaImagem2.jpg)
Boas-vindas!

### Notes:
ID da imagem: 365572922

<!-- Slide number: 3 -->
Apresentação – Professor executivo
Currículo - Júlio César Chaves
Doutorado em Engenharia Civil, COPPE/UFRJ, 2018
E-mail: julio.cesar.chaves@prof.fgv.edu.br
CV Lattes

Professor de Banco de Dados, Modelagem Informacional e Gestão e Governança de Dados (FGV/EMAp).
Graduado em Tecnologia em Informática pela UNIVERCIDADE/RJ (2006), mestre (2011) e doutor (2018) pela COPPE/UFRJ em Engenharia Civil, com foco em mobilidade urbana a partir de dados de telefonia móvel, IBGE e transportes.
20 anos como DBA, atuando na governança de infraestrutura computacional — gerindo ambientes de nuvem pública e privada e apoiando projetos de pesquisa com grandes volumes de dados e arquiteturas informacionais de maior porte.

![](Imagem8.jpg)
FOTO

### Notes:

<!-- Slide number: 4 -->
# Conteúdo
Aula 1 - Fundamentos
Plano geral
Da Contabilidade ao Big Data
Nuvem, IA e serviços para dados

01
02
03

<!-- Slide number: 5 -->
01
Plano da Disciplina

<!-- Slide number: 6 -->
# syllabus
| Aula | Data | Tópico | Atividades |
| --- | --- | --- | --- |
| 1 | 22-set | M1 — Tipos de dados e Big Data | Teoria (1h40) + Lab 1 (1h40) |
| 2 | 28-set | M2 — Ferramentas distribuídas | Teoria (1h40) + RPG (1h40) |
| 3 | 29-set | M3 — Cloud e pipelines (ETL→ELT) | Teoria (1h40) + Lab 3 (1h40) |
| 4-5 | 3-out | M4 — Miniprojeto Lakehouse | Teoria curta + Miniprojeto |

<!-- Slide number: 7 -->
# Conteúdo da Aula
01 | Breve histórico da organização de dados (validado: 1890→1956→1970→1979→2003)
02 | Tipos de dados: estruturados / semi / não + schema-on-write vs read
03 | Dado transacional (OLTP ACID) vs. analítico (OLAP star/snowflake)
04 | Os 5 Vs do Big Data (com 4 camadas de Veracidade)
05 | LODLog: 8 fontes do cenário + arquitetura Medallion
06 | Lab 1: classificação das fontes LODLog

<!-- Slide number: 8 -->
# Objetivos da Disciplina
• Compreender os diferentes tipos de dados utilizados em ambientes analíticos e de Big Data
• Gerenciar as possíveis alternativas computacionais para manuseio de dados em ambientes de Big Data
• Evidenciar os requisitos para a arquitetura analítica e processos de ingestão
• Compreender os principais componentes das arquiteturas modernas de dados (lake/warehouse/lakehouse)
• Construir um data lake/lakehouse visando a dados estruturados e não estruturados (Delta/Iceberg)
• Identificar arquiteturas de dados em ambientes cloud e distribuídos (Kafka/Spark)
• Avaliar alternativas tecnológicas para armazenamento e processamento de dados em escala

<!-- Slide number: 9 -->
# Avaliação
Disciplina isenta de prova, avaliada por trabalho

Individual (70%):
  • Sub-cenário escolhido (rotas/manutenção/estoque/fraude)
  • Fontes de dados mapeadas (mínimo 3–5)
  • Análise dos 5 Vs + 4 camadas de Veracidade
  • Arquitetura Bronze/Silver/Gold (Lakehouse Delta/Iceberg)
  • Prazo: 15 dias após a última aula

Em grupo (30%): arquitetura simplificada + apresentação/análise sobre o lake

<!-- Slide number: 10 -->
# Ferramenta do Curso: Databricks Community Edition
Ambiente gratuito para laboratórios
Notebook colaborativo baseado em Jupyter + Spark distribuído
SQL integrado + visualizações embarcadas
Formatos do lab: JSON (schema-on-read), CSV (inferência), Parquet/Delta (schema-on-write tipado)

Acesso: https://community.cloud.databricks.com
Para o miniprojeto, grupos poderão explorar créditos AWS/Azure

<!-- Slide number: 11 -->
02
Breve históricoligado a organização de dados

### Notes:

<!-- Slide number: 12 -->
Herman Hollerith — tabulador para o Censo dos EUA de 1890 --> conclusão em 30 meses, o de 1880 levou 8 anos
Tabulating Machine Company (1896) → Computing Tabulating Recording CTR (1911, fusão) → International Business Machines IBM (1924, renomeação)
Cartões = memória de códigos: padrão de furos lido por contato elétrico

A partir de 1950: mídias magnéticas; cartões declinam até discos (1960-70)

# Herman Hollerith, (1890 → 1911 → 1924)

![](Picture6.jpg)

![Ver a imagem de origem](Picture2.jpg)
Dados em um cartão perfurado?
https://www.youtube.com/watch?v=YnnGbcM-H8c
Herman Hollerith - Wikipedia, la enciclopedia libre
https://www.census.gov/about/history/stories/monthly/2016/january-2016.html , https://www.uspto.gov/learning-and-resources/journeys-innovation/historical-stories/count-me , https://www.smithsonianmag.com/smithsonian-institution/herman-holleriths-tabulating-machine-2504989/

### Notes:

<!-- Slide number: 13 -->
# Fitas magnéticas, 1951
UNIVAC I — primeiro computador comercial com fitas magnéticas como secundário
Processamento batch: leitura sequencial → gravação em nova fita

Limitação decisiva: acesso obrigatoriamente sequencial
  • Volume >> memória principal → merge manual de fitas
  • Organização física ditava a lógica do programa

Gargalo que o modelo relacional eliminaria décadas depois

.

![Foto preta e branca de menino ao lado de som Descrição gerada automaticamente](EspaçoReservadoparaConteúdo15.jpg)
1951-Magnetic-Tapes.jpeg (940×705) (goodcloudstorage.net)
Fonte: Silberschatz, A., Korth, H. F., & Sudarshan, S. (2019). Database System Concepts (7th. edition). In McGraw Hill. Pg.29.

### Notes:
UNIVAC (Universal Automatic Computer), (UNIVAC - Wikipedia), precedido pelo ENIAC e sucedido pela UNYSIS
Iniciou as atividades em 1951 e foi descontinuada em 1986

<!-- Slide number: 14 -->
# Paul Allen (15) e Bill Gates (13) na Universidade de Washington em 1968

![Ver a imagem de origem](Picture2.jpg)

![](Picture4.jpg)
Paul Allen (15) e Bill Gates (13) fizeram um programa em Fortran cujo objetivo era ler dados brutos de contagem de tráfego e gerar um relatório para os engenheiros de transporte. O feito deu origem à empresa Traf-O-Data, o primeiro nome da Microsoft.
A menção à Microsoft é meramente ilustrativa, pois diversos programadores fizeram trabalhos similares. Mesmo que de forma geral o padrão estabelecido era de que grandes empresas eram contratadas para essa finalidade, tal como a IBM.
Microsoft founders Bill Gates(13) and Paul Allen(15) connect to a PDP-10 computer at the University of Washington, through a teletype terminal at their Lakeside School in Seattle in 1968 - [1895x1293] : HistoryPorn (reddit.com)
Traf-O-Data – Wikipedia Early Days as a Computer Programmer | Bill Gates (gatesnotes.com)

### Notes:
Na ocasião, os dados eram recebidos em “fitas perfuradas”

<!-- Slide number: 15 -->
# O matemático Edgar F. Codd, 1970, e o modelo relacional
Na era inicial da mídia magnética, os bancos de dados seguiam o modelo hierárquico e em rede, onde era necessário levar em conta as organizações internas dos arquivos dos bancos de dados, sob um complexo sistema de ponteiros.
Nesse contexto, Codd fez uma conexão entre conceitos matemáticos e organização de dados que viria a mudar a forma de lidar com bancos de dados, e que é largamente usada até hoje.
Na primeira frase de seu artigo “A Relational Model of Data for Large Shared Data Banks”, Codd levanta uma crítica ao sistema de banco de dados da época:
“Future users of large data banks must be protected from having to know the data is organized in the machine (the internal representation).”
Além do conceito de “relação” de conjuntos que deu origem ao modelo relacional, Codd propôs uma linguagem de alto nível, que permitisse a declaração das relações entre os conjuntos e seus domínios, e que, basicamente deu origem à linguagem SQL.

![Ver a imagem de origem](Picture2.jpg)
Fórum Técnico: La batalla por las bases de datos (forumtecnico.com)
A História das Bases de Dados - O Início - Pplware (sapo.pt)

Relational database - Wikipedia
Important Papers: Codd and the Relational Model (twobithistory.org)
A História das Bases de Dados - Os SGBD Relacionais Mais Marcantes #1 (sapo.pt)
A relational model of data for large shared databanks (uwaterloo.ca)

### Notes:
“Futuros usuários de grandes bancos de dados devem ser protegidos de saber que os dados estão organizados na máquina (a representação interna).”

Edgar F. Codd — IBM Research — 'A Relational Model of Data for Large Shared Data Banks'

Ideia central: proteger o usuário da organização interna (independência física/lógica)
Conexão teoria dos conjuntos ↔ organização de dados + linguagem → origem do SQL

Citação: 'Future users of large data banks must be protected...'
Primeiro SGBD comercial: Oracle V2 (1979) — SDL fundada em 1977

<!-- Slide number: 16 -->
# Discos rígidos e o acesso randômico, anos 70
Consequência para a engenharia de dados
- A posição física do dado deixou de importar.
- Programadores passaram a construir estruturas de dados abstraindo questões de hardware.
- Isso viabilizou, anos depois, o modelo relacional de Codd: só faz sentido exigir independência física/lógica quando o hardware já permite acessar qualquer registro diretamente.
O primeiro protótipo (1952) continha 50 discos de 24" e armazenava 5 milhões de caracteres. O conceito só se popularizou no fim dos anos 60 e 70, quando o hardware tornou-se acessível.
Por que isso mudou tudo?
Diferente das fitas magnéticas, os discos permitiam acesso direto e randômico ao dado — não era mais necessário percorrer sequencialmente toda a fita para chegar a um registro.

![](Picture2.jpg)
Computer History Displays - The University of Auckland - Historydisplays - FifthFloor - MagneticDataStorage
Fonte: Silberschatz, A., Korth, H. F., & Sudarshan, S. (2019). Database System Concepts (7th. edition). In McGraw Hill. Pg.29.

### Notes:
Fonte: Silberschatz, Korth & Sudarshan (2019), p. 29.

    Notes:
    - Contraste explícito com slide 12 (fitas = sequencial) e slide 18 (Codd = independência lógica/física).
    - Curiosidade pessoal: "Fiz o segundo grau num curso de nome 'Processamento de Dados'".
    - Tempo: 2 minutos. É ponte histórica, não aprofundamento técnico.

<!-- Slide number: 17 -->
# Bob Miner, Ed Oates, Bruce Scott e Larry Ellison em 1977-1979
SDL (Software Development Laboratories) fundada 1977 por Miner/Oates/Scott/Ellison
Cliente inicial: Força Aérea dos EUA
Produto: Oracle V2 (1979) — primeiro SGBD relacional comercial com SQL

Antes: empresas cuidavam manualmente de arquivos/transações
Depois: foco nos requisitos de negócio; SGBD cuida de concorrência/armazenamento

Informalmente, através de reuniões com a Oracle, conta a história que ninguém acreditava que seria possível a materialização da teoria de Codd, muitos tentaram e abandonaram o projeto, exceto Larry Ellison, que perseverou e tornou-se um visionário na época.

![Ed Oates Bruce Scott Bob Miner Larry Ellison](Picture4.jpg)
Life after Larry may be coming, but it's not here yet for Oracle (diginomica.com)
A História das Bases de Dados - O Início - Pplware (sapo.pt)
Relational database - Wikipedia
Important Papers: Codd and the Relational Model (twobithistory.org)

História da Oracle (devmedia.com.br)
IBM não acreditou no modelo relacional  -  The early history of databases and DB2 – DataGeek.blog
A História das Bases de Dados - Os SGBD Relacionais Mais Marcantes #1 (sapo.pt)
A relational model of data for large shared data banks (uwaterloo.ca)

### Notes:

<!-- Slide number: 18 -->
# Banco de dados e SGBDarquitetura típica
Acesso direto vs indireto
Execução de comandos DDL e DML
Criação de banco de dados

![](Picture3.jpg)
Manutenção e administração de banco de dados
Gestão interna de recursos de CPU, memória e disco
Gestão de acesso concorrente
Fonte: Jukic, N., Vrbsky, S., Nestorov, S., & Sharma, A. (2021). Database Systems: An Introduction to Databases and Data Warehouses. Copyright Prospect Press.

Copyright (c) 2020 Nenad Jukic and Prospect Press

### Notes:
Tipicamente esta é a arquitetura de um sgbd - sistema gerenciamento de banco de dados, uma tradução de DBMS – database management system.
O sgbd é uma camada de software que faz a gestão dos bancos de dados. Essa camada permite a execução de algumas operações, tais como:
criação exclusão de bancos de dados,
execução de comandos DDL - data definition language e DML - data manipulation language, (todos estão familiarizados com essas siglas?),
manutenção e administração de bancos de dados,
gestão interna de recursos de CPU, memória e disco,
questão de acesso concorrente, identidade e acesso.
As aplicações não se conectam diretamente ao banco de dados, mas sim ao sgbd, para gestão de identidade e acesso.
Os usuários podem realizar operações através de interações diretas, conectando-se diretamente ao sgbd, ou interações indiretas, através das aplicações.
Imaginemos a diferença entre trabalhar com dados em um arquivo Excel e um banco de dados em um sgbd. O que acontece ao tentar abrir uma planilha muito grande? o que acontece se mais de uma pessoa precisa usar a planilha ao mesmo tempo?

<!-- Slide number: 19 -->
# Informação transacional vs informação analítica

![Interface gráfica do usuário Descrição gerada automaticamente com confiança média](Imagem4.jpg)
Transacional (Operacional)
Registra o fato no momento em que ele acontece
Suporta processos do dia a dia
Responde: "O que aconteceu?"
Analítica (Decisão)
Agrega fatos históricos para revelar padrões
Suporta planejamento estratégico
 Responde: "Por que aconteceu? E o que vai acontecer?"
Fonte: (www)

### Notes:
Uma organização lida com diversas fontes de dados
Tipicamente, o mesmo fato pode ter tanto uma proposta operacional quanto analítica.
Por exemplo, o dado descrevendo que o cliente X comprou o produto Y na loja Z pode ser armazenado em um banco de dados operacional para suportar os processos de negócio, tal como monitor o estoque ou a realização de transações financeiras. O mesmo fato pode também ser armazenado em um DW, aonde o mesmo fato pode ser combinado com um vasto número de fatos similares acumulados em um período de tempo, e isso pode servir para revelar tendências importantes tais como padrões de venda ou comportamento do consumidor.
Vemos na figura alguns exemplos de informações que são coletadas no dia-a-dia (esquerda). Se estes registros de transações forem processados com uma determinada finalidade, podem ser usados para suporte à decisões gerenciais
Transacional – recibos de compra e venda, passagem de avião, recibo de entrega
Analítica – estatísticas de produtos, projeção de vendas, crescimento futuro, tendências
O termo informação analítica remete às informações agregadas, calculadas e processadas para alguma finalidade.
Se passar o cartão no metrô da Glória é uma transação, então inferir a mobilidade urbana da população do Rio de Janeiro a partir do banco de dados contendo os dados de todas as catracas de todas as estações do metrô, por exemplo, é uma informação analítica.
Tipicamente o uso operacional fica apartado do uso analítico, essa á a recomendação devido ao isolamento transacional

<!-- Slide number: 20 -->
# Bill Inmon e Ralph Kimball nos anos 90
Dois profissionais com larga experiência em banco de dados tornaram-se referência defendendo a tese de que a análise de dados demandava por uma organização informacional distinta do modelo que atendia plenamente as necessidades transacionais: esquema estrela (Kimball) e Data Warehouse estruturado (Inmon).

A demanda por relatórios era atendida através da leitura direta dos bancos de dados transacionais, impactando a performance operacional e não atendendo plenamente a necessidade analítica.

Inovação: Estabelecer conceitos que iriam guiar o mercado na jornada de análise de dados.
Requisitos/condições: papel, caneta e um extenso background corporativo.

Resultado esperado: As empresas possuírem um ambiente analítico modelado (DW) que é apartado do ambiente transacional.

![Ver a imagem de origem](Picture2.jpg)

![](EspaçoReservadoparaConteúdo5.jpg)
Interview – Bill Inmon, Father of Data Warehouse (analyticsindiamag.com)
A Short History of Data Warehousing - DATAVERSITY

<!-- Slide number: 21 -->
# Data Warehouse (DW)
Um data warehouse é um repositório estruturado e integrado composto por:
Dados orientados para assuntos, através do modelo dimensional.
Dados que abrangem toda a companhia,
Dados históricos que possuem vários instantes de tempo.

Os componentes de um DW são:
O próprio Data Warehouse - um repositório de dados em um SGBD.
O ETL (Extract Transform Load) - que tem a função de ler, transformar e carregar os dados a partir das fontes para o destino, o DW.
Aplicações de front-end - que permitem o acesso indireto dos usuários ao DW, tal qual ferramentas de visualização.

Definição e Exemplos de Data Warehouse | Astera

<!-- Slide number: 22 -->
# DATA WAREHOUSE

![](Picture3.jpg)
Jukić, Vrbsky, Nestorov, Sharma – Database Systems – Copyright Nenad Jukic and Prospect Press
Chapter 10 – Slide  22

### Notes:
This example is discussed on Pages 328-329.

<!-- Slide number: 23 -->
# OLTP vs. OLAP
| Característica | OLTP (transacional) | OLAP (analítico) |
| --- | --- | --- |
| Objetivo | Registrar transações (ACID) | Responder perguntas de negócio |
| Modelo | 3FN normalizado | Star/Snowflake desnormalizado (Kimball vs Inmon) |
| Queries | INSERT/UPDATE/DELETE rápidos | SELECT + GROUP BY + JOIN (milhões) |
| Volume | Milhões/hora, alta concorrência | Scans sobre histórico longo |
| Ferramentas | PostgreSQL, MySQL, Oracle | Redshift, BigQuery, Databricks SQL, Snowflake |
| Usuários | Sistema, operadores | Analistas, dashboards, ML |

<!-- Slide number: 24 -->
# Inmon vs Kimball & ETL → ELT
Inmon (top-down): EDW 3FN central → data marts (consistência, custo alto inicial)
Kimball (bottom-up): star marts + dimensões conformadas → EDW lógico (valor rápido, requer coordenação)
Prática: híbrido com busway dimensional

Snowflake = dimensões normalizadas (economiza espaço, mais JOINs);
Star = padrão por performance

ETL = transform antes do load (staging dedicado, on-prem)
ELT = load direto no warehouse/lakehouse + transform dentro (elasticidade cloud, retém brutos)
Inmon, W. H. Building the Data Warehouse. 4th ed. Wiley, 2005. (Obra fundadora da abordagem top-down; define DW como "subject-oriented, integrated, time-variant, non-volatile collection of data".)
Kimball, Ralph; Ross, Margy. The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling. 3rd ed. Wiley, 2013. (Referência central da abordagem bottom-up, dimensional; define dimensões conformadas e a "enterprise data warehouse bus architecture/matrix".)

<!-- Slide number: 25 -->

![](EspaçoReservadoparaConteúdo7.jpg)
#

### Notes:
Inmon (top-down)
Correto: Inmon define o Data Warehouse corporativo (EDW) como um repositório centralizado, integrado, normalizado (3FN), construído primeiro a partir de uma visão corporativa dos dados.
Os data marts são derivados do EDW depois, geralmente departamentais e dimensionais, alimentados a partir do repositório central.
Vantagens: alta consistência e integridade dos dados (única fonte da verdade), já que tudo passa pelo modelo normalizado antes de virar mart.
Desvantagens: custo e tempo iniciais altos, pois exige modelar toda a empresa antes de entregar valor aos usuários finais.
Kimball (bottom-up)
Correto: Kimball parte da construção de data marts dimensionais (esquemas estrela/floco de neve) voltados a processos de negócio específicos.
A integração entre os marts ocorre por meio de dimensões conformadas (conformed dimensions) — dimensões compartilhadas com a mesma estrutura/chaves entre os marts, permitindo consultas cruzadas.
O conjunto de marts interligados por essas dimensões formam o que ele chama de "EDW", mas de forma lógica/federada, não um repositório único normalizado.
Vantagens: valor de negócio mais rápido (entrega incremental, mart por mart).
Desvantagens: exige forte governança e coordenação do barramento de dimensões conformadas (bus matrix) para evitar inconsistências entre os marts ao longo do tempo.
Sua formulação está tecnicamente alinhada com a literatura padrão da área.
Referências para citar:
Inmon, W. H. Building the Data Warehouse. 4th ed. Wiley, 2005. (Obra fundadora da abordagem top-down; define DW como "subject-oriented, integrated, time-variant, non-volatile collection of data".)
Kimball, Ralph; Ross, Margy. The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling. 3rd ed. Wiley, 2013. (Referência central da abordagem bottom-up, dimensional; define dimensões conformadas e a "enterprise data warehouse bus architecture/matrix".)
Kimball, Ralph; Ross, Margy; Thornthwaite, Warren; Mundy, Joy; Becker, Bob. The Kimball Group Reader: Relentlessly Practical Tools for Data Warehousing and Business Intelligence. 2nd ed. Wiley, 2016. (Coletânea de artigos que detalham a bus matrix e a integração entre marts.)
Kimball Group — artigo "Differences of Opinion" (kimballgroup.com), no qual Kimball e Inmon debatem publicamente as diferenças entre as duas abordagens — ótima fonte primária para contrastar os dois métodos em sala de aula.
Golfarelli, Matteo; Rizzi, Stefano. Data Warehouse Design: Modern Principles and Methodologies. McGraw-Hill, 2009. (Boa fonte acadêmica secundária que compara e contextualiza as duas arquiteturas de forma neutra.)
Inmon, W. H.; Strauss, Derek; Neushloss, Genia. DW 2.0: The Architecture for the Next Generation of Data Warehousing. Morgan Kaufmann, 2008. (Evolução da visão de Inmon, útil se o curso cobrir arquiteturas mais recentes.)

<!-- Slide number: 26 -->
# NASA & Big Data
Primeiro uso 'Big Data': Cox & Ellsworth, 1997 (visualização de datasets grandes)
NASA: 12.1 TB/dia de ~100 missões ativas; picos de 24 TB/dia
Challenge: handling, storing, managing em escala

![](Imagem11.jpg)
Do you know that the term “big data” was first used in a 1997 paper by scientists at NASA, describing an interesting challenge, they had with visualizing the large datasets? The volume of data NASA has to manage is mind-boggling. According to Kevin Murphy, NASA Program Executive for Earth Science Data Systems, NASA – one of the biggest generators of data – is generating 12.1TB of data every single day from nearly 100 currently active missions and thousands of sensors and systems around the Earth and space. Some missions could generate as much as 24TB in a single day. Handling, storing, and managing this data is a massive challenge.
https://crayondata.ai/how-does-nasa-use-big-data/
Primeiro uso do termo “Big Data”: M. Cox and D. Ellsworth, “Application-controlled demand paging for out-of-core visualization,” Proc. IEEE Vis. Conf., pp. 235–244, 1997, doi: 10.1109/visual.1997.663888.

### Notes:
|Slide number 26
|Instructor notes
|The goal of this section is to highlight each characteristic, how they intertwine, and the trade-offs involved in making design decisions. Generally it's value first, and then volume/velocity variety/veracity as pairs.
|
|Student notes
The five Vs are volume, velocity, variety, veracity and value.

Consider volume and velocity together because you will make infrastructure decisions about how to collect, store, and process data based on the combination of how much data you need to ingest and how quickly you will ingest it.

Variety and veracity both relate to the data itself—what type of data is it and what's the quality of it. Data engineers and data scientists will transform and organize the data based on its variety and veracity to make it useful for analysis.

Value is about ensuring that you are getting the most out of the data that you have collected. Value is also about ensuring that there is business value in the outputs from all that collecting, storing, and processing.

<!-- Slide number: 27 -->
# Big Data: atingindo os “limites atuais”

Volume

Velocidade

Variedade

Veracidade

Valor

![preencoded.png](Image0.jpg)

![preencoded.png](Image1.jpg)

![preencoded.png](Image2.jpg)

![preencoded.png](Image3.jpg)

![preencoded.png](Image4.jpg)
Qual é o tamanho do conjunto de dados?
Com que frequência novos dados são gerados e ingeridos?
Quais tipos e formatos? De quantas fontes diferentes vêm os dados?
Quão exatos, precisos e confiáveis são os dados?
Quais insights podem ser extraídos dos dados?
2.5 Quintilhões
40.000 GB
80%
1 em cada 3
R$ 430 bi
de bytes criados por dia no mundo
de dados gerados por segundo globalmente
dos dados do mundo são não estruturados
líderes empresariais não confiam em seus dados
de valor gerado pelo Big Data até 2028

<!-- Slide number: 28 -->
# Os 5 Vs em Detalhes (1/2)
VOLUME — ~864k eventos IoT/dia (450 × 288) → ~30 GB/mês brutos
  Decisão: particionamento por data + compressão (Parquet) + retenção 90d Bronze

VELOCITY — IoT a cada 30s; TMS tempo real; WMS 15min; ERP diário
  Decisão: híbrido streaming (alertas) + batch (analytics) + CDC/Event-driven

VARIETY — JSON (IoT), SQL (ERP), CSV (IBGE), XML (ANTT), Parquet (Silver)
  Decisão: Bronze schema-on-read (JSON bruto) → Silver/Gold schema-on-write (Delta)

<!-- Slide number: 29 -->
# Os 5 Vs em Detalhes (2/2)
VERACITY — 4 camadas: Edge (Validação na origem) → Stream (Checagem em tempo real) → Cross (Cruzamento de fontes) → Trust (Segurança e rastreio)
  Decisão: validação na zona Silver; Silver é onde veracidade é garantida (DAMA-DMBOK: completude, acurácia...)

VALUE — predição de atraso (R$4.2M multas), manutenção (R$2.1M), rota (18% combustível)
  Decisão: priorizar casos de uso com ROI medido

Interligação: variedade alta → risco veracidade; valor justifica custo dos 4 Vs

### Notes:
VERACITY — 4 camadas: Edge (range/rate/duplicate) → Stream (JSON Schema/Avro + isolation forest) → Cross (sensor fusion) → Trust (mTLS/HSM/provenance)
  Decisão: validação na Silver; Silver é onde veracidade é garantida (DAMA-DMBOK: completude, acurácia...)

VALUE — predição de atraso (R$4.2M multas), manutenção (R$2.1M), rota (18% combustível)
  Decisão: priorizar casos de uso com ROI medido

Interligação: variedade alta → risco veracidade; valor justifica custo dos 4 Vs

<!-- Slide number: 30 -->
# Classificação dos Dados por Tipo
| Tipo | Descrição (schema) | Exemplos LODLog | Formatos |
| --- | --- | --- | --- |
| Estruturados | Esquema fixo (schema-on-write) | ERP/WMS/TMS → Parquet tipado | SQL tables, Parquet (int32/float/date...), CSV+DDL |
| Semi | Tags/hierarquia flexível (schema-on-read) | IoT JSON, APIs XML/JSON, logs | JSON, XML, YAML (+ XSD/JSON Schema) |
| Não estrut. | Sem esquema (NLP/CV/OCR) | PDFs manutenção, imagens CD, e-mails | Texto, imagem, vídeo, áudio, PDF |

<!-- Slide number: 31 -->
# Dados Não Estruturados — Custo e Técnica
Exemplos LODLog: PDFs escaneados (OCR), imagens CD (visão computacional), transcrições (NLP), e-mails (classificação)
Sem esquema; extração exige IA → custo maior, valor potencial alto
Armazenamento: Data Lake objetos brutos + catálogo; sem governança = data swamp
Mitigação: camada de metadados Lakehouse (Delta Lake / Iceberg / Hudi) com ACID + time-travel

### Notes:
Ferramentas: Tesseract OCR, spaCy/transformers, YOLO/CLIP

<!-- Slide number: 32 -->
# Larry Page e Sergey Brin em Stanford em 1998
1998: PageRank — ranqueia por quantidade/qualidade de links (Stanford)

Análise ainda confinada a DWs corporativos
2003: Google File System (GFS) — grid com hardware commodity (2003)

Na sequência: MapReduce (2004) + Bigtable (2006) → padrão para escala a baixo custo

Inovação: arquitetura para Big Data já descrito por Cox/Ellsworth (NASA, 1997)

![](Picture2.jpg)
History of Google - Wikipedia
Google File System - Wikipedia
Fonte: (1) M. Cox and D. Ellsworth, “Managing Big Data for Scientific Visualization,” ACM Siggraph, vol. 97, no. January 1997, pp. 1–17, 1997, [Online]. Available: http://www.dcs.ed.ac.uk/teaching/cs4/www/visualisation/lectures/98-99/lect16ref.ps.gz.

<!-- Slide number: 33 -->
# DATA LAKE - um conceito adequado para lidar com Big Data

![](Picture7.jpg)
Jukić, Vrbsky, Nestorov, Sharma – Database Systems – Copyright Nenad Jukic and Prospect Press
Chapter 10 – Slide  33

### Notes:
This example is discussed on Pages 328-329.

<!-- Slide number: 34 -->
# Data Lake — Conceito (com swamp alert)
Repositório em formato nativo: estruturados + semi + não (sem pré-processamento)
Características:
  • Schema-on-read (ingestão rápida sem validação prévia)
  • Object storage barato (S3) + retenção longa
  • Escalabilidade horizontal + multi-formato simultâneo

Risco: sem catálogo/governança → data swamp
Resposta: Lakehouse com Delta/Iceberg/Hudi (ACID, time-travel, schema enforcement)

<!-- Slide number: 35 -->
# Breve história da computação na nuvem

![Virtualization changes everything](Picture2.jpg)
| Época | Marco | O que mudou |
| --- | --- | --- |
| Anos 50 | Mainframes compartilhados | CPU e armazenamento divididos entre terminais distintos — primeiro compartilhamento de recursos |
| Anos 70 | IBM VM (virtualização) | Múltiplos sistemas virtuais num mesmo servidor físico — computadores distintos dentro de uma mesma máquina |
| Anos 90–2000 | Virtualização + Internet | Hospedagem compartilhada on-line otimiza o uso de recursos; surgem os primeiros provedores de infraestrutura |
"The Network Is the Computer" — Sun Microsystems, John Gage (Reiss 1996)
A Brief History of Cloud Computing | IBM
(www) (www)

### Notes:
Assim nasce a nuvem

Ao instalar e configurar um software chamado hypervisor em vários nós físicos, pode-se usar todos os recursos do ambiente como se esses recursos estivessem em um único nó físico.
Para visualizar esse ambiente, os tecnólogos usaram termos como “computação utilitária” e “computação em nuvem”, já que a soma das partes parecia uma bolha nebulosa de recursos de computação que você poderia segmentar conforme necessário (como as empresas de telecomunicações fizeram na década de 1990). Nesses ambientes de computação em nuvem, era fácil adicionar recursos à “nuvem” – adicionar outro servidor ao rack e configurá-lo para fazer parte do sistema maior.

À medida que as tecnologias e os hipervisores melhoraram ao compartilhar e fornecer recursos de maneira confiável, muitas empresas empreendedoras decidiram dividir o ambiente maior. Eles queriam disponibilizar os benefícios da nuvem para usuários que não tinham muitos servidores físicos disponíveis para criar sua própria infraestrutura de computação em nuvem. Esses usuários podem solicitar “instâncias de computação em nuvem” (também conhecidas como “servidores de nuvem”) solicitando os recursos necessários do conjunto maior de recursos de nuvem disponíveis. Como os servidores já estavam online, o processo de “ligar” uma nova instância ou servidor é quase instantâneo. Como há pouca sobrecarga para o proprietário do ambiente de computação em nuvem quando uma nova instância é solicitada ou cancelada (já que é tratada pelo software da nuvem), o gerenciamento do ambiente é muito mais fácil.
 Notes:
    - Três marcos: compartilhamento (50), virtualização (70), internet + comercialização (90/2000).
    - Não detalhar hypervisor aqui — é o foco do slide 32 ("Nasce a nuvem").
    - Destacar a analogia da "computação utilitária": você não gera sua própria eletricidade, contrata o que consome.
    - Gancho slide 32: "Mas como isso funciona na prática? Entra o hypervisor."
    - Tempo: 2 minutos. É contextualização histórica, não aula de infraestrutura.

<!-- Slide number: 36 -->
# Modelo on-premises (em local próprio)

![](Imagem3.jpg)
Paga-se por “onde se pode chegar”
O custo das aquisições está conectado a capacidade máxima do ambiente, o pico teórico. Mesmo que esse pico nunca chegue, o custo já foi mobilizado.
Obsolescência
Ocorre amortização de equipamento de informática em 5 anos.
Necessário atentar para suporte e reposição de peças, pois os modelos ficam obsoletos.
Manutenção e gestão
A empresa precisa manter equipes distintas e especializadas para as diferentes camadas de infraestrutura: sistemas operacionais, bancos de dados, redes, servidores, virtualização, etc.
Differences and advantages of a On-Premise CRM and On-Demand CRM (efficy.com)

### Notes:

<!-- Slide number: 37 -->
# Modelo em nuvem

![](Imagem4.jpg)
Paga-se pelo que for usado
O custo dos serviços está conectado diretamente ao uso realizado.
Obsolescência
O provedor de nuvem é responsável pelo suporte e reposição de peças, gerindo a obsolescência.
Manutenção e gestão
A empresa precisa manter analistas qualificados para gestão de serviços e sistemas utilizados pela área de negócio, desonerando funções mais ligadas a artefatos físicos.
Differences and advantages of a On-Premise CRM and On-Demand CRM (efficy.com)

### Notes:

<!-- Slide number: 38 -->
# Aquisições on-premise são embasadas em pico teórico.Aquisições na nuvem, sob demanda(*).

![Cartoon of hot servers and a thermometer showing a hot temperature.](Picture1.jpg)

![](Picture8.jpg)

![](Picture7.jpg)

![Cartoon of servers.](Picture5.jpg)

![A thermometer showing a cold temperature.](Picture2.jpg)
Capacidade do servidor superestimada
Escalabilidade sob demanda
Capacidade do servidor subestimada

![](Picture4.jpg)
(*) Desde que devidamente configurada.
© 2019 Amazon Web Services, Inc. ou suas afiliadas. Todos os direitos reservados.

### Notes:
Vantagem 3 – Pare de tentar adivinhar a capacidade: pare de tentar adivinhar quanta capacidade de infraestrutura é necessária. Quando você toma uma decisão de capacidade antes de implantar um aplicativo, muitas vezes tem recursos ociosos caros ou lida com capacidade limitada. Com a computação em nuvem, esses problemas são resolvidos. Você pode acessar a quantidade que quiser e ajustar a escala conforme a necessidade em poucos minutos.

<!-- Slide number: 39 -->
# Modelo de serviço em nuvem
PaaS
(Plataforma como serviço)
SaaS
(Software como serviço)
IaaS
(Infraestrutura como serviço)

Mais controle sobre os recursos de TI
Menos controle sobre os recursos de TI

![](Imagem15.jpg)
© 2019 Amazon Web Services, Inc. ou suas afiliadas. Todos os direitos reservados.

### Notes:
Existem três modelos principais de serviços em nuvem. Cada modelo representa uma parte diferente da pilha de computação em nuvem e oferece um nível diferente de controle sobre seus recursos de TI:

Infraestrutura como serviço (IaaS): os serviços nesta categoria são os componentes básicos da TI em nuvem e, geralmente, fornecem acesso (virtual ou no hardware dedicado) a recursos de rede e computadores, bem como espaço para o armazenamento de dados. A IaaS oferece o mais alto nível de flexibilidade e controle de gerenciamento sobre seus recursos de TI. É o modelo mais semelhante aos recursos de TI existentes com os quais muitos departamentos e desenvolvedores de TI já estão familiarizados.

Plataforma como serviço (PaaS): os serviços nessa categoria reduzem a necessidade de gerenciar a infraestrutura subjacente (geralmente hardware e sistemas operacionais) e permitem que você se concentre na implantação e no gerenciamento de seus aplicativos.

Software como serviço (SaaS): os serviços nesta categoria fornecem um produto completo que o provedor de serviços executa e gerencia. Na maioria dos casos, o software como serviço refere-se a aplicativos de usuário final. Com uma oferta de SaaS, não é necessário pensar na manutenção do serviço ou no gerenciamento da infraestrutura subjacente. É necessário pensar apenas em como você planeja usar esse software específico. Um exemplo comum de aplicação do SaaS é o webmail, no qual você pode enviar e receber e-mails sem precisar gerenciar recursos adicionais para o produto de e-mail nem manter os servidores e sistemas operacionais no qual o programa de e-mail está sendo executado.

<!-- Slide number: 40 -->
# Modelos de serviço — onde cada um normalmente opera no pipeline
IaaS
(Infraestrutura): máquinas virtuais, redes, storage → usado para alimentar (ingestão) e armazenar (Data Lake).
PaaS
(Plataforma): bancos gerenciados, serviços de ETL, Kafka/Kinesis → usado para transformar (processamento).
SaaS
(Software): BI, dashboards, APIs prontas → usado para disponibilizar (consumo).

<!-- Slide number: 41 -->
# LODLog Transportes e Distribuição S.A.
Logística — Campinas/SP, fundada em 2010
  • 450 veículos (leves/médios/pesados)  • 12 CDs no Brasil
  • 3.200 clientes (varejo/indústria)  • ~18.000 entregas/mês  • R$380M faturamento

Problema: 'Sabemos que estamos perdendo dinheiro, mas não sabemos onde nem por quê.'

<!-- Slide number: 42 -->
# LODLog — Dores de Negócio

| Dor | Impacto Estimado |
| --- | --- |
| 23% entregas com atraso | R$ 4,2 MM/ano em multas |
| Retrabalho por falta de inventário | +R$ 1,8 MM horas extras |
| Rotas em planilhas Excel | +18% combustível |
| Manutenção corretiva (quebras) | R$ 2,1 MM/ano reboque/downtime |
| Relatórios com 5 dias de atraso | Perda de janela tática |

<!-- Slide number: 43 -->
# Fontes de Dados LODLog (8 fontes)

| Fonte | Tipo | Formato | Volume/dia | Frequência |
| --- | --- | --- | --- | --- |
| Sensores IoT | Semi | JSON | ~864k eventos | 30s (streaming) |
| ERP | Estrut | Relacional | ~3k reg | Batch diário |
| WMS | Estrut | Relacional | ~48k reg | 15min (batch) |
| TMS | Estrut | Relacional | ~3k reg | Tempo real (CDC) |
| API Google Maps | Semi | JSON | ~60k req | 5min (streaming) |
| API INMET | Semi | JSON | ~1.5k | Horário (batch) |
| API ANTT | Semi | JSON/XML | ~20 eventos | Event-driven |
| Base IBGE | Estrut | CSV | ~500 MB | Mensal (batch) |

<!-- Slide number: 44 -->
# Exemplo: Evento IoT da Frota (JSON)
Tipo: Semiestruturado (JSON, schema-on-read) — campos podem faltar
Campos: veiculo_id, timestamp, lat/lon, velocidade_kmh, rpm, temp_motor_c, nivel_combustivel_pct, peso_carga_kg, hodometro_km
5 Vs: Volume 864k/d · Velocity 30s streaming · Variety JSON variável · Veracity sensores falham → 4 camadas validação · Value predição/rotas
Armazenamento: Bronze JSON bruto (S3) → Silver Delta validado → Gold agregação/veículo/hora

<!-- Slide number: 45 -->
# Exemplo: Registro TMS (estruturado)
TMS = Transportation Management System (Sistema de Gestão de Transportes).

Tipo: Estruturado (schema fixo; JSON com schema ou tabela) → Silver Parquet (schema-on-write)
Campos: pedido_id, cliente_id, origem_cd, destino_endereco, prazo_entrega, peso_total_kg, volumes, prioridade, veiculo_alocado, motorista_id
5 Vs: Volume 3k/d (baixo) · Velocity tempo real (CDC) · Variety baixa (esquema fixo) · Veracity alta (transacional, mas cross-check com WMS) · Value SLA/multas

<!-- Slide number: 46 -->
# Valor: Casos de Uso de IA (LODLog)
1. Predição de atraso: input distância/horário/peso/clima/tráfego/histórico → output prob. atraso + desvio min (XGBoost/RF) → -R$4.2M multas
2. Manutenção preditiva: temp/RPM/vibração/hodômetro/dias última manutenção → score risco 0-100 (RF + séries) → -R$2.1M downtime
3. Otimização de rotas: tráfego real + clima + peso → rota ótima (graph algorithms + ML) → -18% combustível

<!-- Slide number: 47 -->
# Veracidade: Camadas de Validação
| Fonte | Problema | Mitigação (camadas) |
| --- | --- | --- |
| IoT | Falhas, fora de range | Edge: range 0-200km/h, 50-150°C, rate, duplicate | Stream: JSON Schema/Avro, isolation forest, média móvel |
| TMS/WMS | Status inconsistente | Dicionário padronizado + cross-validation TMS↔WMS+IoT + SCD Tipo 2 |
| APIs | Disponibilidade/latência | Cache + retry backoff exponencial + circuit breaker |
| ERP | Histórico incompleto | Flag completude + estimativa + provenance (device/fw version) |
| Geral | Linhagem/confiança | Trust anchors: mTLS/HSM, logs imutáveis, metadados provenance |
mTLS (mutual TLS) — variante do protocolo TLS em que as duas pontas da conexão se autenticam mutuamente via certificados digitais, não só o servidor (como no HTTPS comum). Cliente e servidor trocam e validam certificados X.509 antes de estabelecer o canal criptografado. Usado para garantir que só serviços/dispositivos autorizados (ex.: um microsserviço, um sensor IoT, um pipeline de ingestão) conseguem se conectar a um endpoint, sem depender de senha/token.
HSM (Hardware Security Module) — dispositivo físico (ou serviço em nuvem equivalente, ex.: AWS CloudHSM, Azure Key Vault com HSM) dedicado a gerar, armazenar e usar chaves criptográficas sem que a chave privada jamais saia do hardware. Operações de assinatura/decriptação acontecem dentro do módulo; a chave nunca é exposta em memória de aplicação. Usado para proteger chaves raiz de criptografia, certificados usados em mTLS, ou segredos de alta sensibilidade (ex.: chaves de assinatura de transações financeiras).

<!-- Slide number: 48 -->
# Variedade na LODLog (vs global)
Estruturados (~30% LODLog; ~20% global didático): ERP/WMS/TMS → Parquet tipado
Semi (~60% LODLog): IoT JSON, APIs JSON/XML (XSD), logs (Avro/JSON Schema no streaming)
Não estrut. (~10% LODLog; ~80% global Dell 2022): PDFs OCR, e-mails NLP, imagens CV
Desafio: acomodar 3 tipos com Bronze schema-on-read → Silver/Gold schema-on-write (Delta)
Solução: Bronze/Silver/Gold + catálogo + contrato de dados

<!-- Slide number: 49 -->
Batch vs. Streaming vs. CDC vs. Event-driven
| Padrão | Latência | Exemplo LODLog | Tecnologia |
| --- | --- | --- | --- |
| Batch | Horas/dias | Fechamento financeiro, IBGE | Spark SQL, Airflow/Dagster, dbt (ELT) |
| Streaming | Segundos/min | Alerta temp. motor | Kafka + Spark Structured Streaming, Event Hubs/Kinesis |
| CDC | Segundos/min | Status pedido TMS↔WMS | Debezium, AWS DMS |
| Event-driven | Sob demanda | Bloqueio ANTT, alerta clima | Webhooks, EventBridge |

### Notes:
DRIFT-05: pipeline híbrido Medallion. Kafka/Flink/Spark para ingestão+validação.

<!-- Slide number: 50 -->
Resumo: Classificação das 8 Fontes LODLog
| Fonte | Tipo | 5 Vs principais | Ingestão |
| --- | --- | --- | --- |
| Sensores IoT | Semi | Volume alto, Velocity alta | Streaming (Kafka→Delta) |
| ERP | Estrut | Valor alto, Veracidade alta | Batch diário (Orquestrador→Parquet) |
| WMS | Estrut | Velocity média, Volume médio | Batch 15min (CDC) |
| TMS | Estrut | Velocity alta, Valor alto | CDC/Streaming |
| API Maps | Semi | Velocity alta, Valor alto | Streaming (5min) |
| API Clima | Semi | Velocity baixa, Valor médio | Batch horário |
| API ANTT | Semi | Event-driven | Event-driven |
| Base IBGE | Estrut | Volume mensal, Valor estratégico | Batch mensal |

### Notes:
Tabela a ser preenchida no lab.

<!-- Slide number: 51 -->
Lab 1: Passo a Passo no Databricks
1. Acessar https://community.cloud.databricks.com
2 Adicionar pasta git -> https://github.com/Escola-de-Matematica-Aplicada/Arq-Dados-Labs-Databricks.git

### Notes:
Guia prático.

<!-- Slide number: 52 -->
Discussão Pós-Lab

### Notes:
Perguntas conectam com drift.

<!-- Slide number: 53 -->
Resumo da Aula
1. Evolução: 1890 (Hollerith censo) → 1951 fitas seq → 1956 RAMAC rand → 1964 System/360 → 1970 Codd → 1979 Oracle V2 → 2003 GFS/MapReduce
2. OLTP (ACID, 3FN) vs OLAP (star/snowflake) — Inmon vs Kimball híbrido + ETL→ELT (dbt)
3. Tipos: estruturado (Parquet schema-on-write) vs semi (JSON/XML schema-on-read) vs não (NLP/OCR) + swamp→Lakehouse
4. 5 Vs com Veracidade em 4 camadas (edge/stream/cross/trust)
5. LODLog 8 fontes + Batch/Streaming/CDC/Event + Medallion Bronze/Silver/Gold
Ferramenta: Databricks CE  •  Cenário: LODLog

### Notes:
Recapitulação corrigida.

<!-- Slide number: 54 -->
Próximos Passos
28-set (M2): ler Módulo 2 (eCLASS) + trazer dúvidas classificação → RPG 'As Cinco Torres Isoladas' (DW×Lake×Lakehouse×Data Mesh)
Trabalho individual 70% (18/out): cenário rotas/manutenção/estoque/fraude + 3-5 fontes + 5 Vs + Bronze/Silver/Gold (Delta/Iceberg)
Dica: pense já em contrato de dados + catálogo para evitar swamp

### Notes:
Lembrar peso do trabalho.

<!-- Slide number: 55 -->
Referências
Codd (1970) Relational Model · Inmon (2005) Building DW · Kimball & Ross (2013) Toolkit
Serra (2024) Deciphering data architectures · Kleppmann (2017) DDIA (batch/stream)
Ghemawat et al. (2003) GFS (SOSP) · Delta Lake / Iceberg / Hudi docs (ACID sobre object storage)
DAMA-DMBOK 2 · AWS Academy Data Engineering M1 · LODLog Projeto Eng Dados IA para Negócio

### Notes:
Referências novas validadas.

<!-- Slide number: 56 -->
Dúvidas?
Próxima aula: 28-set — Arquiteturas modernas + RPG As Cinco Torres Isoladas