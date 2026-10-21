# LAB 2 — Avaliando Arquiteturas com o Modelo LODLog Pronto

**Disciplina** Arquitetura de Dados e Big Data
**Aula** 2 — Ferramentas para Gerenciamento de Dados Distribuídos (10 de novembro de 2026)
**Duração do Lab** demo de 20 min em aula (20h50–22h20 é dividido com o RPG e a discussão); execução completa em casa
**Entrega (grupo)** Parecer técnico de 1 página + checklist de "e se...", feitos em casa

> **Como este lab funciona:** vocês **não vão modelar do zero**. A consultoria de dados da LODLog já entregou os scripts (`lodlog_modelo_dados_free.sql`), o seed de dados, os diagramas do modelo (`/Diagramas/`) e notebooks prontos para executar no Databricks Free Edition. O trabalho de vocês é o que um executivo de dados **realmente** faz no dia a dia: **executar, inspecionar, questionar e avaliar** as escolhas arquiteturais de outros — aprovando, contestando ou propondo evolução.

---

## Antes de começar (5 min)

- Releia o **plano de ensino** (Módulo 2, no eClass) e os slides da **Aula 2**.
- Entre no **Databricks Free Edition** ([login.databricks.com](https://login.databricks.com)) — sem cartão, compute serverless. Os schemas do modelo ficam no catálogo `workspace`, schemas `lodlog_op` e `lodlog_dw`.
- Tenha ao lado os **diagramas prontos** na pasta [`/Diagramas/`](../../../Diagramas/):
  - `LODLog_op_v3.png` — modelo operacional (ER, 3FN)
  - `LODLog_dw_v3.png` — modelo analítico (Star Schema)

> ℹ️ **Sobre o dataset:** a LODLog "de verdade" tem 450 veículos, 12 CDs e ~18 mil entregas/mês. O banco de laboratório é um **recorte piloto**: 5 CDs do corredor Sudeste–Sul, 50 veículos e ~50 mil entregas acumuladas (2024–2026) — tamanho perfeito para o ambiente gratuito.

**Arquivos prontos deste lab (nesta pasta):**

| Arquivo | O que faz | Quando usar |
|---|---|---|
| `lab2-medallion-bronze-silver-gold.py` | Pipeline completo Bronze→Silver→Gold de IoT (executar células 1→6) | Parte 1 |
| `lodlog_modelo_dados_free.sql` | DDL do ER (`lodlog_op`) + Star Schema (`lodlog_dw`) — **executar na Atividade 2.0** e depois ler criticamente | Parte 2 |
| `lodlog_lab2_seed_free.py` | Geração de dados sintéticos para `lodlog_op` + **ETL SQL para `lodlog_dw`** (~3 min) — **executar na Atividade 2.0** | Parte 2 |
| `lab2-nosql-simulation.py` | Simulação KV / Documento / Coluna / Grafo com PySpark+Delta | Parte 2 (demo) |
| [`/Diagramas/`](../../../Diagramas/) | Diagramas ER e Star Schema já desenhados | Parte 2 |

---

## Objetivos de Aprendizagem

Ao final deste lab, você será capaz de:

1. **Executar** um pipeline Medallion (Bronze → Silver → Gold) em Delta Lake e **interpretar** o que cada camada transforma nos dados.
2. **Executar** a DDL do modelo LODLog e o ETL que popula `lodlog_dw` a partir de `lodlog_op`, e **ler** criticamente o resultado: ER 3FN e Star Schema com escolhas de projeto (PK (chave primária) e FK (chave estrangeira), surrogate keys, SCD, mini-dimensão).
3. **Avaliar criticamente** uma arquitetura de dados: reconhecer por que cada escolha foi feita, quais armadilhas ela evita e onde ela quebraria.
4. **Conectar** a escolha de arquitetura (DW/Lake/Lakehouse/Mesh/Fabric) aos objetivos e ao tamanho do negócio.
5. **Redigir** um parecer técnico curto — o artefato que um líder de dados usa para defender ou contestar uma arquitetura diante da diretoria.

---

## Parte 1 — Laboratório Vivo: O Medallion na Prática (30 min)

> 💡 *Na aula vocês discutiram DW × Lake × Lakehouse × Mesh. Este notebook é o Lakehouse "acontecendo": o mesmo dado IoT atravessa Bronze (confiança zero), Silver (confiança validada) e Gold (pronto para decisão). Rodar a esteira é a forma mais rápida de entender as camadas — avaliar o resultado é o que separa o gestor técnico do operador.*

### Atividade 1.1: Execute o pipeline (individual, 10 min)

1. No Databricks: **Workspace > Import > Upload** → `lab2-medallion-bronze-silver-gold.py` → **Run All**.
2. Anote nos comentários de cada célula o que o script faz em uma frase (Bronze: ingestão raw; Silver: filtragem + dedup + proveniência; Gold: agregação por veículo/dia; time-travel; resumo executivo).
3. Registre os três números impressos no console: contagem Bronze, contagem Silver, contagem Gold.

### Atividade 1.2: Interprete os números (grupo, 10 min)

Respondam **por escrito** (serve para o parecer da Parte 4):

1. **Bronze × Silver:** quantas linhas foram descartadas na Silver e **por quê**? O filtro de `velocidade 0–200 km/h` e `temperatura 50–150 °C` protege contra quê, na linguagem dos 5 Vs da Aula 1 (dica: *Veracidade*)?
2. **Silver × Gold:** a Gold tem ~1.500 linhas (50 veículos × 30 dias) contra centenas de milhares na Bronze. Essa "redução" é perda de informação ou ganho de foco? Para qual público cada camada fala (operação de manutenção × diretoria)?
3. **Time-travel:** a célula 5 mostra o `DESCRIBE HISTORY`. Citem **duas situações de negócio** em que poder voltar à versão anterior de uma tabela Delta vale dinheiro ou evita multa (pensem em LGPD (Lei Geral de Proteção de Dados), recall de decisão, auditoria de SLA).

### Atividade 1.3: Quebre a esteira de propósito (grupo, 10 min)

> ⚠️ Regra: **só no notebook do lab** — nunca num ambiente de produção.

1. Na célula 3, **comente uma das validações** (ex.: remova o filtro de temperatura), reexecute Silver e Gold, e observe o efeito nos gráficos/médias.
2. Respondam: se essa mudança acontecesse **em produção sem controle de versão**, como vocês detectariam o problema? O time-travel Delta seria suficiente ou faltaria algo (pensem em contrato de dados, catálogo, monitoração)?
3. Conexão com o RPG: essa célula é exatamente a armadilha da **Porta 3 ("Colheita Silenciosa")** — quick win sem blueprint. Deem um exemplo do mundo real em que "só tirar um filtro temporariamente" virou incidente.

---

## Parte 2 — O Modelo Entregue pela Consultoria: Subir, Executar e Ler (40 min)

> 💡 *O diagrama e a DDL que vocês vão inspecionar são um "produto de dados" entregue por terceiros. Antes de ler criticamente, vocês vão **subir o ambiente**: criar os schemas, popular `lodlog_op` com dados sintéticos e rodar o **ETL que constrói o star schema `lodlog_dw`** — exatamente como um pipeline real faz. O papel do gestor é saber executar, ler e perguntar "por quê?".*

### Atividade 2.0: Subir o modelo e rodar o ETL (grupo, 15 min)

1. No Databricks: **Workspace > Import** → `lodlog_modelo_dados_free.sql` → execute célula a célula (cria os schemas `lodlog_op` e `lodlog_dw` com todas as tabelas do ER e do Star Schema; ao final, a "CÉLULA 8" mostra `SHOW TABLES`).
2. Em seguida importe **`lodlog_lab2_seed_free.py`** → **Run All** (~3 min). Ele faz duas coisas: **(a)** gera dados sintéticos e carrega as 14 tabelas de `lodlog_op` (clientes, frota, pedidos e ~50 mil entregas em 2FN); **(b)** roda o **ETL em SQL** (`INSERT INTO … SELECT` e CTAS) que transforma `lodlog_op` no star schema `lodlog_dw` — 6 dimensões + `fato_entregas`.
3. Confiram no console: as contagens impressas por tabela (ex.: `✓ lodlog_dw.fato_entregas: 50.230 linhas`) — o número maior que 50.000 é proposital; vocês vão descobrir por quê na Atividade 3.4.
4. Registrem: qual foi a **última tabela carregada** pelo ETL e de quais tabelas `lodlog_op` ela depende (dica: olhem os JOINs da "Parte 6" do notebook).

> ⚠️ Não confundir com a Parte 1: lá o pipeline Medallion era de **telemetria IoT** (Bronze→Silver→Gold em Volumes). Aqui o pipeline é **transacional → analítico** (ER `lodlog_op` → ETL SQL → Star `lodlog_dw`). Dois padrões de movimento de dados, dois propósitos.

### Atividade 2.1: Duas camadas, dois propósitos (grupo, 10 min)

Comparem os dois diagramas prontos (`LODLog_op_v3.png` × `LODLog_dw_v3.png`) e completem **apenas 3 linhas** do quadro:

| Característica | ER (`lodlog_op`) | Star Schema (`lodlog_dw`) |
|---|---|---|
| Objetivo principal | *(respondam)* | *(respondam)* |
| Número de tabelas | *(contem nos diagramas)* | *(contem nos diagramas)* |
| Otimizado para | *(respondam)* | *(respondam)* |

Em seguida, **localizem sem responder** (só apontar no diagrama — o facilitador demonstra para a turma): onde está a `fato_entregas`, as 6 dimensões, e uma FK do modelo operacional.

### Atividade 2.2: Caça às escolhas no DDL (grupo, 10 min)

Abram `lodlog_modelo_dados_free.sql` **como leitura** (não editem). Para cada item, encontrem o trecho no script e digam **que problema ele resolve** — uma linha cada:

| # | Escolha no script pronto | Onde encontrar | Problema que resolve (respondam) |
|---|---|---|---|
| 1 | Tabelas `lodlog_op` separadas por domínio (cliente, veiculo, motorista...) | linhas 77–290 | |
| 2 | `sk_cliente` etc. (surrogate keys) no DW em vez de `cliente_id` | schema `lodlog_dw` | |
| 3 | Colunas `valido_de` / `valido_ate` (SCD Tipo 2) em `dim_cliente` | ~linha 374 | |
| 4 | `dim_centro_distribuicao` **sem** `valido_de/ate` (SCD Tipo 1) | ~linha 428 | |
| 5 | `dim_cat_atraso` com apenas 5 registros | ~linha 447 | |
| 6 | `ZORDER BY` nas tabelas Delta de alta cardinalidade | fatos e dims grandes | |

Pergunta de virada (escolha múltipla, justifiquem a letra): *Se um cliente fosse reclassificado de "Varejo" para "E-commerce" e a diretoria quisesse ver o histórico ANTERIOR como era, qual design torna isso possível?*
a) SCD Tipo 1 na dim_cliente · b) SCD Tipo 2 na dim_cliente · c) Mini-dimensão · d) ZORDER BY

