# LAB 1 — Mapeamento do Ecossistema de Dados e Fundamentos

**Disciplina** Arquitetura de Dados e Big Data
**Aula** 1 — Tipos de Dados e Contexto de Big Data
**Duração do Lab** \~1h30 (em aula)
**Entrega** Tabela de classificação preenchida + **ficha da sessão de desenho de arquitetura — a ADS (Architecture Design Session) — bloco 1 de 5** + reflexões em grupo

> **Para quem é este lab:** Você é um executivo ou analista que precisa entender *onde estão os dados da sua empresa* e *como eles fluem*. Não é preciso saber programar — é preciso saber pensar em dados. Este lab te ajuda a diagnosticar o que você já sabe e a alinhar essa visão com os conceitos que vamos construir nas próximas aulas.

---

## Antes de começar

- Releia rapidamente o **plano de ensino** da disciplina (Módulo 1, no eClass) e os slides da **Aula 1**.
- O cenário que vamos usar é a **LODLog Transportes e Distribuição S.A.** — uma empresa fictícia (mas bem realista) de logística com 450 veículos, 12 centros de distribuição e \~18 mil entregas por mês. Você vai analisar as 8 fontes de dados dela, exatamente como um consultor de dados faria no primeiro dia de um projeto.

### O fio condutor dos cinco labs: a ADS

Hoje começa a **ADS (Architecture Design Session, a sessão de desenho de arquitetura)** da LODLog — o método que James Serra descreve no capítulo 3 do livro-texto da disciplina. Uma ADS é uma conversa estruturada entre negócio e tecnologia que produz **duas coisas**: um rascunho de arquitetura e um plano de ação. Ela começa por uma **descoberta** de uma a duas horas, em que o arquiteto só faz perguntas — e **nenhuma delas cita produto**.

São **26 perguntas de descoberta**, distribuídas pelos cinco labs: 7 hoje, 5 no LAB 2, 7 no LAB 3, 5 no LAB 4 e as 2 últimas na Aula 5, quando tudo se fecha no **quadro branco** do miniprojeto. A redação completa de cada pergunta, o que ela decide e a evidência no caso LODLog estão em [`docs/ref/ADS-questionario-serra.md`](../../../docs/ref/ADS-questionario-serra.md).

> 📒 **Ficha ADS do grupo:** abram um documento compartilhado hoje com o título "Ficha ADS — LODLog". Ele cresce um bloco por lab e é o que vira o quadro branco da Aula 5. **Não apaguem nada entre os labs** — uma resposta de hoje pode ser contestada no LAB 3, e esse conflito é material de pitch.

---

## Objetivos de Aprendizagem

Ao final deste lab, você será capaz de:

1. **Diagnosticar** o ecossistema de dados de uma organização real.
2. **Distinguir** sistemas que registram transações (OLTP) daqueles que geram relatórios e insights (OLAP).
3. **Classificar** cada fonte de dados por tipo (estruturado, semiestruturado ou não estruturado).
4. **Avaliar** cada fonte pelos 5 Vs do Big Data (Volume, Velocidade, Variedade, Veracidade, Valor).
5. **Conduzir a descoberta de uma ADS**: responder, com evidência do caso, as sete primeiras perguntas do questionário — sem citar nenhum produto.
6. **Posicionar** serviços de nuvem nos modelos IaaS, PaaS e SaaS — e entender o que isso significa para o seu negócio.

---

## Parte 0 — Formação dos Grupos (5 min)

* Formar grupos de 5 a 6 integrantes.
* Escolher um **"Data Product Owner"** do grupo (quem vai apresentar e representar o grupo) e um **relator da Ficha ADS** (quem escreve as respostas das perguntas de descoberta, hoje e nos próximos labs).
* O facilitador vai distribuir os cenários de cada grupo (veja o final desta parte).

---

## Parte 1 — Linha do Tempo da Engenharia de Dados (10 min)

### Atividade 1.1: Cartão-Resposta Histórico, 6 min

Escolham **quatro** marcos da lista abaixo e respondam, para cada um, em **uma frase simples**: **"Por que isso mudou a forma como organizamos dados?"** Os demais ficam como revisão em casa (são material de prova).

> 💡 *Pense assim: cada um desses momentos foi um "salto" que permitiu que as empresas guardassem e usassem mais dados, de forma mais rápida e barata.*

