# GUIA DE ENTREGA INDIVIDUAL — Avaliação pós-projeto do data lake da LODLog (70%)

**Prazo:** 08/12/2026 (15 dias após a última aula — Aula 5, 23/11) · **Formato:** PDF, até ~8 páginas (ou deck equivalente)
**Título do documento:** *"Avaliação pós-projeto do data lake da LODLog — [seu nome] — Cenário [A/B/C/D]"*

> **O princípio desta entrega:** o grupo **construiu** o data lake sobre o seed do Databricks (70% pronto + 30% do grupo) e o **apresentou** na Aula 5. Agora você, sozinho, faz o que um líder de dados faz depois de um projeto: **avalia criticamente o que foi construído**, interpreta o resultado para o negócio, compara com uma alternativa e decide o próximo passo. Escreva para convencer um board, com evidência ao lado de cada afirmação. **Não se exige código novo.**

---

## Parte A — O que foi construído (25%)

1. **Cenário, pergunta e fontes — 10%**
   O cenário do grupo (A — Rotas, B — Manutenção preditiva, C — Estoque, D — Fraude em faturamento) e a pergunta de negócio. Uma tabela com **3 a 5 fontes** — as do seed que o cenário usa e as que faltaram (internas: ERP, WMS, TMS, IoT; externas: Maps, INMET, ANTT, IBGE): tipo de dado, formato, frequência e quem consome. Inclua os **5 Vs** das fontes principais, com um número cada; em Veracidade, diga onde o dado mente e qual camada barrou.

2. **As etapas percorridas — 15%**
   Descreva a construção e o uso do data lake **das fontes até o consumo**: o que veio pronto no seed, o que o grupo completou (os 4 TODOs) e os números da execução (Etapa 8 do notebook: linhas por camada e quantas a qualidade barrou). Diga, fonte a fonte, se a ingestão seria **batch, streaming ou CDC** em produção e por quê, e se o tratamento é ETL ou ELT.

## Parte B — Avaliação pós-projeto (50%)

3. **O resultado para o negócio — 15%**
   Retome a análise do grupo (TODO 3): o número, a interpretação e **a decisão que ele apoia**. Quais limitações dos dados enfraquecem essa conclusão (amostra, período, dado simulado, regra de qualidade escolhida no TODO 1)? O que você precisaria para levar essa decisão ao board com confiança?

4. **Vantagens e limitações da arquitetura — 20%**
   Avalie a arquitetura adotada (Lakehouse Medallion num único workspace) em quatro lentes: **escala, custo, governança e risco de "pântano de dados"**. Use os 4 pilares da Aula 4 (qualidade, segurança/LGPD, catálogo/linhagem, ciclo de vida): o que o seed e o grupo cobriram e o que ficou descoberto. Compare com **ao menos uma alternativa** — Data Warehouse, Data Mesh, Data Fabric ou a **Ponte dos Contratos** do RPG da Aula 2 — e diga em que condição da LODLog a alternativa seria melhor.

5. **Lições aprendidas e próximos passos — 15%**
   Pelo menos **três lições** (técnicas, de negócio ou de trabalho em equipe), cada uma com o fato que a originou. Termine com **uma escolha do desenho que você defende e uma que contestaria**, e com os próximos passos para elevar a maturidade em dados da LODLog.

## Parte C — Conexão transformadora (15%)

6. **Maturidade em dados e arquitetura empresarial**
   Onde a LODLog estava (silos, planilhas, as "cinco torres" da Aula 2) e aonde este data lake a leva. Que **capacidade de negócio** do cenário passa a ser medida, prevista ou automatizada? Que papéis de governança (dono de dados, steward) e que contratos de dados isso exige? *Opcional: um parágrafo comparando com a empresa onde você trabalha.*

## Comunicação executiva (10%)

Linguagem de board: decisão, risco e valor antes de tecnologia; sem jargão não explicado; uma figura vale mais que um parágrafo.

---

## Anexo técnico (opcional)

Se quiser ir além, **evolua o notebook do grupo** — mais uma fonte até a Gold, uma segunda regra de qualidade, um teste de "E se" — no **Databricks Free Edition** ou reproduza o data lake no **AWS Academy**. Até 4 páginas de prints, com a data de execução. O anexo não é necessário para a nota máxima; ele **conta como evidência** das Partes A e B.

---

## Checklist

- [ ] Cenário e pergunta de negócio em 1 parágrafo
- [ ] Tabela com 3–5 fontes e os 5 Vs com um número cada
- [ ] Etapas percorridas: o que veio pronto × o que o grupo construiu, com os números da Etapa 8
- [ ] Batch/streaming/CDC e ETL/ELT justificados fonte a fonte
- [ ] Resultado da análise interpretado: decisão apoiada e limitações dos dados
- [ ] Vantagens e limitações em escala, custo, governança e risco de pântano
- [ ] Comparação com ao menos uma arquitetura alternativa
- [ ] 3+ lições aprendidas, 1 escolha defendida e 1 contestada, próximos passos
- [ ] Maturidade antes × depois, ligada a uma capacidade de negócio da LODLog
- [ ] Até ~8 páginas, PDF, linguagem executiva

**Fora do escopo:** modelagem dimensional completa e feature engineering/treino de modelos de ML — são objeto de outras disciplinas. Se citar um modelo, trate-o como **consumidor da Gold** (como o motor preditivo do Lab 3).

**Critério de ouro:** toda afirmação de arquitetura com uma evidência ao lado — número, print ou fato do cenário. Na dúvida entre novidade e franqueza, escolha franqueza: "não testei X; testaria Y" é resposta de executivo.