### Atividade 2.3: Demo NoSQL — por que não "um banco para tudo" (individual, 10 min)

O facilitador roda `lab2-nosql-simulation.py` (ou cada grupo executa Run All). Comparem as 4 saídas (KV de rotas, Documento IoT heterogêneo, Coluna série temporal, Grafo de conexões) com a tabela `telemetria` do ER:

1. Citem **um** workload da LODLog que ficaria **pior** se fosse movido para um dos 4 NoSQL (ex.: faturamento em grafo?).
2. Confiram a frase da aula: *NoSQL é camada de ingestão/operação; Lakehouse é camada analítica — polyglot, não "um vence todos"*. O modelo LODLog entregue é coerente com essa frase?

---

## Parte 3 — Pensamento Crítico: "E se..." (20 min)

> 💡 *Toda arquitetura contém hipóteses sobre o negócio. Quando o negócio muda, a hipótese é testada. Estas questões simulam mudanças reais — respondam em grupo, em até 3 linhas cada, SEM alterar nenhum arquivo.*

1. **Crescimento:** A LODLog passa de 12 para 30 CDs em 3 países, e cada região quer autonomia sobre seus dados. O Lakehouse centralizado entregue **aguenta**? Em que momento a resposta vira Data Mesh — e o que muda na prática (quem é dono do quê)?
2. **Nova categoria:** O negócio pede a categoria "Atraso Severíssimo" (> 24h). O que muda em `dim_cat_atraso`, em `fato_entregas` e no pipeline? *(Spoiler: se a resposta envolver reescrever milhões de linhas da fato, algo está errado no desenho.)*
3. **SCD indevidamente:** E se `dim_cliente` fosse SCD Tipo 1 em vez de Tipo 2? Quem perde informação numa reunião de diretoria? Deem um exemplo concreto de pergunta de negócio que ficaria sem resposta.
4. **Pântano à vista:** O script seed cria **anomalias propositais** na `fato_entregas` (~100 duplicatas de `pedido_id`, valores negativos, outliers e FKs quebradas — anunciadas nos comentários do arquivo). Rodem uma contagem simples no Databricks ou SQL editor e respondam: qual camada Medallion **deveria** barrar isso, e por que a Bronze NÃO barra (e não deve)?
5. **Decisão de camada:** Um cientista de dados pede acesso direto à Bronze para treinar um modelo de predição de atraso. Vocês aprovam, negam ou aprovam com condição? Qual zona de Zaloni (Transiente/Sandbox?) resolve sem comprometer a governança?