| Marco | Sua resposta em 1 frase |
|---|---|
| Cartões perfurados (Hollerith, 1911) | |
| Fitas magnéticas (1951) | |
| Discos rígidos e acesso aleatório (anos 70) | |
| Modelo relacional de Codd (1970) | |
| Primeiro SGBD comercial — Oracle (1979) | |
| Data Warehouse (Inmon/Kimball, anos 90) | |
| Google File System / Big Data (2003+) | |
| Cloud computing e hipervisores (2006+) | |
| Transformers / IA Generativa (2017/2022) | |

### Atividade 1.2: Discussão em Grupo, 4 min

Discutam: **"Qual desses marcos foi mais importante para a Inteligência Artificial aplicada a negócios? Por quê?"**

Registrem a conclusão do grupo em **3 linhas** — será útil para a apresentação.

---

## Parte 2 — Transacional vs. Analítico (10 min)

> 💡 *Na prática do dia a dia, sua empresa tem dois "mundos" de dados: um que grava o que acontece agora (vendas, pedidos, sensores) e outro que olha para o passado para encontrar padrões e tomar decisões. Entender a diferença é o primeiro passo para não misturar as coisas.*

### Atividade 2.1: Classifique os Sistemas, 6 min

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

### Atividade 2.2: O sistema que vira os dois, 4 min

Apontem **um sistema que começa como transacional e vira analítico** — por exemplo, os dados de IoT, que nascem como "alguém está dirigindo" e viram "como dirigimos ao longo do mês". Escrevam a frase de virada em 2 linhas.

> 🏠 *Em casa (revisão para a prova): listem 3 sistemas transacionais que a LODLog provavelmente já possui e 2 sistemas analíticos que ela deveria ter.*

---

## Parte 3 — Os 5 Vs na LODLog (25 min)

> 💡 *Os "5 Vs" são a forma mais usada no mercado para descrever o desafio de Big Data. Não são apenas números — são perguntas de negócio que todo executivo deveria fazer sobre os dados da sua empresa.*

> 🔎 **Esta parte já é descoberta de ADS.** As linhas de Variedade, Volume e Velocidade respondem, fonte a fonte, às perguntas **ADS-04** (vai haver dado não relacional?), **ADS-05** (quanto dado precisa ser guardado?) e **ADS-06** (vai haver dado em streaming?). Preencham a matriz pensando já na resposta consolidada da Parte 5.

### Atividade 3.1: Preencha a Matriz dos 5 Vs (grupo, 15 min)

Para cada fonte de dados da LODLog, discutam e preencham o perfil nos 5 Vs e como ela se conecta com oportunidades de negócio e IA. Cada fonte tem sua própria tabela — respondam em 1 a 2 linhas por critério:

#### Fonte 1 — Sensores IoT da frota

| Critério | Resposta do grupo |
|----------|-------------------|
| Valor (insights) | |
| Veracidade (desafios) | |
| Variedade (formato) — *ADS-04* | |
| Velocidade — *ADS-06* | |
| Volume/dia — *ADS-05 e ADS-20* | |
| Conexão com IA/ML | |
| Pergunta do negócio que responde e com que pressa (minutos, horas, D-1) | |

#### Fonte 2 — Pedidos do TMS

| Critério | Resposta do grupo |
|----------|-------------------|
| Valor (insights) | |
| Veracidade (desafios) | |
| Variedade (formato) — *ADS-04* | |
| Velocidade — *ADS-06* | |
| Volume/dia — *ADS-05 e ADS-20* | |
| Conexão com IA/ML | |
| Pergunta do negócio que responde e com que pressa (minutos, horas, D-1) | |

#### Fonte 3 — Estoque do WMS

| Critério | Resposta do grupo |
|----------|-------------------|
| Valor (insights) | |
| Veracidade (desafios) | |
| Variedade (formato) — *ADS-04* | |
| Velocidade — *ADS-06* | |
| Volume/dia — *ADS-05 e ADS-20* | |
| Conexão com IA/ML | |
| Pergunta do negócio que responde e com que pressa (minutos, horas, D-1) | |

#### Fonte 4 — APIs externas (clima, tráfego)

