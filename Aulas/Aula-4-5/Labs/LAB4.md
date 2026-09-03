# LAB 4 — Miniprojeto: Construção e Avaliação de Data Lake

**Disciplina** Arquitetura de Dados e Big Data
**Aulas** 4 e 5 — Miniprojeto: Construção e Avaliação de Data Lake para a LODLog (03 de outubro de 2026)
**Duração** Sessão dupla (~4h, com intervalos)
**Entrega**
- **Individual (70%, 15 dias após a última aula):** relatório + DDL + 2 queries analíticas + 1 de qualidade + conexão com IA
- **Grupo (30%):** apresentação + avaliação pós-projeto

> **Para quem é este lab:** Você é um executivo ou analista que já entende os dados (Aula 1), já sabe onde guardá-los (Aula 2) e já sabe como movê-los (Aula 3). Agora chega o momento de **construir de ponta a ponta** — do caos à solução. Este é o projeto que vai para a sua nota.

---

## Antes de começar

- Releia o **syllabus** (seção Módulo 4) e o conteúdo da **Aula 4-5**.
- Releia os Labs 1, 2 e 3 — tudo se conecta aqui.
- Garanta acesso ao **Databricks Free Edition** ([login.databricks.com](https://login.databricks.com), compute Serverless) — é onde o grupo vai construir o lakehouse.
- Importe o notebook **`lab4_miniprojeto_starter.py`** (nesta pasta): ele constrói um pipeline Bronze → Silver → Gold completo de exemplo (fonte JSON semiestruturada + fonte estruturada) em ~1 minuto, para o grupo adaptar ao seu cenário.
- Escolha um dos 4 cenários abaixo (definido pelo professor ou pelo seu grupo):

| Cenário | Descrição |
|---------|-----------|
| **(A) Rotas** | Otimização de rotas de entrega com dados IoT + Maps |
| **(B) Manutenção Preditiva** | Prever falhas de veículos usando telemetria |
| **(C) Estoque** | Gestão de estoque e previsão de ruptura |
| **(D) Fraude em Faturamento** | Detecção de anomalias em faturamento |

- **Requisito mínimo:** mapear 3–5 fontes de dados (internas e externas).

---

## Objetivos de Aprendizagem

Ao final deste lab, você será capaz de:

1. **Construir** um data lake / lakehouse com camadas Bronze → Silver → Gold no Databricks.
2. **Integrar** dados estruturados (ERP/WMS/TMS) e não estruturados (IoT JSON, APIs) no mesmo ambiente.
3. **Conduzir** uma análise sobre a camada Gold e contar a história com dados.
4. **Aplicar** os 4 pilares de governança para evitar o "pântano de dados".
5. **Avaliar** vantagens, limitações e lições aprendidas do projeto.

---

## Regra da Sessão Dupla

| Bloco | Horário | Duração | Conteúdo |
|-------|---------|---------|----------|
| **Teoria curta** | 19h00–19h40 | 40 min | 4 pilares de governança + checklist + pântano + MLOps |
| Intervalo 1 | 19h40–19h55 | 15 min | — |
| **Miniprojeto — Parte 1** | 19h55–20h55 | 60 min | Escolha de cenário + requisitos + desenho Bronze/Silver/Gold |
| Intervalo 2 | 20h55–21h10 | 15 min | — |
| **Miniprojeto — Parte 2** | 21h10–22h20 | 70 min | Construção Databricks + análise Gold + pitch 5min/grupo |

> ⚠️ *Cada intervalo conta para os 15 min obrigatórios do syllabus. A teoria é concentrada no início; a prática ocupa o restante.*

---

## Parte 1 — Teoria Curta: O Cinto de Segurança (40 min)

> 💡 *Antes de construir, você precisa saber o que pode dar errado. Estas 4 regras evitam que seu data lake vire um "pântano" — um depósito caro onde ninguém confia nos dados.*

### Os 4 Pilares de Governança

| Pilar | Pergunta que responde | Na LODLog |
|-------|----------------------|-----------|
| **1. Qualidade** | Posso confiar nos dados? | Scorecard com dimensões DAMA (completude, acurácia, consistência, atualidade, unicidade, validade) |
| **2. Segurança e LGPD** | Quem pode ver, mudar ou apagar? | Classificação + anonimização de PII + retenção por sensibilidade |
| **3. Catálogo e Linhagem** | Onde está e de onde veio? | Catalog (Glue/Purview) + lineage Bronze→Gold |
| **4. Ciclo de Vida e Operação** | Quanto tempo guardar e quanto custa? | Particionamento + retenção + vacuum + monitoramento |

### O Pântano de Dados (Data Swamp) — o anti-Lake

> *"Um data lake sem governança é só um data swamp com marketing."*

- **Sintomas:** ninguém confia nos números; duplicatas; `select *` varre terabytes; dashboards divergem.
- **Causas:** Bronze sem particionamento; Silver sem deduplicação; Gold sem contrato; sem dono por domínio.
- **Custo para a LODLog:** 26M eventos IoT/mês × 12 meses sem particionamento = scan de 300M linhas por query → centenas de dólares por dashboard.

---

## Parte 2 — Miniprojeto em Grupo (2h20 min)

### Etapa 2.1 — Requisitos e Desenho (60 min)

Para o seu cenário escolhido, defina:

**1. Fontes de dados (mínimo 3–5):**

| Fonte | Tipo | Formato | Volume | Frequência |
|-------|------|---------|--------|------------|
| Ex: Sensores IoT da frota | Semiestruturado | JSON | ~864k eventos/dia | A cada 30s |
| Ex: TMS (pedidos) | Estruturado | SQL/Parquet | ~3k registros/dia | Tempo real |
| Ex: API Google Maps | Semiestruturado | JSON | ~60k req/dia | A cada 5 min |
| Ex: Base IBGE | Estruturado | CSV | ~500 MB | Mensal |
| (Adicione mais...) | | | | |

**2. Análise dos 5 Vs para as fontes escolhidas:**

> 💡 *Cada V é uma pergunta de negócio. Volume = quanto custa guardar? Velocidade = quão rápido preciso reagir? Variedade = preciso de um lake ou de um warehouse? Veracidade = confio nestes dados? Valor = o que o negócio ganha com isso?*

**3. Arquitetura proposta com camadas Bronze/Silver/Gold e justificativa:**

| Camada | O que acontece aqui | Tecnologia |
|--------|---------------------|------------|
| **Bronze** | Dados brutos como vieram | JSON/Parquet no object storage |
| **Silver** | Dados limpos, validados, enriquecidos | Delta Lake com schema enforcement |
| **Gold** | Dados agregados, prontos para consumo e IA | Delta Lake, Star Schema, Feature Store |

**4. Batch vs. Streaming — justifique:**

| Fluxo | Proposta | Justificativa |
|-------|----------|---------------|
| IoT → Bronze | Streaming | Precisa saber a localização dos motoristas em tempo real |
| ERP → Silver | Batch diário | Faturamento não muda em tempo real |
| SLA → Dashboard | Batch/Híbrido | Relatórios diários + alertas para atrasos críticos |

---

### Etapa 2.2 — Construção e Análise (70 min)

**No Databricks Free Edition** (partindo do `lab4_miniprojeto_starter.py`):

1. **Crie as tabelas Bronze** — dados brutos no formato original (JSON, CSV).
2. **Crie as tabelas Silver** — dados limpos com schema aplicado, deduplicados, validados.
3. **Crie as tabelas Gold** — dados agregados e modelados dimensionalmente (Star Schema).
4. **Execute pelo menos 2 queries analíticas** sobre a camada Gold (ex: taxa de atraso por cenário, correlação de variáveis).
5. **Identifique pelo menos 1 problema de qualidade de dados** e proponha a solução.

> 💡 *Use o que aprendeu no LAB 3: queries analíticas, Window Functions, Feature Store, detecção de anomalias.*

---

### Etapa 2.3 — Pitch e Pós-Projeto (30 min)

**Pitch (5 min por grupo):**
- Cenário escolhido e por quê.
- Arquitetura proposta (diagrama simplificado).
- 1 insight de negócio descoberto na análise Gold.
- 1 lição aprendida.

**Pós-projeto (individual, 15 dias):**
- Vantagens e limitações da arquitetura adotada.
- O que mudaria se pudesse recomeçar.

---

## Parte 3 — Entrega Individual (70% da nota)

> *Entregar em até 15 dias após a última aula (prazo: 18 de outubro de 2026).*

O relatório individual deve conter:

1. **Cenário sub-escolhido** (mesmo que diferente do grupo) e fontes de dados mapeadas (mínimo 3–5, internas e externas).
2. **Análise dos 5 Vs** para as fontes escolhidas — com justificativa.
3. **Arquitetura proposta** (Data Lake ou Lakehouse) com camadas Bronze/Silver/Gold e justificativa batch vs. streaming.
4. **DDL** das tabelas criadas no lakehouse.
5. **2 queries analíticas** conduzidas sobre os dados (com interpretação de negócio).
6. **1 query de qualidade de dados** (detectar anomalias) + solução proposta.
7. **Conexão com IA** — como os dados do seu lakehouse alimentam um modelo preditivo.
8. **Avaliação pós-projeto:** vantagens, limitações e lições aprendidas.

---

## Parte 4 — Entrega em Grupo (30% da nota)

**Apresentação na última aula:**
- Arquitetura simplificada do data lake (fontes até o consumo).
- Integração de pelo menos uma fonte estruturada e uma não estruturada/semiestruturada.
- Resultado de uma análise conduzida sobre os dados.
- Avaliação pós-projeto: vantagens, limitações e lições aprendidas.

---

## Checklist do Miniprojeto

Use esta lista para garantir que entregou tudo:

- [ ] Cenário escolhido e justificado
- [ ] 3–5 fontes de dados mapeadas (internas + externas)
- [ ] Análise dos 5 Vs para cada fonte
- [ ] Arquitetura Bronze/Silver/Gold desenhada e justificada
- [ ] Batch vs. Streaming definido por fluxo
- [ ] DDL das tabelas no Databricks
- [ ] 2 queries analíticas com interpretação de negócio
- [ ] 1 query de qualidade de dados
- [ ] Conexão com IA / ML explicitada
- [ ] Avaliação pós-projeto (vantagens/limitações)
- [ ] Conformidade com LGPD considerada (anonimização, retenção)
- [ ] Particionamento e ciclo de vida definidos
- [ ] 4 pilares de governança aplicados

---

## Material de Apoio e Referências

- **Conteúdo da Aula 4-5** (`aula-4-5.md`): 4 pilares de governança, pântano de dados, Feature Store + MLOps, checklist, rubrica de avaliação.
- **Syllabus** (`syllabus.md`): seção Módulo 4 — Avaliação, Competências, Ementa.
- **CLAUDE.md** (`/workspaces/CLAUDE.md`): modelo de dados LODLog — duas camadas (`lodlog_op` + `lodlog_dw`), regra hard de coerência.
- **Modelo de dados:** `Labs/lodlog_modelo_dados_v3.sql` (DDL completa).
- **Labs anteriores:** `Labs/LAB3.md` (queries SQL, Feature Store, data quality).
- **Cenário LODLog:** `Labs/AGENTS.md` — regras do ambiente Databricks e estrutura do modelo.

**Referências complementares para o relatório individual:**
- Serra, J. (2024). *Deciphering data architectures*. O'Reilly Media.
- Inmon, W. H., Linstedt, D., & Levins, M. (2019). *Data architecture: a primer for the data scientist*. Elsevier.
- Kleppmann, M. (2017). *Designing data-intensive applications*. O'Reilly Media.

---

## Notas para o Facilitador

| Item | Detalhe |
|------|---------|
| **Duração** | Sessão dupla (~4h com intervalos) |
| **Teoria** | 40 min — governança, pântano, MLOps |
| **Prática** | 2h20 — construção, análise, pitch |
| **Individual (70%)** | Relatório + DDL + 2 queries + qualidade + IA. Prazo: 18/10 |
| **Grupo (30%)** | Apresentação + avaliação pós-projeto |
| **Avaliação** | Disciplina isenta de prova — trabalho |

**Dica final:** Arquitetura de dados não é sobre escolher a ferramenta mais bonita — é sobre resolver o problema de negócio com o custo e a maturidade certos. Justifiquem cada escolha com base no valor que ela desbloqueia.
