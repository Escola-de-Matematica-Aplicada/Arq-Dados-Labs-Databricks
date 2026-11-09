# LAB 1 — Mapeamento do Ecossistema de Dados e Fundamentos

**Disciplina** Arquitetura de Dados e Big Data
**Aula** 1 — Tipos de Dados e Contexto de Big Data
**Duração do Lab** \~1h30 (em aula)
**Entrega** Tabela de classificação preenchida + reflexões em grupo

> **Para quem é este lab:** Você é um executivo ou analista que precisa entender *onde estão os dados da sua empresa* e *como eles fluem*. Não é preciso saber programar — é preciso saber pensar em dados. Este lab te ajuda a diagnosticar o que você já sabe e a alinhar essa visão com os conceitos que vamos construir nas próximas aulas.

---

## Antes de começar

- Releia rapidamente o **plano de ensino** da disciplina (Módulo 1, no eClass) e os slides da **Aula 1**.
- O cenário que vamos usar é a **LODLog Transportes e Distribuição S.A.** — uma empresa fictícia (mas bem realista) de logística com 450 veículos, 12 centros de distribuição e \~18 mil entregas por mês. Você vai analisar as 8 fontes de dados dela, exatamente como um consultor de dados faria no primeiro dia de um projeto.

---

## Objetivos de Aprendizagem

Ao final deste lab, você será capaz de:

1. **Diagnosticar** o ecossistema de dados de uma organização real.
2. **Distinguir** sistemas que registram transações (OLTP) daqueles que geram relatórios e insights (OLAP).
3. **Classificar** cada fonte de dados por tipo (estruturado, semiestruturado ou não estruturado).
4. **Avaliar** cada fonte pelos 5 Vs do Big Data (Volume, Velocidade, Variedade, Veracidade, Valor).
5. **Posicionar** serviços de nuvem nos modelos IaaS, PaaS e SaaS — e entender o que isso significa para o seu negócio.

---

## Parte 0 — Formação dos Grupos (5 min)

* Formar grupos de 5 a 6 integrantes.
* Escolher um **"Data Product Owner"** do grupo (quem vai apresentar e representar o grupo).
* O facilitador vai distribuir os cenários de cada grupo (veja o final desta parte).

---

## Parte 1 — Linha do Tempo da Engenharia de Dados (20 min)

### Atividade 1.1: Cartão-Resposta Histórico, 10 min

Para cada marco histórico abaixo, responda em **uma frase simples**: **"Por que isso mudou a forma como organizamos dados?"**

> 💡 *Pense assim: cada um desses momentos foi um "salto" que permitiu que as empresas guardassem e usassem mais dados, de forma mais rápida e barata.*

#### Cartões perfurados (Hollerith, 1911)

Sua Resposta (1 frase): ______________________________________________________

#### Fitas magnéticas (1951)

Sua Resposta (1 frase): ______________________________________________________

#### Discos rígidos e acesso aleatório (anos 70)

Sua Resposta (1 frase): ______________________________________________________

#### Modelo relacional de Codd (1970)

Sua Resposta (1 frase): ______________________________________________________

#### Primeiro SGBD comercial — Oracle (1979)

Sua Resposta (1 frase): ______________________________________________________

#### Data Warehouse (Inmon/Kimball, anos 90)

Sua Resposta (1 frase): ______________________________________________________

#### Google File System / Big Data (2003+)

Sua Resposta (1 frase): ______________________________________________________

#### Cloud computing e hipervisores (2006+)

Sua Resposta (1 frase): ______________________________________________________

#### Transformers / IA Generativa (2017/2022)

Sua Resposta (1 frase): ______________________________________________________

### Atividade 1.2: Discussão em Grupo, 10 min

Discutam: **"Qual desses marcos foi mais importante para a Inteligência Artificial aplicada a negócios? Por quê?"**

Registrem a conclusão do grupo em **3 a 5 linhas** — será útil para a apresentação.

---

## Parte 2 — Transacional vs. Analítico (20 min)

