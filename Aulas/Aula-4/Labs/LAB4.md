# LAB 4 — Miniprojeto: Construção e Avaliação do Data Lake da LODLog

**Disciplina** Arquitetura de Dados e Big Data
**Aulas** 4 e 5 — Miniprojeto: Construção e Avaliação de Data Lake para a LODLog
**Datas** Aula 4 (17/11/2026): teoria curta + construção sobre o seed · Aula 5 (23/11/2026): 1ª metade para concluir o trabalho, 2ª metade para apresentações e lições aprendidas
**Entrega**
- **Individual (70%, até 08/dez — 15 dias após a Aula 5):** avaliação pós-projeto → siga o [`GUIA-ENTREGA-individual.md`](GUIA-ENTREGA-individual.md)
- **Grupo (30%):** notebook seed completado e executado + pitch de 10 min e 5 min de Q&A na Aula 5 (23/11) → siga o [`GUIA-ENTREGA-grupo.md`](GUIA-ENTREGA-grupo.md)

> **Como este miniprojeto funciona:** vocês **não começam do zero, mas também não recebem tudo pronto**. O notebook [`lab4_miniprojeto_seed.py`](lab4_miniprojeto_seed.py) entrega **70% do data lake da LODLog pronto e explicado** — sete fontes (estruturadas, semiestruturadas e não estruturadas) na Bronze, quatro delas tratadas na Silver, uma Gold de referência, exemplos de análise e governança e o tratamento do **dado mais crítico da empresa: o cliente e seu endereço**, cadastrados de jeitos diferentes no ERP, no TMS e na planilha comercial (MDM com SQL e IA). Os **30% restantes são do grupo**, em cinco TODOs curtos: levar uma fonte semi/não estruturada até a Silver, construir a Gold do cenário, interpretar a análise de negócio, aplicar governança com glossário e decidir o registro de ouro do cliente. O trabalho avaliado é o de um líder de dados: **decidir regras, escolher a métrica que responde ao negócio, executar, interpretar e avaliar a arquitetura com evidência.**

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
| **Seed do miniprojeto (70% pronto)** | [`lab4_miniprojeto_seed.py`](lab4_miniprojeto_seed.py) | 7 fontes LODLog na Bronze, 4 Silvers, Gold de referência, exemplos e o MDM de cliente e endereço; **5 TODOs para o grupo** — é o notebook do trabalho |
| Pipeline Medallion de referência (starter) | [`lab4_miniprojeto_starter.py`](lab4_miniprojeto_starter.py) | versão mínima 100% pronta (JSON IoT + TMS), para consulta |
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
3. **Aplicar** os 4 pilares de governança (qualidade, segurança/LGPD, metadados e glossário, ciclo de vida) como **lentes de avaliação** sobre uma arquitetura existente.
4. **Tratar o dado crítico** da empresa como dado mestre: padronizar, casar os registros dos três sistemas, medir a qualidade e **decidir** o registro de ouro — e nomear quem responde por ele.
5. **Justificar** — e quando for o caso, **contestar com evidência** — escolhas arquiteturais: batch vs streaming, ETL vs ELT, Lambda vs Kappa, SCD, centralização vs Mesh.
6. **Comunicar** decisões de arquitetura para uma banca executiva: parecer, números e lições — não slides decorados.

---

## Organização das Aulas 4 e 5

**Aula 4 (17/11) — construir sobre o seed:**

| Bloco | Horário | Duração | Conteúdo |
|-------|---------|---------|----------|
| **Teoria curta** | 19h00–19h40 | 40 min | Pântano + 4 pilares de governança (qualidade do dado crítico, segurança, metadados e glossário, ciclo de vida) + checklist |
| **Prática — Parte 1** | 19h40–20h40 | 60 min | Briefing + escolha do cenário + Etapa 2.1 (Run All do seed, leitura do que veio pronto) + TODO 1 |
| Intervalo | 20h40–20h55 | 15 min | — |
| **Prática — Parte 2** | 20h55–22h05 | 70 min | Etapa 2.2: TODO 2 (Gold do cenário), TODO 3 (interpretação) e TODO 5 (registro de ouro do cliente) |
| **Checkpoint** | 22h05–22h20 | 15 min | Cada grupo mostra a Etapa 8 do notebook (✅/⬜) e o que falta para a Aula 5 |

**Aula 5 (23/11) — concluir, apresentar e avaliar:**

