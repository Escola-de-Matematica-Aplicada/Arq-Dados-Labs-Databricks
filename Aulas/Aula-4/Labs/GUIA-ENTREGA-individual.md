# GUIA DE ENTREGA INDIVIDUAL — Avaliação pós-projeto do data lake da LODLog (70%)

**Prazo:** 08/12/2026 (15 dias após a última aula, a Aula 5) · **Formato:** PDF, até ~10 páginas (ou deck equivalente)
**Título do documento:** *"Avaliação pós-projeto do data lake da LODLog — [seu nome] — Cenário [A/B/C/D]"*

> **O princípio desta entrega:** o grupo **construiu** o data lake sobre o seed do Databricks (70% pronto + 30% do grupo) e o **apresentou** na Aula 5. Agora você, sozinho, faz o que um líder de dados faz depois de um projeto: **avalia criticamente o que foi construído**, interpreta o resultado para o negócio, **trata o dado mais crítico como um ativo da empresa** e **planeja como a organização vai mudar** para adotar a nova arquitetura. Escreva para convencer um board, com evidência ao lado de cada afirmação. **Não se exige código novo.**

---

## Parte A — O que foi construído (20%)

1. **Cenário, pergunta e fontes — 8%**
   O cenário do grupo (A — Rotas, B — Manutenção preditiva, C — Estoque, D — Fraude em faturamento) e a pergunta de negócio. Uma tabela com **3 a 5 fontes** — as do seed que o cenário usa e as que faltaram (internas: ERP, WMS, TMS, IoT; externas: Maps, INMET, ANTT, IBGE): tipo de dado, formato, frequência e quem consome. Inclua os **5 Vs** das fontes principais, com um número cada; em Veracidade, diga onde o dado mente e qual camada barrou.

2. **As etapas percorridas — 12%**
   Descreva a construção e o uso do data lake **das fontes até o consumo**: o que veio pronto no seed, o que o grupo completou (os 5 TODOs) e os números da execução (Etapa 8 do notebook: linhas por camada e quantas a qualidade barrou). Diga, fonte a fonte, se a ingestão seria **batch, streaming ou CDC** em produção e por quê, e se o tratamento é ETL ou ELT.

## Parte B — Avaliação pós-projeto (35%)

3. **O resultado para o negócio — 10%**
   Retome a análise do grupo (TODO 3): o número, a interpretação e **a decisão que ele apoia**. Quais limitações dos dados enfraquecem essa conclusão (amostra, período, dado simulado, regra de qualidade escolhida no TODO 1)? O que você precisaria para levar essa decisão ao board com confiança?

4. **Vantagens e limitações da arquitetura — 15%**
   Avalie a arquitetura adotada (Lakehouse Medallion num único workspace) em quatro lentes: **escala, custo, governança e risco de "pântano de dados"**. Use os 4 pilares da Aula 4 (qualidade, segurança/LGPD, metadados e glossário, ciclo de vida): o que o seed e o grupo cobriram e o que ficou descoberto. Compare com **ao menos uma alternativa** — Data Warehouse, Data Mesh, Data Fabric ou a **Ponte dos Contratos** do RPG da Aula 2 — e diga em que condição da LODLog a alternativa seria melhor. Organize a avaliação em **três registros de decisão (ADRs)** — um de armazenamento (D1/D2), um de movimento (D4–D7) e um de governança (D3/D8/D9) do [dossiê "Por que esta arquitetura?"](../../../docs/LODLog/Por-que-esta-arquitetura.md) —, cada um com a dor, as opções, a escolha, o que se perde e o gatilho de revisão. Feche com **um contra-cenário** (seção 6 do dossiê): mude um fato da LODLog e mostre que a resposta muda.

5. **Lições aprendidas e próximos passos — 10%**
   Pelo menos **três lições** (técnicas, de negócio ou de trabalho em equipe), cada uma com o fato que a originou. Termine com **uma escolha do desenho que você defende e uma que contestaria**, e com os próximos passos para elevar a maturidade em dados da LODLog.

## Parte C — O dado crítico (20%)

> No seed, o grupo tratou o dado mais crítico da LODLog — **o cliente e seu endereço** (Etapa 7B, TODO 5). Aqui você **estende essa visão para o seu cenário** e responde às perguntas que a Aula 4 fez: *qual é o dado mais crítico? ele é gerenciado? o responsável sabe que é responsável? temos um catálogo?* (DMBOK caps. 3, 10, 12 e 13.)

6. **Identificação e responsabilidade — 8%**
   Qual é o **elemento crítico de dados** do seu cenário (por exemplo: a entrega e o prazo prometido em A; a leitura de temperatura em B; o saldo do SKU em C; o valor faturado em D) e **por que** ele é crítico — use os critérios do DMBOK: relatório regulatório ou financeiro, operação, satisfação do cliente, estratégia, e o tamanho do prejuízo se ele estiver errado. De que **dados mestres** ele depende (cliente, veículo, CD)? Como ele é gerenciado hoje na LODLog e **quem deveria ser o dono e o steward**? Eles sabem disso? Como você faria com que soubessem?

7. **Conceito de negócio e glossário — 6%**
   Mostre como o termo central do seu dado crítico **muda de significado entre áreas** (como "entrega" para o financeiro, o entregador, o cliente e a operação) e que números diferentes isso produz. Proponha a **definição oficial** para o glossário — termo, definição, regra de cálculo, dono e steward. Diga **o que o catálogo precisa registrar sobre o dado crítico** — o que ele significa, de onde vem (sistema e camada) e quem responde por ele — e onde a definição oficial fica nesse catálogo. Use os dois termos que o grupo registrou no TODO 4 como ponto de partida.