> 💡 *Na prática do dia a dia, sua empresa tem dois "mundos" de dados: um que grava o que acontece agora (vendas, pedidos, sensores) e outro que olha para o passado para encontrar padrões e tomar decisões. Entender a diferença é o primeiro passo para não misturar as coisas.*

### Atividade 2.1: Classifique os Sistemas, 10 min

Classifique cada sistema da LODLog como **Transacional (T)** ou **Analítico (A)**.

| Sistema | T ou A? |
|---------|---------|
| ERP que registra o pagamento de um pedido | |
| Dashboard de SLA de entregas do mês | |
| WMS que baixa o estoque no momento da expedição | |
| Modelo de ML que prediz atraso de entrega | |
| TMS que aloca um veículo a um pedido | |
| Relatório de ranking de CDs por eficiência | |
| API de IoT que recebe evento do sensor da frota | |
| Planilha Excel usada pelo supervisor para escalar motoristas | |

### Atividade 2.2: Mapeamento LODLog, 10 min

No cenário da LODLog, liste:

1. **3 sistemas transacionais** que a empresa provavelmente já possui.
2. **2 sistemas analíticos** que ela deveria ter.
3. **1 sistema que começa como transacional e vira analítico** — ex: os dados de IoT, que nascem como "alguém está dirigindo" e viram "como dirigimos ao longo do mês".

---

## Parte 3 — Os 5 Vs na LODLog (25 min)

> 💡 *Os "5 Vs" são a forma mais usada no mercado para descrever o desafio de Big Data. Não são apenas números — são perguntas de negócio que todo executivo deveria fazer sobre os dados da sua empresa.*

### Atividade 3.1: Preencha a Matriz dos 5 Vs (grupo, 15 min)

Para cada fonte de dados da LODLog, discutam e preencham o perfil nos 5 Vs e como ela se conecta com oportunidades de negócio e IA. Cada fonte tem sua própria tabela — respondam em 1 a 2 linhas por critério:

#### Fonte 1 — Sensores IoT da frota

| Critério | Resposta do grupo |
|----------|-------------------|
| Valor (insights) | |
| Veracidade (desafios) | |
| Variedade (formato) | |
| Velocidade | |
| Volume/dia | |
| Conexão com IA/ML | |
| Pergunta do negócio que responde e com que pressa (minutos, horas, D-1) | |

#### Fonte 2 — Pedidos do TMS

| Critério | Resposta do grupo |
|----------|-------------------|
| Valor (insights) | |
| Veracidade (desafios) | |
| Variedade (formato) | |
| Velocidade | |
| Volume/dia | |
| Conexão com IA/ML | |
| Pergunta do negócio que responde e com que pressa (minutos, horas, D-1) | |

#### Fonte 3 — Estoque do WMS

| Critério | Resposta do grupo |
|----------|-------------------|
| Valor (insights) | |
| Veracidade (desafios) | |
| Variedade (formato) | |
| Velocidade | |
| Volume/dia | |
| Conexão com IA/ML | |
| Pergunta do negócio que responde e com que pressa (minutos, horas, D-1) | |

#### Fonte 4 — APIs externas (clima, tráfego)

| Critério | Resposta do grupo |
|----------|-------------------|
| Valor (insights) | |
| Veracidade (desafios) | |
| Variedade (formato) | |
| Velocidade | |
| Volume/dia | |
| Conexão com IA/ML | |
| Pergunta do negócio que responde e com que pressa (minutos, horas, D-1) | |

#### Fonte 5 — Planilhas Excel do supervisor

| Critério | Resposta do grupo |
|----------|-------------------|
| Valor (insights) | |
| Veracidade (desafios) | |
| Variedade (formato) | |
| Velocidade | |
| Volume/dia | |
| Conexão com IA/ML | |
| Pergunta do negócio que responde e com que pressa (minutos, horas, D-1) | |

#### Fonte 6 — Faturamento do ERP

| Critério | Resposta do grupo |
|----------|-------------------|
| Valor (insights) | |
| Veracidade (desafios) | |
| Variedade (formato) | |
| Velocidade | |
| Volume/dia | |
| Conexão com IA/ML | |
| Pergunta do negócio que responde e com que pressa (minutos, horas, D-1) | |

