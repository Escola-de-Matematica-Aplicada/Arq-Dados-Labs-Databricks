# LAB 4 — Miniprojeto: Avaliação de um Data Lake Executável

**Disciplina** Arquitetura de Dados e Big Data
**Aulas** 4 e 5 — Miniprojeto: Construção e Avaliação de Data Lake para a LODLog
**Datas** Aula 4 (17/11/2026): teoria curta + execução e análise · Aula 5 (23/11/2026): apresentação dos grupos e lições aprendidas
**Entrega**
- **Individual (70%, até 08/dez — 15 dias após a Aula 5):** relatório guiado → siga o [`GUIA-ENTREGA-individual.md`](GUIA-ENTREGA-individual.md)
- **Grupo (30%):** pitch de 10 min + 5 min de Q&A na Aula 5 (23/11) → siga o [`GUIA-ENTREGA-grupo.md`](GUIA-ENTREGA-grupo.md)

> **Como este miniprojeto funciona:** vocês **não vão construir um data lake do zero**. O ambiente pronto já traz tudo: a DDL do modelo LODLog (`lodlog_modelo_dados_free.sql`), o seed com ~50 mil entregas (`lodlog_lab2_seed_free.py`), os diagramas do ER e do Star Schema ([`/Diagramas/`](../../../Diagramas/)) e um pipeline Medallion executável (`lab4_miniprojeto_starter.py`) que roda em ~1 minuto no Databricks Free Edition. O trabalho avaliado é o que um líder de dados faz de verdade diante de uma plataforma pronta: **executar, inspecionar, analisar os resultados, questionar as escolhas de arquitetura e sustentá-las (ou contestá-las) com evidência.** Justificativa vale mais que linha de código — é isso que a banca cobra.

---

## Antes de começar