| Critério | Resposta do grupo |
|----------|-------------------|
| Valor (insights) | |
| Veracidade (desafios) | |
| Variedade (formato) — *ADS-04* | |
| Velocidade — *ADS-06* | |
| Volume/dia — *ADS-05 e ADS-20* | |
| Conexão com IA/ML | |
| Pergunta do negócio que responde e com que pressa (minutos, horas, D-1) | |

#### Fonte 5 — Planilhas Excel do supervisor

| Critério | Resposta do grupo |
|----------|-------------------|
| Valor (insights) | |
| Veracidade (desafios) | |
| Variedade (formato) — *ADS-04* | |
| Velocidade — *ADS-06* | |
| Volume/dia — *ADS-05 e ADS-20* | |
| Conexão com IA/ML | |
| Pergunta do negócio que responde e com que pressa (minutos, horas, D-1) | |

#### Fonte 6 — Faturamento do ERP

| Critério | Resposta do grupo |
|----------|-------------------|
| Valor (insights) | |
| Veracidade (desafios) | |
| Variedade (formato) — *ADS-04* | |
| Velocidade — *ADS-06* | |
| Volume/dia — *ADS-05 e ADS-20* | |
| Conexão com IA/ML | |
| Pergunta do negócio que responde e com que pressa (minutos, horas, D-1) | |

#### Fonte 7 — Cotações da ANTT

| Critério | Resposta do grupo |
|----------|-------------------|
| Valor (insights) | |
| Veracidade (desafios) | |
| Variedade (formato) — *ADS-04* | |
| Velocidade — *ADS-06* | |
| Volume/dia — *ADS-05 e ADS-20* | |
| Conexão com IA/ML | |
| Pergunta do negócio que responde e com que pressa (minutos, horas, D-1) | |

#### Fonte 8 — IBGE (dados econômicos)

| Critério | Resposta do grupo |
|----------|-------------------|
| Valor (insights) | |
| Veracidade (desafios) | |
| Variedade (formato) — *ADS-04* | |
| Velocidade — *ADS-06* | |
| Volume/dia — *ADS-05 e ADS-20* | |
| Conexão com IA/ML | |
| Pergunta do negócio que responde e com que pressa (minutos, horas, D-1) | |

> 📌 *Dica: "Valor" é a pergunta que o negócio mais precisa responder. "Veracidade" é onde você desconfia dos dados. "Variedade" mostra se você precisa de um data lake (para juntar tudo) ou de um data warehouse tradicional.*

### Atividade 3.2: Priorização, 10 min

Dado o problema de negócio da LODLog (*"estamos perdendo dinheiro, mas não sabemos onde"*), ordenem as fontes acima por **prioridade de ingestão** (1 = mais urgente). Justifiquem a escolha das 3 primeiras pela linha "pressa": que dor em R$ cada uma ataca e quanto tempo o negócio aceita esperar?

> 💬 *Pergunta-guia: se você só pudesse ingerir 3 fontes de dados hoje, quais seriam e por quê?*
>
> 🔎 *Esta é a regra de ouro da ADS — **pensar grande, começar pequeno**. Guardem a lista: ela volta na Aula 5, quando o orçamento (ADS-17) e o prazo (ADS-18) entrarem na conversa.*

---

## Parte 4 — Nuvem e Modelos de Serviço (10 min)

> 💡 *Quando falamos de "nuvem", existem três formas principais de contratar tecnologia. Saber qual é qual evita desperdício — e é a base para entender onde seus dados vão morar.*

### Atividade 4.1: Classifique os Serviços (individual, 6 min)

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

> 💬 *Analogia rápida: IaaS = alugar o terreno e construir; SaaS = ficar num hotel onde só você escolhe a diária; PaaS = alugar o apartamento mobiliado.*

### Atividade 4.2: Onde mora cada sistema hoje (4 min)

Marquem, na tabela acima, quais desses modelos a LODLog **já usa hoje** e onde cada um dos 8 sistemas está hospedado: na nuvem, no datacenter da própria empresa (*on-premises*) ou nos dois. Essa marcação é a matéria-prima das perguntas ADS-01 e ADS-19 da próxima parte.

---

## Parte 5 — Ficha ADS: a descoberta da LODLog (30 min)

