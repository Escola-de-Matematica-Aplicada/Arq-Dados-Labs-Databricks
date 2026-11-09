# Questionário da ADS (Architecture Design Session) — mapa para os labs da disciplina

**Fonte:** SERRA, James. *Deciphering Data Architectures: Choosing Between a Modern Data Warehouse,
Data Fabric, Data Lakehouse, and Data Mesh*. Sebastopol: O'Reilly, 2024 — capítulo 3, "The
Architecture Design Session". No repositório do professor, o texto integral está em
`docs/ref/Deciphering-Data-Architectures-Book.md`, linhas \~1194–1700.

**Para que serve este arquivo:** é a fonte única das 26 perguntas de descoberta da ADS
(*Architecture Design Session*, a sessão de desenho de arquitetura) usadas na disciplina. Cada
pergunta recebe um código `ADS-NN`, é respondida em um lab específico sobre o caso **LODLog**, e
todas se encontram no **quadro branco** do miniprojeto, na Aula 5. Os labs citam os códigos; a
redação canônica da pergunta e o "o que ela decide" ficam aqui.

---

## 1. O que é uma ADS, segundo Serra

Uma ADS é uma **discussão estruturada** entre as áreas de negócio e de tecnologia, conduzida por um
arquiteto, para definir o desenho de alto nível de uma solução de dados. Não é workshop técnico,
nem treinamento, nem demonstração de produto, nem levantamento detalhado de requisitos.

Ela produz **dois entregáveis**:

1. uma **arquitetura** (um "blueprint") que serve de ponto de partida para a solução;
2. um **plano de ação de alto nível** — demonstrações, provas de conceito e decisões de produto.

Três regras do capítulo que valem para a disciplina inteira:

- **Descoberta antes de solução.** Serra passa uma a duas horas só perguntando; nenhuma das 26
  perguntas cita produto. A escolha de ferramenta vem depois, por cima das respostas.
- **Pensar grande, começar pequeno.** A arquitetura pode prever dezenas de fontes; o primeiro
  passo escolhe duas ou três de alto valor e baixo esforço.
- **Quadro branco, não slides.** O artefato da sessão é um quadro com objetivos priorizados,
  dores, o rascunho da arquitetura, o "estacionamento" (assuntos fora de tema) e os
  encaminhamentos. Toda dor listada tem que estar resolvida — ou ter reunião marcada — no fim.

---

## 2. Distribuição das 26 perguntas pelos labs

| Lab | Aula | Lente da aula | Perguntas |
|---|---|---|---|
| LAB 1 | 1 — Tipos de dados e contexto de Big Data | De onde vem o dado, de que tipo, em que volume e velocidade | ADS-01, ADS-02, ADS-04, ADS-05, ADS-06, ADS-19, ADS-20 |
| LAB 2 | 2 — Ferramentas e arquiteturas | Quem consome e como — o que decide entre Warehouse, Lake, Lakehouse e Mesh | ADS-07, ADS-08, ADS-15, ADS-16, ADS-26 |
| LAB 3 | 3 — Organização e manuseio (pipelines) | Como o dado se move, com que prazo e com que time | ADS-03, ADS-09, ADS-10, ADS-21, ADS-22, ADS-23, ADS-25 |
| LAB 4 | 4 — Governança | O que protege, o que não pode parar e qual é o dado mestre | ADS-11, ADS-12, ADS-13, ADS-14, ADS-24 |
| Miniprojeto | 5 — Conclusão e apresentação | As restrições que forçam "pensar grande, começar pequeno" + o quadro branco | ADS-17, ADS-18 + consolidação das 26 |

> As respostas são **acumulativas**: a ficha de cada lab entra na "Ficha ADS da LODLog" do grupo, e
> é ela que vira o quadro branco do pitch da Aula 5.

---

## 3. As 26 perguntas

Cada item traz a pergunta como ela é feita ao cliente, **o que ela decide na arquitetura** (síntese
do comentário de Serra) e **onde está a evidência no caso LODLog** — o dossiê citado é
[`docs/LODLog/Por-que-esta-arquitetura.md`](../LODLog/Por-que-esta-arquitetura.md).

### LAB 1 — Aula 1: a natureza e a origem do dado

