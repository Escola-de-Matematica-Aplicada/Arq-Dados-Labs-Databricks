# GUIA DE ENTREGA EM GRUPO — Miniprojeto LODLog (30%)

**Quando:** Aula 5 (23/11/2026). A construção começa na Aula 4 (17/11, com checkpoint sem nota) e continua na **primeira metade da Aula 5 (19h00–20h30)**; os pitches (10 min + 5 min de Q&A por grupo; com 5 ou mais grupos, 7 + 3) acontecem na segunda metade.
**Entregáveis:** (1) notebook `lab4_miniprojeto_seed.py` com os 30% completados e executado de ponta a ponta (Etapa 8 toda ✅) · (2) pitch ao vivo na Aula 5 · (3) síntese pós-projeto preliminar de 1 página entregue no dia do pitch
**Formato do pitch:** até 5 slides (ou 1 slide + prints no Databricks) — "menos é mais" (slide "Pitch do Grupo na Aula 5" da Aula 4)

> **O princípio desta entrega:** o grupo recebe o seed do Databricks com **70% do data lake pronto e explicado** e **constrói os 30% restantes**: leva uma fonte semi/não estruturada até a Silver (TODO 1), constrói a Gold do cenário (TODO 2), interpreta a análise de negócio (TODO 3), aplica governança com dois termos no glossário (TODO 4) e decide o registro de ouro do cliente — o dado mais crítico da LODLog (TODO 5). O pitch mostra **o que veio pronto, o que o grupo construiu e o que o número diz ao negócio** — e abre a avaliação pós-projeto, que cada um aprofunda na entrega individual.

---

## 1. O pitch — 10 min + 5 min Q&A (roteiro com tempos)

| # | Bloco | Tempo | O que mostrar | Critério da rubrica (Aula 4, "Como Você Será Avaliado — Grupo") |
|---|---|---|---|---|
| 1 | **Cenário + pergunta de negócio** | 1 min | "Escolhemos (A) Rotas para atacar os 23% de atraso e R$ 4,2 MM/ano em multas." | Compreensão do cenário — 10% |
| 2 | **Arquitetura comentada** | 2 min | O fluxo das fontes ao consumo (pode ser o quadro da Parte 2 do LAB4 ou um desenho simples) **com 3 setas suas**: onde entra a sujeira (Bronze), onde ela é barrada (Silver), onde nasce o número do dashboard (Gold). Marquem o que veio pronto e o que o grupo construiu. | Arquitetura das fontes até o consumo — 20% |
| 3 | **Construção e execução** | 2 min | A Etapa 8 do notebook: linhas Bronze → Silver → Gold e quantas a qualidade barrou. **O que o grupo construiu**: as regras do TODO 1, a métrica-chave do TODO 2 e o **registro de ouro do TODO 5** (quantos registros viraram quantos clientes mestres, de onde vem o endereço oficial e o que é endereço válido). + 1 linha por fonte na tabela "fonte × camada × batch/streaming/CDC". | Integração estruturada + semi/não estruturada — 15% |
| 4 | **Análise Gold com número** | 2 min | O resultado do TODO 3: pergunta, número e frase de negócio ("nos dias de chuva forte a pontualidade cai de 83% para 48%"). | Análise sobre o data lake, com número — 20% |
| 5 | **Pós-projeto (preliminar)** | 2 min | 1 vantagem · 1 limitação · **1 escolha que defendemos + 1 que contestaríamos** (com o "E se", se testaram) · 1 lição aprendida. | Pós-projeto e lições — 15% · Apresentação — 5% |
| — | **Folga** | 1 min | Margem para transição e imprevistos — não usar para esticar blocos. | — |
| — | **Q&A** | 5 min | A banca sorteia 1 dos 4 pilares de governança e pergunta sobre ELE no desenho de vocês (o TODO 4 é o ponto de partida). | Governança (pilar sorteado) — 15% |

