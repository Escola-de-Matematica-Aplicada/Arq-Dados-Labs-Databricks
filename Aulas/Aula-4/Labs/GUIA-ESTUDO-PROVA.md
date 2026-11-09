# GUIA DE ESTUDO — Prova presencial de Arquitetura de Dados e Big Data (70%)

**1ª chamada:** 28/11/2026 · **2ª chamada:** 18/12/2026 · **Verificação suplementar:** 30/01/2027
**Formato:** presencial, individual — questões **objetivas** sobre os conceitos dos Módulos 1 a 3 e questões **dissertativas** aplicadas ao cenário LODLog, sobre o data lake que o seu grupo construiu.
**Local e horário:** confira no eClass.

> **Mudança de critério (06/11/2026):** a disciplina deixou de ser isenta de prova. A avaliação passou a ser **70% prova + 30% trabalho em grupo**, e o antigo relatório individual ("Avaliação pós-projeto do data lake da LODLog", 70%) **não é mais entregue** — o seu conteúdo é exatamente o que as dissertativas desta prova cobram. Se você já tinha começado o relatório, nada do seu trabalho se perdeu: ele virou o seu material de estudo.

> **O princípio da prova:** o grupo **construiu** o data lake sobre o seed do Databricks (70% pronto + 30% do grupo) e o **apresentou** na Aula 5. Na prova, você faz sozinho o que um líder de dados faz depois de um projeto: **avalia criticamente o que foi construído**, interpreta o resultado para o negócio, **trata o dado mais crítico como um ativo da empresa** e **explica como a organização vai mudar** para adotar a nova arquitetura. Responda como quem fala a um board: decisão, risco e valor antes de tecnologia, com a evidência ao lado de cada afirmação — o número da Etapa 8, o resultado do TODO 3, o fato do cenário.

**O que levar na cabeça:** os números do notebook do seu grupo (linhas por camada, quantas a qualidade barrou, o número da análise da Gold, o resultado do registro de ouro do cliente). As dissertativas pedem evidência concreta; quem não participou da construção não tem como respondê-las.

---

## Bloco objetivo — conceitos dos Módulos 1 a 3

- **Transversal (Módulos 1 a 4):** a **sessão de desenho de arquitetura (ADS)** de Serra — o que ela é, os dois entregáveis (rascunho de arquitetura e plano de ação), por que a descoberta vem antes da solução e por que nenhuma das 26 perguntas cita produto. Os cinco campos do quadro branco: objetivos priorizados, dores, arquitetura, assuntos em aberto e encaminhamentos.
- **Módulo 1:** tipos de dado (estruturado, semiestruturado, não estruturado); OLTP × OLAP; os **5 Vs**, com Veracidade em camadas; padrões de ingestão (batch, streaming, CDC, evento).
- **Módulo 2:** **Data Warehouse × Data Lake × Lakehouse × Data Mesh × Data Fabric** — o que cada um resolve, o que custa e quando usar; arquitetura **Medallion** (Bronze/Silver/Gold) e as zonas de refinamento; contratos de dados e governança federada (a "Ponte dos Contratos" do RPG da Aula 2).
- **Módulo 3:** modelos de serviço em nuvem (IaaS/PaaS/SaaS); Hadoop, Spark e Hive; **ETL × ELT**; **batch × streaming**; arquiteturas **Lambda × Kappa**; pipeline em camadas (ingestão → processamento → consumo).

---

## Bloco A — O que foi construído

1. **Cenário, pergunta e fontes**
   O cenário do seu grupo (A — Rotas, B — Manutenção preditiva, C — Estoque, D — Fraude em faturamento) e a pergunta de negócio. Saiba descrever **3 a 5 fontes** — as do seed que o cenário usa e as que faltaram (internas: ERP, WMS, TMS, IoT; externas: Maps, INMET, ANTT, IBGE): tipo de dado, formato, frequência e quem consome. Saiba dar os **5 Vs** das fontes principais, com um número cada; em Veracidade, onde o dado mente e qual camada barrou.

2. **A descoberta antes da solução**
   O que as 26 perguntas da ADS revelaram sobre a LODLog, lab a lab (a Ficha ADS do seu grupo): origem e natureza do dado, quem consome, como o dado se move, o que protege e o que não pode parar, orçamento e prazo. Saiba apontar **duas respostas que mudaram a arquitetura do grupo** e **uma pergunta que ficou "a confirmar"**, com o responsável. E saiba dizer por que a escolha de ferramenta só vem depois.

3. **As etapas percorridas**
   A construção e o uso do data lake **das fontes até o consumo**: o que veio pronto no seed, o que o grupo completou (os 5 TODOs) e os números da execução (Etapa 8 do notebook: linhas por camada e quantas a qualidade barrou). Saiba dizer, fonte a fonte, se a ingestão seria **batch, streaming ou CDC** em produção e por quê, e se o tratamento é ETL ou ELT.