| Código | Pergunta | O que ela decide | Evidência na LODLog |
|---|---|---|---|
| **ADS-01** | A empresa já usa nuvem? | Se não usa, a conversa começa pelo motivo da resistência — quase sempre uma objeção vencida (segurança, custo). | Dossiê 2.2: equipe de 5 pessoas; sem gente de dados nos 12 centros de distribuição. |
| **ADS-02** | A solução é nova ou é uma migração? | Migração traz uma conversa inteira sobre como mover o que já existe, com o legado no ar. | Hosting do ERP (Enterprise Resource Planning, o sistema que registra pedidos e faturamento) vence em 14 meses. |
| **ADS-04** | Vai haver dado **não relacional**? | É a pergunta da *Variedade*. Qualquer fonte semi ou não estruturada já exige um data lake. | Sensores, ocorrências em texto livre, APIs de clima e trânsito. |
| **ADS-05** | Quanto dado precisa ser guardado? | É a pergunta do *Volume*: define particionamento, formato e o risco de consulta lenta. | \~26 milhões de eventos de sensor por mês. |
| **ADS-06** | Vai haver dado em **streaming**? | É a pergunta da *Velocidade*: define se entram produtos de evento contínuo ou se lote resolve. | Só 2 das 7 perguntas de negócio pedem resposta em minutos. |
| **ADS-19** | A origem do dado está na nuvem, no local (*on-premises*) ou nos dois? | Fonte no local exige um canal de saída para a nuvem, e o volume pode forçar mudança de desenho. | ERP no data center próprio; WMS em 12 instalações e 3 versões. |
| **ADS-20** | Quanto dado precisa entrar por dia? | Define a janela de carga: se não cabe na madrugada, a carga passa a ser horária ou paralela. | \~860 mil eventos de sensor/dia + \~600 entregas/dia. |

### LAB 2 — Aula 2: quem consome e como

| Código | Pergunta | O que ela decide | Evidência na LODLog |
|---|---|---|---|
| **ADS-07** | Vão usar painéis e/ou consultas livres (*ad hoc*)? | Painel exige resposta em milissegundos; consulta livre exige dado aberto e documentado. | Diretoria quer o SLA do mês; operação quer cruzar o dia. |
| **ADS-08** | As consultas serão em lote e/ou interativas? | Define o tipo de armazenamento e quanto poder de cálculo precisa ficar ligado. | Fechamento mensal (lote) × ranking de centros de distribuição (interativo). |
| **ADS-15** | Quantos usuários simultâneos no pico? E na média? | Vários produtos têm teto de concorrência; o desenho evita encostar nesse teto. | 12 centros de distribuição + diretoria; pico no fechamento. |
| **ADS-16** | Qual é o nível técnico dos usuários finais? | Usuário leigo puxa a arquitetura para o modelo dimensional e o pouco código; usuário técnico permite o lakehouse cru. | Supervisores que hoje trabalham em planilha. |
| **ADS-26** | Quanto de autoatendimento em BI (Business Intelligence, relatórios e painéis feitos pelo próprio usuário) se quer? | Muito autoatendimento com usuário leigo empurra para Data Warehouse relacional e *star schema*; usuário técnico aceita o lakehouse. | A planilha do supervisor é autoatendimento sem governança. |

### LAB 3 — Aula 3: como o dado se move

| Código | Pergunta | O que ela decide | Evidência na LODLog |
|---|---|---|---|
| **ADS-03** | Quais são as competências do time de engenharia? | Ferramenta que o time já conhece custa menos treinamento — e muda a recomendação de produto. | 5 pessoas na equipe de dados, sem especialista em evento contínuo. |
| **ADS-09** | Em quanto tempo os relatórios precisam rodar? Existe SLA (Service Level Agreement, prazo acordado) escrito? | Milissegundos ou minutos mudam a arquitetura, os produtos e quantas cópias do dado são necessárias. | Multa contratual por atraso; relatório que hoje chega em D+5. |
| **ADS-10** | O dado vai alimentar análise preditiva ou aprendizado de máquina? | Se sim, a coleta precisa preservar o histórico que treina o modelo. | Motor de risco de atraso (LAB 3) e manutenção preditiva. |
| **ADS-21** | Quais são as dores atuais de desempenho, escala, armazenamento, concorrência e tempo de consulta? | É a lista que o quadro branco precisa riscar no fim: ninguém troca de arquitetura para continuar com o mesmo problema. | Relatório em D+5; planilha que trava; número de atraso divergente entre áreas. |
| **ADS-22** | Querem usar ferramentas de terceiros e/ou de código aberto? | Quase nenhum cliente fica só no catálogo de um provedor; abre espaço para o que o time já domina. | Formatos abertos evitam o aprisionamento citado na decisão D4. |
| **ADS-23** | Aceitam produtos em *preview* (ainda não liberados em versão final)? | Antecipa recurso novo, mas com risco de falha, de falta de suporte e de preço indefinido. | Retorno exigido em até 18 meses: pouca tolerância a risco de produto. |
| **ADS-25** | Movimentar o dado é um problema? | Muitas origens, ou mistura de nuvem e local, mudam a decisão de ingestão (por exemplo, replicação). | 8 fontes, 3 versões de WMS, APIs externas com limite de requisição. |