| Bloco | Horário | Duração | Conteúdo |
|-------|---------|---------|----------|
| **Trabalho em grupo** | 19h00–20h30 | ~1h30 | Fechar os TODOs pendentes, TODO 4 (governança e glossário), Run All final, montar o pitch — com o professor circulando |
| Intervalo | 20h30–20h50 | 15–20 min | — |
| **Apresentações** | 20h50–21h55 | ~1h05 | Pitch de cada grupo (Etapa 2.3) — 10 + 5 min até 4 grupos; 7 + 3 com 5 ou mais |
| **Fechamento** | 21h55–22h20 | 25 min | Lições aprendidas da disciplina e preparação da entrega individual |

---

## Parte 1 — Teoria Curta: O Cinto de Segurança (40 min)

> 💡 *Antes de avaliar qualquer plataforma, você precisa saber o que pode dar errado. Estas 4 lentes evitam que um data lake vire um "pântano" — um depósito caro onde ninguém confia nos números.*

### Os 4 Pilares de Governança (use-os como lista de auditoria nas Práticas)

| Pilar | Pergunta que responde | Anti-padrão (swamp) |
|-------|----------------------|---------------------|
| **1. Qualidade** | Posso confiar nos dados? | Silver sem dedup/validação; anomalias chegando ao dashboard |
| **2. Segurança e LGPD** | Quem pode ver, mudar ou apagar? | PII exposta na Gold; bucket público |
| **3. Metadados e Glossário** | O que significa, onde está e de onde veio? | "De onde veio esse número?" sem resposta; cada área com a sua definição de "entrega" |
| **4. Ciclo de Vida e Operação** | Quanto tempo guardar e quanto custa? | Bronze sem particionamento; JSONs pequenos demais |

> Os "10 mandamentos" do slide "Critérios de Sucesso" da Aula 4 (Bronze imutável, particione, tipifique, deduplique, valide ranges, catalogue, anonimize, MERGE idempotente, monitore drift, documente lineage) são as perguntas que a banca fará no pitch da Aula 5.

---

## Parte 2 — Prática em Grupo (Aula 4: 2h25 · Aula 5: ~1h30 de trabalho + apresentações)

O notebook do grupo é o [`lab4_miniprojeto_seed.py`](lab4_miniprojeto_seed.py). Ele roda inteiro desde o começo (Run All, ~2 min); as partes do grupo ficam "em branco" até serem preenchidas, e a **Etapa 8** do notebook mostra o que já está ✅ e o que falta ⬜.

| | O que vem pronto (70%) | O que o grupo faz (30%) |
|---|---|---|
| **Fontes** | 7 fontes LODLog geradas com sujeira realista: IoT (JSON), TMS, ERP, WMS, API de clima (JSON), ocorrências dos motoristas (texto livre) e o cadastro de clientes em três sistemas (ERP, TMS e CRM) | — |
| **Bronze** | Todas as 7 fontes, com metadados de ingestão | — |
| **Silver** | IoT, TMS, ERP e WMS, com regras de qualidade comentadas | **TODO 1** — levar `clima` ou `ocorrencias` até a Silver, decidindo as regras |
| **Gold** | `resumo_diario_frota` (referência) + modelo quase pronto para cada cenário | **TODO 2** — escrever a métrica-chave da Gold do cenário |
| **Análise** | Exemplo completo: pergunta → consulta → frase para a diretoria; a consulta de cada cenário também vem pronta | **TODO 3** — pergunta de negócio e interpretação |
| **Governança** | Exemplo aplicado na Gold de referência (dono, descrição, PII, retenção), glossário de negócio e tags no catálogo | **TODO 4** — governança da Gold do grupo + regra de qualidade + **2 termos no glossário** com dono e steward |
| **Dado crítico (MDM)** | Cliente e endereço em ERP, TMS e CRM: padronização por regras SQL e por IA (`ai_query` com `system.ai.llama-4-maverick`), tabela de-para, scorecard de qualidade e análise de impacto na pontualidade | **TODO 5** — o registro de ouro: de onde vem o endereço oficial e o que é um "endereço válido para entrega" |

### Etapa 2.1 — Rodar o seed e entender o que veio pronto (Aula 4, ~45 min)

