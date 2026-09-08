# LAB 2 — Modelagem de Dados para Analytics

**Disciplina** Arquitetura de Dados e Big Data
**Aula** 2 — Ferramentas para Gerenciamento de Dados Distribuídos (28 de setembro de 2026)
**Duração do Lab** ~1h40 (em aula)
**Entrega** Diagrama ER + DDL SQL + justificativas + mapeamento para camadas Medallion

> **Para quem é este lab:** Você é um executivo ou analista que agora sabe *quais dados tem* (Aula 1) e precisa decidir *onde guardá-los* e *como organizá-los*. Este lab te guia pela escolha certa de arquitetura, com foco no que importa para o negócio.

---

## Antes de começar

- Releia o **syllabus** (seção Módulo 2) e o conteúdo da **Aula 2**.
- Se possível, entre no **Databricks Free Edition** (crie sua conta gratuita em [databricks.com/learn/free-edition](https://www.databricks.com/learn/free-edition) e faça login em [login.databricks.com](https://login.databricks.com)) e inspecione as tabelas do modelo LODLog no menu **Catalog** — elas ficam no catálogo `workspace`, schemas `lodlog_op` e `lodlog_dw`.
- Scripts de referência (nesta pasta): `lodlog_modelo_dados_free.sql` (DDL) e `../../Aula-3/Labs/lodlog_lab3_seed_free.py` (seed de dados).

> ℹ️ **Sobre o dataset:** a LODLog "de verdade" tem 450 veículos, 12 CDs e ~18 mil entregas/mês. O banco de laboratório é um **recorte piloto**: 5 CDs do corredor Sudeste–Sul, 50 veículos e ~50 mil entregas acumuladas (2024–2026) — tamanho perfeito para o ambiente gratuito.

---

## Objetivos de Aprendizagem

Ao final deste lab, você será capaz de:

1. **Diferenciar** Data Warehouse, Data Lake, Lakehouse e Data Mesh — e escolher a mais adequada ao seu cenário.
2. **Explicar** a arquitetura Medallion (Bronze → Silver → Gold) e as zonas de refinamento de Zaloni.
3. **Normalizar** um modelo entidade-relacionamento para a 3FN (Terceira Forma Normal).
4. **Projetar** um Star Schema para analytics, incluindo a mini-dimensão de KPIs.
5. **Justificar** o uso de surrogate keys vs. natural keys — e quando desnormalizar para ganho de performance.
6. **Conectar** a escolha de arquitetura aos objetivos de negócio da empresa.

---

## Parte 0 — Contexto (5 min)

Na Aula 1, o grupo mapeou o ecossistema de dados da LODLog. Agora é hora de **estruturar** esses dados — decidir onde cada um vai morar e como vai ser organizado.

> 💡 *Pense assim: se os dados são o petróleo bruto que a LODLog extrai de 8 fontes diferentes, a modelagem é o refino. Você não vende petróleo cru — você transforma em combustível que move o negócio.*

**Problema do dia:** A LODLog tem dados espalhados em ERP, WMS, TMS e sensores IoT. Cada sistema usa suas próprias chaves e formatos. Não há uma visão unificada do cliente, do veículo ou do produto. Relatórios demoram porque precisam fazer JOINs complexos entre sistemas.

**Missão do LAB 2:** Entender as arquiteturas disponíveis, normalizar o modelo até a 3FN, projetar o Star Schema com a nova mini-dimensão de categoria de atraso, e implementar o DDL correspondente.

---

## Parte 1 — Arquiteturas Modernas: O Quadrante de Decisão (30 min)

> 💡 *Não existe "a melhor arquitetura". Existe a mais adequada ao tamanho, orçamento e maturidade da sua empresa. Seu papel como executivo é escolher com consciência.*

### Atividade 1.1: Complete o Quadrante Comparativo (individual, 10 min)

Preencha os espaços em branco na tabela comparativa. Use como referência o conteúdo da Aula 2 e o modelo LODLog:

| Arquitetura | Tipo de Dados Suportados | Estratégia de Schema | Caso Ideal de Uso | Limitações (Evitar quando...) |
|---|---|---|---|---|
| **Data Warehouse** | Estruturado apenas | Schema-on-write (validação rígida na escrita) | BI tradicional, dashboards executivos estáveis | Dados semiestruturados de alta frequência (IoT), dados não estruturados |
| **Data Lake** | Todos os tipos, em formato bruto | Schema-on-read (descoberto na leitura) | Armazenamento em escala, Big Data, exploração de Data Science | Usuários de negócio precisam de consultas rápidas (risco de *data swamp*) |
| **Lakehouse** | Todos os tipos, com governança | Híbrido (metadados abertos com ACID) | Unificar BI + ML num só lugar, reduzir custos e complexidade | Projetos muito pequenos com equipes sem maturidade |
| **Data Mesh** | Descentralizado (por domínio) | Descentralizado, cada domínio é dono do seu dado | Grandes organizações com múltiplos domínios autônomos | Organizações pequenas/médias sem cultura de cooperação |

> 💬 *Para a LODLog: 450 veículos, 12 CDs, ~18 mil entregas/mês — um Lakehouse (Databricks + Delta Lake) é a escolha natural. Data Mesh só faz sentido se a empresa crescer para dezenas de CDs autônomos.*

### Atividade 1.2: Posicionamento Estratégico da LODLog (grupo, 15 min)

Discutam o seguinte cenário de crescimento e tomem uma decisão de arquitetura:

| Momento | Detalhes |
|---------|----------|
| **Hoje** | 450 veículos, 12 CDs, ~18 mil entregas/mês |
| **Daqui a 3 anos** | 1.500 veículos, 30 CDs, ~60 mil entregas/mês, operação em 3 países da América Latina |

**Questão:** *"Qual arquitetura analítica vocês recomendam para a LODLog hoje? Qual a evolução proposta para os próximos 3 anos? Justifiquem em 6 a 10 linhas."*

### Atividade 1.3: Arquitetura Medallion — Bronze, Silver, Gold (grupo, 10 min)

> 💡 *O padrão Medallion é a forma mais prática de organizar dados num Lakehouse. Funciona como uma esteira de produção: raw → limpo → pronto para consumo.*

Para cada fonte de dados da LODLog, preencham o que acontece em cada camada:

| Fonte Original | Camada Bronze (Raw) | Camada Silver (Limpo) | Camada Gold (Consumo) |
|---|---|---|---|
| Telemetria IoT (GPS e Sensores) | JSON bruto, particionado por data | Schema aplicado, validação de ranges, dedup | `fato_iot_hora` + `dim_veiculo` — médias por veículo/hora |
| Pedidos do TMS (Banco Relacional) | Tabelas replicadas sem transformação | FKs validadas, tipos corrigidos | `fato_entregas` + métricas de SLA |
| Estoque do WMS (Arquivos CSV) | CSV bruto | Nulos tratados, SKUs uniformizados | Nível de giro por CD, alertas de ruptura |
| APIs Externas (Clima, Tráfego) | JSON/XML bruto com timestamp | Temperaturas padronizadas, condições classificadas | Features para predição de atraso |

> 💬 *Regra de ouro: a camada Bronze nunca é reescrita destrutivamente. Se algo der errado, você sempre pode reprocessar a partir do raw.*

---

## Parte 2 — Modelagem: Normalização e Star Schema (35 min)

> 💡 *Agora que decidimos *onde* guardar, precisamos *como* estruturar. Existem dois modelos que servem a propósitos diferentes: o ER (para transações) e o Star Schema (para análises).*

### Atividade 2.1: A Tabela Entrega em 2FN — Problema Proposital (grupo, 10 min)

> ⚠️ *A tabela `lodlog_op.entrega` foi entregue propositalmente em 2FN — com dependências transitivas (dados redundantes de cliente, veículo, motorista e CD). Sua missão é normalizar até a 3FN.*

Inspecione a tabela no Databricks. Ela tem a PK `entrega_id` (simples) — então está em 1FN e 2FN (sem dependências parciais), mas tem **4 grupos de dependências transitivas**:

- **Dados do CLIENTE** → `cliente_id` → `cliente_cnpj` → `cliente_razao_social` → `cliente_segmento`
- **Dados do VEÍCULO** → `veiculo_id` → `veiculo_placa` → `veiculo_modelo` → `veiculo_fabricante`
- **Dados do MOTORISTA** → `motorista_id` → `motorista_nome` → `motorista_cnh` → `motorista_categoria`
- **Dados do CD** → `cd_origem_id` → `cd_origem_codigo` → `cd_origem_nome` → `cd_origem_uf`

**Responda (escreva no caderno ou no chat):**

1. Se um cliente trocar de razão social, **quantas linhas** precisariam ser atualizadas? Por que isso é um problema?
2. Se o veículo 42 mudar de placa, quantos registros precisam ser atualizados?
3. Se uma entrega for cancelada, **o que acontece com os dados do cliente** nessa entrega?
4. Liste as 4 dependências funcionais transitivas no formato `X → Y → Z`.

### Atividade 2.2: Normalize até a 3FN (grupo, 15 min)

Decomponham a tabela ENTREGA (que está em 2FN) até a **Terceira Forma Normal (3FN)**.

**Sua entrega deve conter:**

1. Lista de tabelas finais (mínimo: `cliente`, `veiculo`, `motorista`, `centro_distribuicao`, `entrega`).
2. Para cada tabela: PK e FKs.
3. Atualize o script SQL (`lodlog_modelo_dados_free.sql`) para que a tabela ENTREGA fique na 3FN.

### Atividade 2.3: Star Schema — ER vs. Analytics (grupo, 10 min)

> 💡 *O ER serve para garantir que tudo que é escrito está correto (transações). O Star Schema serve para que tudo que é lido seja rápido (análises). São complementares, não concorrentes.*

| Característica | Modelo ER (Transacional) | Star Schema (Analítico) |
|---|---|---|
| Objetivo principal | | |
| Número de tabelas | | |
| Tipo de JOIN | | |
| Granularidade | | |
| Uso de surrogate keys | | |
| Otimizado para | | |

Para as perguntas de negócio abaixo, indiquem quais tabelas do DW trariam a resposta:

1. Qual a taxa de pontualidade por centro de distribuição e por mês?
2. Qual o custo médio de frete por região e por tipo de veículo?
3. Quantos pedidos foram entregues com atraso por cliente no último trimestre?
4. Qual a distribuição de atrasos por categoria (Adiantado / No Prazo / Atraso Leve / Moderado / Crítico) por mês?
5. Qual a correlação entre a categoria de atraso e o score de segurança do motorista?

---

## Parte 3 — Mini-dimensão e Surrogate Keys (15 min)

### Atividade 3.1: Surrogate Keys — Por quê? (individual, 5 min)

| Tabela | Usa surrogate key? | Por que? |
|---|---|---|
| Fato entregas | | |
| Dimensão Tempo | | |
| Dimensão Cliente | | |
| Dimensão Veículo | | |
| Dimensão Categoria Atraso | | |

### Atividade 3.2: Mini-dimensão do KPI (grupo, 5 min)

> 💡 *Uma mini-dimensão é como uma "tabela de classificação" pequena e estável. Em vez de guardar a string "Atraso Crítico" em cada linha da fato (ocupando espaço e podendo mudar), você guarda um número inteiro que referencia uma tabela pequena de categorias. Se a descrição mudar, você altera só na tabela de categorias.'*

O script de seed (`lodlog_lab3_seed_free.py`) já criou a mini-dimensão `lodlog_dw.dim_cat_atraso` com 5 registros. Respondam:

1. **Por que** a categoria de atraso foi para uma mini-dimensão (e não na dim_tempo ou dim_motorista)?
2. A coluna `kpi_cat_atraso` aparece **duas vezes** no modelo: na entrega (operacional) e na fato_entregas (DW). Isso é redundância aceitável? Justifique.
3. A coluna `sla_violado` é uma flag booleana. Ela poderia virar uma dimensão separada (SCD Tipo 1)?

---

## Parte 4 — SQL DDL (20 min)

### Atividade 4.1: Substitua a Tabela Entrega no Script SQL (individual, 10 min)

1. Abra o script `lodlog_modelo_dados_free.sql` no Databricks Free Edition (Workspace > Import).
2. Localize o `CREATE TABLE lodlog_op.entrega` (que está em 2FN).
3. **Substitua-o** pela versão normalizada em 3FN — apenas com FKs e medidas (sem colunas redundantes).

### Atividade 4.2: Valide a Mini-Dimensão no DW (individual, 5 min) (opcional)

1. Query que conta quantas entregas tem cada categoria (JOIN de fato e cat_atraso).
2. Query que mostra a taxa de pontualidade por região (usando `dim_centro_distribuicao`).

Usem:
```sql
USE CATALOG workspace;
USE lodlog_dw;

SELECT c.regiao,
       SUM(CASE WHEN f.indicador_atraso = 0 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS taxa_pontualidade
FROM fato_entregas f
INNER JOIN dim_centro_distribuicao c ON f.sk_cd_origem = c.sk_cd
GROUP BY c.regiao;
```

### Atividade 4.3: Justifiquem suas Escolhas (grupo, 5 min)

1. Por que escolheram essa granularidade para a tabela fato?
2. Qual dimensão vai crescer mais? Como lidariam?
3. Se o negócio pedir uma nova categoria "Atraso Severíssimo" (> 24h), o que muda no modelo?

---

## ---- fim da parte obrigatória ----

## Material de Apoio e Referências

- **Conteúdo da Aula 2** (`aula-2.md`): NoSQL, DW/Lake/Lakehouse/Mesh/Fabric, Medallion/Zaloni, RPG "As Cinco Torres Isoladas".
- **Syllabus** (`syllabus.md`): seção Módulo 2.
- **Modelo de dados**: `lodlog_modelo_dados_free.sql` (DDL completa, nesta pasta — adaptada ao Databricks Free Edition).
- **RPG "As Cinco Torres Isoladas"** (materiais em `docs/Aulas-de-outros-cursos/Aula 8 Arquitetura de Dados/`) — pode substituir ou complementar esta parte.

**Dica do Professor:** O Star Schema não é "melhor" que o ER — são modelos para propósitos diferentes. O ER serve para operar (transações); o Star Schema serve para analisar (agregações). Um pipeline de dados bem projetado começa no ER dos sistemas transacionais (em 3FN) e termina no Star Schema do DW — com mini-dimensões para KPIs de baixa cardinalidade.

---

## Notas para o Facilitador

| Item | Detalhe |
|------|---------|
| **Duração total** | ~1h40 (100 min) |
| **Teoria** | Arquiteturas modernas, Medallion, NoSQL (~40 min) |
| **Prática** | Normalização, Star Schema, DDL (~60 min) |
| **Entrega** | Diagrama ER, DDL SQL, tabela Medallion preenchida |
| **Próxima aula** | 29/09 — Módulo 3: Cloud, Hadoop/Spark, Pipelines ETL/ELT |

**Conexão com o trabalho em grupo (30%):** O miniprojeto da Aula 4-5 exige que cada grupo projete um lakehouse Bronze→Silver→Gold — este lab é a base técnica para essa entrega.