8. **Qualidade e registro de ouro — 6%**
   Para o dado crítico, defina **três regras de qualidade** com dimensão do DMBOK e limite (ex.: completude ≥ 98%), cada limite justificado pelo impacto no negócio. Avalie a decisão do TODO 5 (de onde vem o endereço oficial e o que é endereço válido): o que ela resolve, o que esconde e quem perde poder com ela. Use o scorecard e a análise de impacto da Etapa 7B como evidência. **Onde a causa-raiz deve ser corrigida** — no pipeline ou no processo de quem digita?

## Parte D — Maturidade, mudança organizacional e plano de comunicação (20%)

> Arquitetura nova é mudança organizacional: muda quem decide, quem corrige e quem responde pelo número (DMBOK cap. 17, Aula 5). Esta parte transforma a sua recomendação em um plano que a LODLog consiga executar.

9. **Maturidade e arquitetura empresarial — 5%**
   Onde a LODLog estava (silos, planilhas, as "cinco torres" da Aula 2) e aonde este data lake a leva. Que **capacidade de negócio** do cenário passa a ser medida, prevista ou automatizada? Que papéis de governança (dono de dados, steward, conselho) e que contratos de dados isso exige? Use os gatilhos do roteiro D10 do dossiê para dizer **quando** a arquitetura deve evoluir (por exemplo, para Data Mesh no plano 2028). *Opcional: um parágrafo comparando com a empresa onde você trabalha.*

10. **Plano de comunicação e gestão da mudança — 15%**
    - **Diagnóstico da mudança (fórmula de Gleicher, mudança = D × V × F > R):** a insatisfação que já existe (com número), a **visão** em linguagem de negócio — e não "implantar o lakehouse" —, os **primeiros passos** concretos e as **resistências** esperadas (quem perde autonomia ou controle do próprio número).
    - **Riscos de Kotter:** os **dois erros** dos oito (Aula 5) mais prováveis na LODLog e como você os evita. Inclua uma **vitória rápida** que o board consiga ver em até 90 dias.
    - **Matriz de comunicação** (tabela): para cada público — diretoria, gerentes de CD, operadores do cadastro no TMS, motoristas, time comercial, TI —, a **mensagem-chave** (o que muda para ele e por quê), o **canal**, a **frequência**, o **responsável** e o **indicador de adoção** (por exemplo: % de endereços cadastrados com número; consultas ao glossário).
    - **Como ancorar a mudança na cultura:** que incentivo, meta ou rotina faz o novo comportamento durar depois que o projeto acabar (por exemplo: o operador avaliado pela baixa correta, e não só pela velocidade).

## Comunicação executiva (5%)

Linguagem de board: decisão, risco e valor antes de tecnologia; sem jargão não explicado; uma figura vale mais que um parágrafo.

---

## Anexo técnico (opcional)

Se quiser ir além, **evolua o notebook do grupo** — mais uma fonte até a Gold, uma segunda regra de qualidade, um teste de "E se" — no **Databricks Free Edition**, a plataforma única dos labs da disciplina. Até 4 páginas de prints, com a data de execução. O anexo não é necessário para a nota máxima; ele **conta como evidência** das Partes A e B.

---

## Checklist

- [ ] Cenário e pergunta de negócio em 1 parágrafo
- [ ] Tabela com 3–5 fontes e os 5 Vs com um número cada
- [ ] Etapas percorridas: o que veio pronto × o que o grupo construiu, com os números da Etapa 8
- [ ] Batch/streaming/CDC e ETL/ELT justificados fonte a fonte
- [ ] Resultado da análise interpretado: decisão apoiada e limitações dos dados
- [ ] Vantagens e limitações em escala, custo, governança e risco de pântano
- [ ] Comparação com ao menos uma arquitetura alternativa
- [ ] 3 ADRs (armazenamento, movimento, governança) com o que se perde e o gatilho, + 1 contra-cenário
- [ ] 3+ lições aprendidas, 1 escolha defendida e 1 contestada, próximos passos
- [ ] Dado crítico do cenário: por que é crítico, de que dados mestres depende, como é gerenciado hoje, dono e steward
- [ ] Termo central com significados divergentes entre áreas, a definição oficial proposta para o glossário e o registro no catálogo (significado, origem e responsável)
- [ ] Três regras de qualidade com dimensão e limite justificados + avaliação do registro de ouro (TODO 5)
- [ ] Maturidade antes × depois, ligada a uma capacidade de negócio da LODLog
- [ ] Gleicher (D, V, F e R) + dois erros de Kotter + vitória rápida em até 90 dias
- [ ] Matriz de comunicação por público (mensagem, canal, frequência, responsável, indicador de adoção)
- [ ] Até ~10 páginas, PDF, linguagem executiva

**Fora do escopo:** modelagem dimensional completa e feature engineering/treino de modelos de ML — são objeto de outras disciplinas. Se citar um modelo, trate-o como **consumidor da Gold** (como o motor preditivo do Lab 3).

**Critério de ouro:** toda afirmação de arquitetura com uma evidência ao lado — número, print ou fato do cenário. Na dúvida entre novidade e franqueza, escolha franqueza: "não testei X; testaria Y" é resposta de executivo.