1. **Importe e rode:** Workspace › Import › `lab4_miniprojeto_seed.py` › defina `CENARIO` na primeira célula › Run All.
2. **Leia as Etapas 1 a 3:** para cada fonte, anote tipo de dado, forma de ingestão típica (batch, streaming, CDC) e **quantas linhas a Silver barrou e por quê** — é o slide de execução do pitch.
3. **Faça o TODO 1** (~20 min): escolha a fonte extra recomendada para o cenário e defina as regras (limite de chuva plausível ou palavras-chave das ocorrências). O notebook avisa se a regra deixou texto demais em `outros`.

### Etapa 2.2 — Gold e análise do cenário (Aula 4, 70 min)

1. **TODO 2** (~20 min): no modelo de Gold do seu cenário, troque `CAST(NULL AS DOUBLE)` pela fórmula da métrica-chave (a dica está no comentário). A Gold junta uma fonte **estruturada** com a fonte **semi/não estruturada** do TODO 1 — é a integração exigida na entrega.
2. **TODO 3** (~15 min): a consulta do cenário já vem pronta. Escreva a pergunta de negócio e a interpretação: *"o que eu diria ao diretor com este número? que decisão ele apoia?"*
3. **TODO 5** (~25 min) — **o dado mais crítico da LODLog** (Etapa 7B do notebook). Rodem as células prontas e leiam: o mesmo cliente nos três sistemas, a padronização por regra e por IA, a tabela de-para e o scorecard de qualidade. Então decidam, como um conselho de dados decidiria: **de onde vem o endereço oficial** (ERP, a versão mais usada no TMS ou a mais completa) e **o que é um endereço válido para entrega** (que regras valem). A célula seguinte grava o registro de ouro, leva os termos ao glossário com dono e steward e mostra quanto o endereço ruim custa em pontualidade.
4. **Para quem terminar antes — 1 teste de "E se"** (vira ponto forte no pós-projeto):
   - Mude a regra de qualidade da Silver do TODO 1 → o que muda na Gold e na conclusão?
   - Rode a Silver sem o `DISTINCT` → quantas duplicatas chegariam à Gold? Isso é a armadilha da "Colheita Silenciosa" (RPG da Aula 2)?
   - Sua Gold tem `cliente_id` ou `motorista_id`? Que pilar da LGPD isso aciona e em qual camada vocês tratariam?
   - No TODO 5, liguem e desliguem `tem_bairro`: quantos clientes "bons" passam a ser reprovados? O que isso faz com a análise de impacto?

Às 22h05, checkpoint: cada grupo mostra a Etapa 8 do notebook ao professor (formativo, sem nota).

### Etapa 2.3 — Concluir e apresentar (Aula 5, 23/11)

- **19h00–20h30:** concluir os TODOs pendentes, fazer o **TODO 4** (governança e glossário), rodar o Run All final com tudo ✅ e montar o pitch.
- **20h50–21h55:** **pitch de cada grupo** (10 min + 5 min de Q&A; com 5 ou mais grupos, 7 + 3) — formato no [`GUIA-ENTREGA-grupo.md`](GUIA-ENTREGA-grupo.md). Essência: cenário e pergunta → arquitetura (o que veio pronto × o que o grupo construiu) → números da Etapa 8 → insight de negócio → avaliação pós-projeto preliminar.

> ⚠️ *Diagrama novo não é exigido. O exigido é o fluxo do seed **comentado por vocês**: onde entra a sujeira, onde ela é barrada e onde nasce o número do dashboard.*

---

## Parte 3 — Entregas

As entregas têm guia próprio, com estrutura, pesos da rubrica (slides "Como Você Será Avaliado" da Aula 4) e checklist de submissão:

- **Grupo (30%, Aula 5 — 23/11):** [`GUIA-ENTREGA-grupo.md`](GUIA-ENTREGA-grupo.md) — o notebook seed com os 30% completados e executado de ponta a ponta (Etapa 8 toda ✅) + pitch de 10 min e 5 min de Q&A + 1 página de síntese pós-projeto preliminar.
- **Individual (70%, até 08/12/2026 — 15 dias após a Aula 5):** [`GUIA-ENTREGA-individual.md`](GUIA-ENTREGA-individual.md) — "Avaliação pós-projeto do data lake da LODLog": relatório executivo que parte do data lake que o grupo construiu e avalia criticamente a arquitetura, interpreta os resultados para o negócio, compara com uma alternativa e registra as lições aprendidas. Não exige código novo.

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