---

## Parte 4 — Entrega do Grupo: Parecer Técnico (15 min em aula + 20 min em casa)

> 💡 *É isto — e só isto — que o grupo entrega. Nada de diagrama novo, nada de reescrever SQL. O miniprojeto da Aula 4-5 (trabalho em grupo, 30%) vai CONSTRUIR um lakehouse; este parecer é o músculo de AVALIAR, que a banca mais cobra: justificativa.*

**Formato:** 1 página (ou 1 slide), 4 seções:

1. **Parecer (5–8 linhas):** que arquitetura vocês recomendam para a LODLog **hoje** e qual a **evolução proposta para 3 anos** (a partir do cenário da Atividade "E se..." 1). Citem ao menos 2 critérios da matriz decisória da aula (dados, custo, governança, maturidade, escala).
2. **Dois "aprovamos":** duas escolhas do modelo entregue que vocês sustentariam sem mudança (ex.: mini-dimensão, SCD2 em cliente, Bronze imutável) — cada uma com **um** argumento de negócio, não técnico.
3. **Um "contestamos ou evoluímos":** uma escolha que vocês mudariam ou monitorariam de perto, com risco e mitigação (usem o vocabulário do RPG: armadilha, contrato de dados, governança federada leve, dívida técnica).
4. **Evidência da execução:** os 3 números do console da Atividade 1.1 (linhas Bronze/Silver/Gold) + print de uma consulta da Atividade 3.4.