- Releia o **plano de ensino** (Módulo 4 e Avaliação, no eClass) e os slides da **Aula 4**: 4 pilares de governança, pântano de dados, quem consome a Gold.
- Releia os Labs 1–3 — tudo se conecta aqui: tipos de dados e 5 Vs (L1), arquiteturas e Medallion (L2), SQL e qualidade (L3).
- Garanta acesso ao **Databricks Free Edition** ([login.databricks.com](https://login.databricks.com), compute Serverless) ANTES da aula.

**O que vocês recebem pronto:**

| Artefato | Onde | O que entrega de bandeja |
|---|---|---|
| DDL completa (ER `lodlog_op` + Star `lodlog_dw`) | [`../../Aula-2/Labs/lodlog_modelo_dados_free.sql`](../../Aula-2/Labs/lodlog_modelo_dados_free.sql) | modelo dimensional já projetado — para ler e criticar, não para escrever |
| Seed LODLog (~50k entregas, com anomalias propositais) | [`../../Aula-2/Labs/lodlog_lab2_seed_free.py`](../../Aula-2/Labs/lodlog_lab2_seed_free.py) | dados reais para as suas queries de análise e qualidade |
| Notebook de apoio com queries guiadas | [`../../Aula-3/Labs/LAB3_apoio_free.ipynb`](../../Aula-3/Labs/LAB3_apoio_free.ipynb) | ponto de partida das queries analíticas |
| Pipeline Medallion completo (starter) | [`lab4_miniprojeto_starter.py`](lab4_miniprojeto_starter.py) | Bronze→Silver→Gold funcionando (JSON IoT + TMS) — adaptem ao cenário do grupo |
| Diagramas prontos (ER + Star Schema) | [`/Diagramas/`](../../../Diagramas/) | `LODLog_op_v3.png` e `LODLog_dw_v3.png` — use-os no pitch e no relatório |

**Escolha do cenário** (1 por grupo; o individual pode ser outro, se quiser):

| Cenário | Pergunta de negócio | Gold de referência |
|---|---|---|
| **(A) Rotas de entrega** | Como reduzir os 23% de atraso e as multas de R$ 4,2 MM/ano? | `fato_entregas` + pontualidade por CD/mês |
| **(B) Manutenção Preditiva** | Como evitar quebras e R$ 2,1 MM/ano em reboque? | resumo diário da frota (temp, rpm, combustível) |
| **(C) Estoque e reposição** | Como evitar ruptura e +R$ 1,8 MM em horas extras? | `receita_diaria`/giro por CD |
| **(D) Fraude em Faturamento** | Como detectar divergências entre TMS, WMS e ERP? | anomalias em `fato_entregas` + regra de validação |

---

## Objetivos de Aprendizagem

Ao final deste miniprojeto, você será capaz de:

1. **Executar** um pipeline Medallion completo (Bronze → Silver → Gold) sobre dados semiestruturados e estruturados, e **explicar** o que cada camada transformou.
2. **Conduzir** análises sobre a camada Gold e **auditar** a qualidade dos dados com SQL — usando as anomalias propositais do seed como material de prova.
3. **Aplicar** os 4 pilares de governança (qualidade, segurança/LGPD, catálogo/linhagem, ciclo de vida) como **lentes de avaliação** sobre uma arquitetura existente.
4. **Justificar** — e quando for o caso, **contestar com evidência** — escolhas arquiteturais: batch vs streaming, ETL vs ELT, Lambda vs Kappa, SCD, centralização vs Mesh.
5. **Comunicar** decisões de arquitetura para uma banca executiva: parecer, números e lições — não slides decorados.

---

## Organização das Aulas 4 e 5

**Aula 4 (17/11) — construir e analisar:**

| Bloco | Horário | Duração | Conteúdo |
|-------|---------|---------|----------|
| **Teoria curta** | 19h00–19h40 | 40 min | 4 pilares de governança + checklist + pântano + MLOps |
| **Prática — Parte 1** | 19h40–20h40 | 60 min | Briefing + escolha do cenário + Etapa 2.1 (executar o starter e mapear o cenário) |
| Intervalo | 20h40–20h55 | 15 min | — |
| **Prática — Parte 2** | 20h55–22h05 | 70 min | Etapa 2.2 (análise Gold + auditoria + "E se") + pós-projeto e rascunho do pitch |
| **Checkpoint** | 22h05–22h20 | 15 min | Cada grupo mostra o que tem e o que falta para a Aula 5 |

**Aula 5 (23/11) — apresentar e avaliar:** pitch de cada grupo (10 min + 5 min de Q&A), discussões entre os grupos e lições aprendidas da disciplina (Etapa 2.3).

---

## Parte 1 — Teoria Curta: O Cinto de Segurança (40 min)

> 💡 *Antes de avaliar qualquer plataforma, você precisa saber o que pode dar errado. Estas 4 lentes evitam que um data lake vire um "pântano" — um depósito caro onde ninguém confia nos números.*

### Os 4 Pilares de Governança (use-os como lista de auditoria nas Práticas)

| Pilar | Pergunta que responde | Anti-padrão (swamp) |
|-------|----------------------|---------------------|
| **1. Qualidade** | Posso confiar nos dados? | Silver sem dedup/validação; anomalias chegando ao dashboard |
| **2. Segurança e LGPD** | Quem pode ver, mudar ou apagar? | PII exposta na Gold; bucket público |
| **3. Catálogo e Linhagem** | Onde está e de onde veio? | "De onde veio esse número?" sem resposta |
| **4. Ciclo de Vida e Operação** | Quanto tempo guardar e quanto custa? | Bronze sem particionamento; JSONs pequenos demais |

> Os "10 mandamentos" do slide "Critérios de Sucesso" da Aula 4 (Bronze imutável, particione, tipifique, deduplique, valide ranges, catalogue, anonimize, MERGE idempotente, monitore drift, documente lineage) são as perguntas que a banca fará no pitch da Aula 5.

---

## Parte 2 — Prática em Grupo (Aula 4: 2h25 · Aula 5: apresentação)

### Etapa 2.1 — Execute o Lakehouse Pronto e prove que ele funciona (Aula 4, 50 min)

> 💡 *O starter já faz o que um projeto levaria semanas. O trabalho de vocês é executar, ler com atenção e **ver com os próprios olhos** cada promessa de arquitetura se materializando (ou não) nos números do console.*

1. **Suba o ambiente:** execute (se ainda não feito) `lodlog_modelo_dados_free.sql` e `lodlog_lab2_seed_free.py` nos seus workspaces.
2. **Rode `lab4_miniprojeto_starter.py` (Run All, ~1 min)** e registre no notebook os números do console: linhas Bronze IoT × Silver IoT (quantos eventos a mais/menos? por quê?), linhas TMS, agregados Gold.
3. **Inspecione as 6 tabelas criadas** (`lodlog_bronze.*`, `lodlog_silver.*`, `lodlog_gold.*`): para cada uma, anote uma frase — *o que entra aqui, o que sai daqui, quem consumiria isso* (operação? diretoria? modelo de IA?).
4. **Mapeie o cenário do grupo sobre o pronto:** preencha a tabela fonte×camada do seu cenário usando as tabelas existentes + o que o starter simula (ex.: cenário B → `iot_eventos` da Silver é o coração; cenário D → a auditoria nasce das anomalias do seed na `fato_entregas`).
5. **Aponte as lentes:** marque quais dos 4 pilares o starter **cumpre visivelmente** e quais ele **não cobre** (dica: ele particiona a Bronze? ele anonimiza PII? ele registra lineage?). Isso vira conteúdo do pós-projeto.

### Etapa 2.2 — Análise com evidência: Gold e qualidade (Aula 4, 40 min + 30 min de pós-projeto)

Usando o `LAB3_apoio_free.ipynb` como referência de escrita SQL (copiem células para o notebook do grupo — adaptar é permitido e esperado):

1. **2 queries analíticas** sobre os dados do cenário — uma sobre as tabelas Gold do starter, uma sobre `lodlog_dw.fato_entregas` (+ dimensões). Cada uma com **uma frase de interpretação de negócio** ("o que eu diria ao Diretor de Operações com este número?").
2. **1 query de auditoria** explorando as anomalias propositais do seed (duplicatas de `pedido_id`, valores negativos, outliers, FK quebrada): quantifiquem cada tipo e respondam **em qual camada Medallion cada anomalias deveria ser barrada — e por que na Bronze ela deve passar**.
3. **1 teste de "E se" arquitetural** (escolham um):
   - Alterem um range de validação na Silver do starter → o que muda na Gold? Que dano silencioso isso causaria em produção sem time-travel?
   - Transformem o MERGE/overwrite em append puro → rodem duas vezes → contem as duplicatas. Isso é ou não é a armadilha da "Colheita Silenciosa" (RPG da Aula 2)?
   - Apaguem o filtro de PII/nulo → reflitam: que artigo de LGPD está sendo violado em qual camada?

Nos 30 min finais da Parte 2, rascunhem o pós-projeto (2 vantagens, 2 limitações, 1 lição) e o esqueleto do pitch. Às 22h05, cada grupo mostra o checkpoint ao professor (formativo, sem nota).

### Etapa 2.3 — Pitch do grupo (Aula 5, 23/11)

**10 min por grupo + 5 min de Q&A** — formato completo no [`GUIA-ENTREGA-grupo.md`](GUIA-ENTREGA-grupo.md). Essência: cenário e pergunta de negócio → diagrama (usem os PNGs prontos, anotados) → números da execução (Bronze/Silver/Gold) → 1 insight de negócio → 1 escolha que defendem + 1 que contestam → lição pós-projeto.

> ⚠️ *O "diagrama novo" não é exigido — o exigido é o diagrama **comentado por vocês**: uma foto do `LODLog_dw_v3.png` com 3 setas marcando onde entra a sujeira, onde ela é barrada e onde nasce o número do dashboard.*

---

## Parte 3 — Entregas

As entregas têm guia próprio, com estrutura, pesos da rubrica (slides "Como Você Será Avaliado" da Aula 4) e checklist de submissão:

- **Individual (70%, até 08/12/2026 — 15 dias após a Aula 5):** [`GUIA-ENTREGA-individual.md`](GUIA-ENTREGA-individual.md) — "Aprofundamento de cenário da LODLog": PDF de 4–6 páginas com o núcleo de arquitetura (fontes, 5 Vs, Bronze/Silver/Gold com batch × streaming) e a conexão transformadora (maturidade em dados × arquitetura empresarial); anexo técnico opcional no Databricks ou no AWS Academy.
- **Grupo (30%, apresentação na Aula 5 — 23/11):** [`GUIA-ENTREGA-grupo.md`](GUIA-ENTREGA-grupo.md) — pitch de 10 min + 5 min de Q&A + 1 página de síntese pós-projeto.

Em ambas, o critério de ouro é o mesmo da disciplina: **toda afirmação de arquitetura precisa de uma evidência** (um número do console, uma query, uma linha de DDL, um quadro do diagrama) — ou de uma pergunta honesta ("não testamos X; testaríamos assim").

---

## Material de Apoio e Referências

- **Slides das Aulas 4 e 5** (eClass): governança, pântano, rubricas e template do pitch.
- **Plano de ensino** (eClass): Módulo 4 e Avaliação.
- **Artefatos prontos:** ver tabela "O que vocês recebem pronto" no topo.
- **LAB 2 refeito** (`../../Aula-2/Labs/LAB2.md`): o parecer técnico do grupo é o modelo do que se espera de justificativa arquitetural aqui.
- **Referências complementares:** Serra (2024) cap. 3–5; Inmon et al. (2019); Kleppmann (2017) cap. 1–3.

**Dica do Professor:** Arquitetura de dados não é sobre escolher a ferramenta mais bonita — é sobre resolver o problema de negócio com o custo e a maturidade certos. Como desta vez a arquitetura já vem escolhida por terceiros, sobra tempo para o que realmente diferencia um executivo de dados: perguntar *"por quê?"* a cada tabela e provar a resposta com números.

---