#### Fonte 7 — Cotações da ANTT

| Critério | Resposta do grupo |
|----------|-------------------|
| Valor (insights) | |
| Veracidade (desafios) | |
| Variedade (formato) | |
| Velocidade | |
| Volume/dia | |
| Conexão com IA/ML | |
| Pergunta do negócio que responde e com que pressa (minutos, horas, D-1) | |

#### Fonte 8 — IBGE (dados econômicos)

| Critério | Resposta do grupo |
|----------|-------------------|
| Valor (insights) | |
| Veracidade (desafios) | |
| Variedade (formato) | |
| Velocidade | |
| Volume/dia | |
| Conexão com IA/ML | |
| Pergunta do negócio que responde e com que pressa (minutos, horas, D-1) | |

> 📌 *Dica: "Valor" é a pergunta que o negócio mais precisa responder. "Veracidade" é onde você desconfia dos dados. "Variedade" mostra se você precisa de um data lake (para juntar tudo) ou de um data warehouse tradicional.*

### Atividade 3.2: Priorização, 10 min

Dado o problema de negócio da LODLog (*"estamos perdendo dinheiro, mas não sabemos onde"*), ordenem as fontes acima por **prioridade de ingestão** (1 = mais urgente). Justifiquem a escolha das 3 primeiras pela linha "pressa": que dor em R$ cada uma ataca e quanto tempo o negócio aceita esperar?

> 💬 *Pergunta-guia: se você só pudesse ingerir 3 fontes de dados hoje, quais seriam e por quê?*

---

## Parte 4 — Nuvem e Modelos de Serviço (20 min)

> 💡 *Quando falamos de "nuvem", existem três formas principais de contratar tecnologia. Saber qual é qual evita desperdício — e é a base para entender onde seus dados vão morar.*

### Atividade 4.1: Classifique os Serviços (individual, 10 min)

Classifique cada serviço/tecnologia como **IaaS**, **PaaS**, **SaaS** ou **On-Premise**:

| Serviço/Tecnologia | IaaS / PaaS / SaaS / On-Prem? |
|---|---|
| Servidor físico no datacenter da empresa | |
| Amazon EC2 (máquina virtual) | |
| Amazon RDS (banco gerenciado) | |
| Power BI Online | |
| Databricks Free Edition | |
| PostgreSQL instalado em um EC2 | |
| Snowflake | |
| Excel instalado no computador do usuário | |

> 💬 *Analogia rápida: IaaS = alugar o terreno e construir; PaaS = alugar o apartamento mobiliado; SaaS = ficar num hotel onde só você escolhe a diária.*

### Atividade 4.2: Reflexão em grupo, 10 min

1. Qual desses serviços a LODLog já deve estar usando hoje?
2. Para onde a empresa deveria migrar nos próximos 3 anos, se o volume de dados triplicar? Considerem as restrições do [dossiê](../../../docs/LODLog/Por-que-esta-arquitetura.md) (seção 2.2): 5 pessoas em dados e o hosting do ERP vencendo em 14 meses.

---

## Material de Apoio e Referências

- **Slides da Aula 1** (eClass): histórico, tipos de dados, OLTP vs OLAP, 5 Vs, fontes de dados da LODLog.
- **Dossiê "Por que esta arquitetura?"** ([`docs/LODLog/Por-que-esta-arquitetura.md`](../../../docs/LODLog/Por-que-esta-arquitetura.md)): as restrições da LODLog e a tabela dor → requisito.
- **Plano de ensino** (eClass): Módulo 1 — objetivos de aprendizagem e conteúdo programático.
- **Cenário LODLog**: `Labs/` — modelo de dados completo e descrição do cenário.

**Dica do Professor:** Não se preocupe em "acertar" a arquitetura agora. O objetivo do LAB 1 é **diagnosticar** o que o grupo já sabe e **alinhá-lo** com os conceitos da aula. A arquitetura evoluirá nos próximos labs.