> 💡 *Agora vocês trocam de cadeira: deixam de ser alunos classificando fontes e passam a ser o arquiteto conduzindo a descoberta. **Regra única e inegociável: nenhuma resposta pode citar produto** ("vamos usar o Databricks" está proibido). A escolha de ferramenta vem depois, por cima das respostas — é assim que Serra separa diagnóstico de venda.*

### Atividade 5.1: Responder as sete perguntas (grupo, 20 min)

Respondam na Ficha ADS, **com a evidência ao lado** (um número do cenário, uma linha do [dossiê](../../../docs/LODLog/Por-que-esta-arquitetura.md) ou uma célula da matriz dos 5 Vs). Três respostas já estão prontas na Parte 3 — copiem a conclusão consolidada, não a tabela inteira.

| Código | Pergunta de descoberta | Resposta do grupo | Evidência |
|---|---|---|---|
| **ADS-01** | A LODLog já usa nuvem? Se usa pouco, o que segura? | | |
| **ADS-02** | Isto é uma solução nova ou uma migração do que já existe? | | |
| **ADS-04** | Vai haver dado **não relacional** (texto, JSON, imagem)? Quais fontes? | | |
| **ADS-05** | Quanto dado precisa ser guardado — e por quanto tempo? | | |
| **ADS-06** | Vai haver dado em **streaming**? Qual decisão piora se ele chegar uma hora depois? | | |
| **ADS-19** | As fontes estão na nuvem, no datacenter próprio (*on-premises*) ou nos dois? | | |
| **ADS-20** | Quanto dado precisa **entrar por dia**? Isso cabe numa janela de madrugada? | | |

Três armadilhas que o facilitador vai procurar nas respostas:

1. **ADS-02 respondida como "é nova".** A LODLog tem ERP, WMS e TMS rodando. Quase todo projeto de dados é, em parte, migração — e isso muda a conversa inteira.
2. **ADS-06 respondida com "tudo em tempo real".** Streaming fica sempre ligado e sempre custa. A pergunta não é "dá para ter?", é "que decisão de negócio piora sem ele?".
3. **ADS-05 confundida com ADS-20.** Guardar 50 terabytes é um problema de armazenamento; receber 800 mil eventos por dia é um problema de janela de carga. São dois desenhos diferentes.

### Atividade 5.2: Duas perguntas de volta (grupo, 5 min)

Serra lembra que, na descoberta, **quem mais fala é o cliente**. Escrevam **duas perguntas** que vocês fariam ao diretor de operações da LODLog e que **nenhuma das 26 perguntas do questionário cobre**. Elas entram no campo "estacionamento" do quadro branco da Aula 5 — e valem ponto no pitch se forem boas.

### Atividade 5.3: Fechamento da ficha (5 min)

- Confiram que as 7 linhas têm resposta **e** evidência. Linha sem evidência vira "a confirmar", não vira resposta inventada.
- Registrem no topo da ficha: data, grupo, relator.
- Uma frase de síntese: *"Pelo que ouvimos hoje, a LODLog precisa de uma arquitetura que ______, porque ______."* — sem nome de produto.

---

## Material de Apoio e Referências

- **Slides da Aula 1** (eClass): histórico, tipos de dados, OLTP vs OLAP, 5 Vs, fontes de dados da LODLog, a ADS e seus dois entregáveis.
- **Questionário da ADS** ([`docs/ref/ADS-questionario-serra.md`](../../../docs/ref/ADS-questionario-serra.md)): as 26 perguntas, o que cada uma decide e em que lab é respondida. Fonte: Serra (2024), cap. 3.
- **Dossiê "Por que esta arquitetura?"** ([`docs/LODLog/Por-que-esta-arquitetura.md`](../../../docs/LODLog/Por-que-esta-arquitetura.md)): as restrições da LODLog e a tabela dor → requisito.
- **Plano de ensino** (eClass): Módulo 1 — objetivos de aprendizagem e conteúdo programático.
- **Cenário LODLog**: `Labs/` — modelo de dados completo e descrição do cenário.

**Dica do Professor:** Não se preocupe em "acertar" a arquitetura agora. O objetivo do LAB 1 é **diagnosticar** o que o grupo já sabe e **alinhá-lo** com os conceitos da aula. A arquitetura evoluirá nos próximos labs — e a Ficha ADS é o fio que liga os cinco.

---