## Bloco B — Avaliação pós-projeto

4. **O resultado para o negócio**
   A análise do grupo (TODO 3): o número, a interpretação e **a decisão que ele apoia**. Que limitações dos dados enfraquecem essa conclusão (amostra, período, dado simulado, regra de qualidade escolhida no TODO 1)? O que seria preciso para levar essa decisão ao board com confiança?

5. **Vantagens e limitações da arquitetura**
   Saiba avaliar a arquitetura adotada (Lakehouse Medallion num único workspace) em quatro lentes: **escala, custo, governança e risco de "pântano de dados"**. Use os 4 pilares da Aula 4 (qualidade, segurança/LGPD, metadados e glossário, ciclo de vida): o que o seed e o grupo cobriram e o que ficou descoberto. Saiba comparar com **ao menos uma alternativa** — Data Warehouse, Data Mesh, Data Fabric ou a **Ponte dos Contratos** do RPG da Aula 2 — e dizer em que condição da LODLog a alternativa seria melhor. Treine escrever **registros de decisão (ADRs)** — de armazenamento (D1/D2), de movimento (D4–D7) e de governança (D3/D8/D9) do [dossiê "Por que esta arquitetura?"](../../../docs/LODLog/Por-que-esta-arquitetura.md) —, cada um com a dor, as opções, a escolha, **o que se perde** e o **gatilho de revisão**. E treine o **contra-cenário** (seção 6 do dossiê): muda um fato da LODLog, muda a resposta.

6. **Lições aprendidas e próximos passos**
   Pelo menos **três lições** (técnicas, de negócio ou de trabalho em equipe), cada uma com o fato que a originou. E **uma escolha do desenho que você defende e uma que contestaria**, com os próximos passos para elevar a maturidade em dados da LODLog.

## Bloco C — O dado crítico

> No seed, o grupo tratou o dado mais crítico da LODLog — **o cliente e seu endereço** (Etapa 7B, TODO 5). Aqui a prova **estende essa visão para o seu cenário** e cobra as perguntas que a Aula 4 fez: *qual é o dado mais crítico? ele é gerenciado? o responsável sabe que é responsável? temos um catálogo?* (DMBOK caps. 3, 10, 12 e 13.)

6. **Identificação e responsabilidade**
   Qual é o **elemento crítico de dados** do seu cenário (por exemplo: a entrega e o prazo prometido em A; a leitura de temperatura em B; o saldo do SKU em C; o valor faturado em D) e **por que** ele é crítico — pelos critérios do DMBOK: relatório regulatório ou financeiro, operação, satisfação do cliente, estratégia, e o tamanho do prejuízo se ele estiver errado. De que **dados mestres** ele depende (cliente, veículo, CD)? Como ele é gerenciado hoje na LODLog e **quem deveria ser o dono e o steward**? Eles sabem disso? Como fazer com que soubessem?

7. **Conceito de negócio e glossário**
   Como o termo central do seu dado crítico **muda de significado entre áreas** (como "entrega" para o financeiro, o entregador, o cliente e a operação) e que números diferentes isso produz. A **definição oficial** para o glossário — termo, definição, regra de cálculo, dono e steward. **O que o catálogo precisa registrar sobre o dado crítico** — o que ele significa, de onde vem (sistema e camada) e quem responde por ele. Os dois termos que o grupo registrou no TODO 4 são o ponto de partida.

8. **Qualidade e registro de ouro**
   Para o dado crítico, **três regras de qualidade** com dimensão do DMBOK e limite (ex.: completude ≥ 98%), cada limite justificado pelo impacto no negócio. A decisão do TODO 5 (de onde vem o endereço oficial e o que é endereço válido): o que ela resolve, o que esconde e quem perde poder com ela — com o scorecard e a análise de impacto da Etapa 7B como evidência. E **onde a causa-raiz deve ser corrigida**: no pipeline ou no processo de quem digita?

## Bloco D — Maturidade, mudança organizacional e comunicação

> Arquitetura nova é mudança organizacional: muda quem decide, quem corrige e quem responde pelo número (DMBOK cap. 17, Aula 5).

9. **Maturidade e arquitetura empresarial**
   Onde a LODLog estava (silos, planilhas, as "cinco torres" da Aula 2) e aonde este data lake a leva. Que **capacidade de negócio** do cenário passa a ser medida, prevista ou automatizada? Que papéis de governança (dono de dados, steward, conselho) e que contratos de dados isso exige? Os gatilhos do roteiro D10 do dossiê dizem **quando** a arquitetura deve evoluir (por exemplo, para Data Mesh no plano 2028).