### LAB 4 — Aula 4: proteção, continuidade e dado mestre

| Código | Pergunta | O que ela decide | Evidência na LODLog |
|---|---|---|---|
| **ADS-11** | Quais são os requisitos de alta disponibilidade e de recuperação de desastre — RTO (Recovery Time Objective, em quanto tempo o serviço precisa voltar) e RPO (Recovery Point Objective, quanto de dado se aceita perder)? | Exigência alta pode forçar réplicas e mudanças grandes no desenho; a pergunta também faz o cliente pensar no assunto pela primeira vez. | Disputa de multa exige provar entrega de até 24 meses atrás. |
| **ADS-12** | É preciso **dado mestre** (MDM — Master Data Management, o registro único de cada cliente, lugar ou produto)? | Se sim, o MDM entra no desenho como componente, não como arrumação posterior. | Cliente e endereço cadastrados de três jeitos (ERP, TMS, CRM) — TODO 5 do LAB 4. |
| **ADS-13** | Há limitação de segurança, definida em contrato com clientes, para guardar dado na nuvem? | Contrato pode proibir a saída do dado do país ou a ida de dado pessoal para a nuvem — e isso muda a arquitetura. | 40 clientes concentram 62% da receita e impõem cláusulas próprias. |
| **ADS-14** | A solução exige acesso 24 horas por dia, 7 dias por semana? | Se exige, não pode haver janela de manutenção para carregar e limpar dado. | Operação de transporte roda de madrugada e em fim de semana. |
| **ADS-24** | Quais são os requisitos de segurança? Há exigência de soberania de dados (o dado não pode sair do país)? | Pode exigir criptografia, controles extras ou mais de um data lake. | Plano 2028 prevê operação em 2 países. |

### Aula 5 — miniprojeto: as restrições e o fechamento

| Código | Pergunta | O que ela decide | Evidência na LODLog |
|---|---|---|---|
| **ADS-17** | Qual é o orçamento? | Orçamento curto obriga a trocar desempenho por custo; é o que transforma "pensar grande" em "começar pequeno". | R$ 1,6 milhão no primeiro ano. |
| **ADS-18** | Qual é o prazo planejado? | Prazo longo permite esperar produto que ainda vai ser lançado; prazo curto fecha o escopo no que existe hoje. | Retorno exigido em até 18 meses. |

---

## 4. O quadro branco (o artefato da Aula 5)

Serra fecha a ADS com um quadro — não com slides. É isso que o miniprojeto entrega, em cinco
campos:

| Campo do quadro | O que entra | De onde vem na disciplina |
|---|---|---|
| **Objetivos priorizados** | o que o grupo quer que a arquitetura entregue, em ordem | pergunta de negócio do sub-cenário (LAB 4) |
| **Dores** | a lista de ADS-21, com um ✔ em cada dor que a arquitetura proposta resolve | LAB 3 e LAB 4 |
| **Arquitetura (rascunho)** | fontes → Bronze → Silver → Gold → consumo, com o que veio pronto e o que o grupo construiu | seed do LAB 4 |
| **Estacionamento** | o que apareceu e é assunto de outra sessão (modelagem dimensional completa, engenharia de atributos para modelos, DevOps) | o "fora de escopo" da disciplina |
| **Encaminhamentos** | o que o grupo faria em seguida, com responsável: prova de conceito, nova fonte, conversa com área | plano de ação de alto nível (2º entregável da ADS) |

E o **plano de ação**, que acompanha o quadro: "pensar grande, começar pequeno" — das fontes
mapeadas no LAB 1, quais **duas ou três** entram primeiro, considerando ADS-17 (orçamento) e
ADS-18 (prazo), e por quê.

---

## 5. O que a disciplina deliberadamente não usa do capítulo

O capítulo 3 também trata da **preparação** e da **condução** da sessão (logística, pré-chamada com
o time de conta, lista de participantes, apresentações, pausas, o e-mail de fechamento, a pesquisa
de satisfação e as dicas de facilitação remota). Isso é ofício de consultoria e fica fora dos labs,
com duas exceções, que aparecem na Aula 1:

- as **quatro perguntas da pré-chamada** ("é isto que eu entendi…", "quem vem à sessão…", "o que
  vocês têm para me mostrar…", "o que seria uma boa sessão para vocês…"), porque são o modelo do
  briefing que o grupo recebe no LAB 1;
- a regra de **não falar de produto na descoberta**, porque é o que separa o diagnóstico da venda —
  e é cobrada nas dissertativas da prova.