**Regras do pitch**
- Cronômetro rigoroso — cortar é melhor que correr.
- Todo mundo fala ao menos 1 bloco.
- Citem de onde vêm os artefatos ("DDL do curso, adaptamos X") — atribuição é honestidade acadêmica, não fraqueza.
- Se algo quebrou na execução, NARREM o erro e a correção: bug bem contado vale ponto no pós-projeto.

---

## 2. Síntese pós-projeto — 1 página

Substitui relatórios longos de grupo. Quatro seções fixas:

1. **Mapeamento fonte × camada (tabela única):** para cada fonte usada pelo cenário — tipo, formato, volume, frequência, camada Bronze/Silver/Gold no notebook executado, quem construiu (seed ou grupo) e batch/streaming/CDC com justificativa de 1 linha.
2. **A análise que conduzimos:** a consulta do TODO 3 + print + interpretação de negócio (2–3 linhas).
3. **Governança sob as 4 lentes:** para cada pilar (qualidade, segurança/LGPD, metadados e glossário, ciclo de vida), uma linha: ✔ cobre (citem o TODO 4) / ✖ não cobre / ➜ cobriríamos com (ação). Sem parágrafo defensivo — a banca prefere o ✖ assumido com plano. Feche com o **dado crítico**: qual é o dado mais crítico do cenário de vocês e por quê, a decisão do TODO 5, o dono e o steward do cliente mestre, os dois termos do glossário e o efeito do endereço ruim na pontualidade.
4. **Avaliação pós-projeto preliminar:** vantagens × limitações (2+2 bullets) + "o que mudaríamos se recomeçássemos" (1 parágrafo) + lições. *(Cada integrante aprofunda isto na entrega individual.)*

**Autoavaliação de participação (checkbox obrigatório):** [ ] todos participaram da execução · [ ] todos falaram no pitch · [ ] cada afirmação de arquitetura tem um print/número ao lado.

---

## 3. Preparação mínima — checkpoint da Aula 4 (22h05) e primeira metade da Aula 5

- [ ] Seed importado e Run All executado no workspace do grupo (ou no de um integrante, compartilhado)
- [ ] `CENARIO` definido e Etapas 1–3 lidas: tipo de dado, ingestão e linhas barradas por fonte
- [ ] TODO 1 — fonte extra na Silver, com menos de 10% de `outros` (se ocorrências)
- [ ] TODO 2 — métrica-chave da Gold preenchida
- [ ] TODO 3 — pergunta de negócio e interpretação escritas
- [ ] TODO 5 — registro de ouro do cliente gravado (`lodlog_gold.cliente_mestre`) e impacto na pontualidade lido
- [ ] TODO 4 — governança aplicada, regra de qualidade sem violações e dois termos no glossário (Aula 5)
- [ ] Etapa 8 toda ✅ e prints salvos
- [ ] Slides montados com prints reais — até 20h30 da Aula 5
- [ ] Ensaio cronometrado: 10 min, todos falam

---

## O que NÃO é exigido (e o que a banca vai valorizar)

| Não precisa | Vai pontuar |
|---|---|
| Desenhar diagrama ER/Star original | Um fluxo simples, anotado, que explique as camadas com setas |
| Escrever DDL do zero | Citar a DDL do curso e dizer o que ela garante/não garante |
| Escrever o pipeline do zero | Completar os 30% do seed e narrar Bronze→Silver→Gold com números reais |
| Modelo de IA treinado ou features criadas | Dizer quem consome a Gold (dashboard ou modelo) e o que esse consumidor exige dela |
| Slides bonitos | 1 print feio do console que prova uma afirmação |

**Critério de ouro (vale para pitch e síntese):** nenhuma frase de arquitetura sem evidência ao lado. E na hora de defender, usem o vocabulário que a disciplina construiu desde a Aula 2: armadilha, contrato de dados, governança federada leve, Bronze imutável, pântano. A banca sabe quais portas do RPG cada escolha de vocês abre e fecha — mostrem que vocês também sabem.