10. **Gestão da mudança e plano de comunicação**
    - **Diagnóstico (fórmula de Gleicher, mudança = D × V × F > R):** a insatisfação que já existe (com número), a **visão** em linguagem de negócio — e não "implantar o lakehouse" —, os **primeiros passos** concretos e as **resistências** esperadas (quem perde autonomia ou controle do próprio número).
    - **Riscos de Kotter:** os **dois erros** dos oito (Aula 5) mais prováveis na LODLog e como evitá-los. Mais uma **vitória rápida** que o board consiga ver em até 90 dias.
    - **Comunicação por público:** para diretoria, gerentes de CD, operadores do cadastro no TMS, motoristas, time comercial e TI — a **mensagem-chave** (o que muda para ele e por quê), o **canal**, a **frequência**, o **responsável** e o **indicador de adoção** (por exemplo: % de endereços cadastrados com número; consultas ao glossário).
    - **Como ancorar a mudança na cultura:** que incentivo, meta ou rotina faz o novo comportamento durar depois que o projeto acabar (por exemplo: o operador avaliado pela baixa correta, e não só pela velocidade).

---

## Checklist de estudo

- [ ] Sei o cenário e a pergunta de negócio do meu grupo em 1 parágrafo
- [ ] Sei citar 3–5 fontes e os 5 Vs com um número cada
- [ ] Sei o que a descoberta (as 26 perguntas da ADS) revelou, duas respostas que mudaram a arquitetura e uma que ficou "a confirmar" com responsável
- [ ] Sei desenhar de memória os cinco campos do quadro branco e dizer qual dor do meu quadro ficou sem ✔
- [ ] Sei separar o que veio pronto no seed do que o grupo construiu, com os números da Etapa 8
- [ ] Sei justificar batch/streaming/CDC e ETL/ELT fonte a fonte
- [ ] Sei o número da análise da Gold, a decisão que ele apoia e as limitações dos dados
- [ ] Sei avaliar a arquitetura em escala, custo, governança e risco de pântano
- [ ] Sei comparar com ao menos uma arquitetura alternativa e dizer quando ela venceria
- [ ] Sei escrever um ADR (dor, opções, escolha, o que se perde, gatilho) e um contra-cenário
- [ ] Tenho 3 lições aprendidas com o fato que as originou, 1 escolha defendida e 1 contestada
- [ ] Sei o dado crítico do meu cenário: por que é crítico, de que dados mestres depende, como é gerenciado hoje, dono e steward
- [ ] Sei o termo com significados divergentes entre áreas, a definição oficial para o glossário e o que o catálogo registra
- [ ] Sei três regras de qualidade com dimensão e limite justificados, e a decisão do registro de ouro (TODO 5)
- [ ] Sei a maturidade antes × depois, ligada a uma capacidade de negócio da LODLog
- [ ] Sei Gleicher (D, V, F e R), dois erros de Kotter e uma vitória rápida em até 90 dias
- [ ] Sei a mensagem por público (mensagem, canal, frequência, responsável, indicador de adoção)
- [ ] Revisei os conceitos dos Módulos 1 a 3 para o bloco objetivo

**Fora do escopo:** modelagem dimensional completa e feature engineering/treino de modelos de ML — são objeto de outras disciplinas. Se um modelo aparecer, trate-o como **consumidor da Gold** (como o motor preditivo do Lab 3).

**Critério de ouro:** toda afirmação de arquitetura com uma evidência ao lado — número ou fato do cenário. Na dúvida entre novidade e franqueza, escolha franqueza: "não testei X; testaria Y" é resposta de executivo.

---

## Material de estudo

| Onde | O que buscar |
|---|---|
| `lab4_miniprojeto_seed.py` (o notebook do seu grupo) | Os números da Etapa 8, o TODO 3 interpretado, o TODO 4 (glossário) e o TODO 5 (registro de ouro) |
| `LAB4.md` e `../aula-4.md` | Os 4 pilares de governança, o checklist de projeto e o pântano de dados |
| `../../Aula-5/aula-5.md` | Gleicher, os 8 erros de Kotter e o quadro de lições da turma |
| `../../../docs/LODLog/Por-que-esta-arquitetura.md` | As 6 forças, as decisões D1–D10 com o que se perde, os gatilhos e os contra-cenários |
| `../../../docs/ref/ADS-questionario-serra.md` | As 26 perguntas da sessão de desenho de arquitetura, o que cada uma decide e os cinco campos do quadro branco |
| `../../Aula-2/Labs/RPG-lodlog.md` | As 5 portas e a Ponte dos Contratos — a comparação entre arquiteturas |
| `../../Aula-3/Labs/LAB3.md` | A matriz de ingestão: batch × streaming × CDC e ETL × ELT justificados |
| `../../../docs/ementa/syllabus.md` | Bibliografia básica e complementar |