Autoavaliação rápida (checkbox na entrega): [ ] todos do grupo participaram da discussão · [ ] rodamos o notebook juntos · [ ] nosso parecer cita o dataset piloto, não só a narrativa.

---

## Material de Apoio e Referências

- **Slides da Aula 2** (eClass): NoSQL, DW/Lake/Lakehouse/Mesh/Fabric, Medallion/Zaloni, RPG "As Cinco Torres Isoladas".
- **Plano de ensino** (eClass): Módulo 2.
- **Modelo de dados (pronto):** `lodlog_modelo_dados_free.sql` (nesta pasta).
- **Diagramas (prontos):** [`/Diagramas/LODLog_op_v3.png`](../../../Diagramas/LODLog_op_v3.png) e [`/Diagramas/LODLog_dw_v3.png`](../../../Diagramas/LODLog_dw_v3.png).
- **RPG "As Cinco Torres Isoladas"** — enunciado do aluno com o cenário LODLog em [`RPG-lodlog.md`](RPG-lodlog.md) (nesta pasta); materiais completos em `docs/Aulas-de-outros-cursos/Aula 8 Arquitetura de Dados/`. Roda na abertura da parte prática e conversa com as Partes 1 e 3 deste lab.

**Dica do Professor:** Vocês não precisam saber desenhar um Star Schema de cabeça para decidir bem — precisam saber **ler** um e perguntar "por quê?". O ER opera (transações); o Star analisa (agregações); o Medallion refina (confiança crescente). Um parecer maduro mostra que você entende as três frases.

---
