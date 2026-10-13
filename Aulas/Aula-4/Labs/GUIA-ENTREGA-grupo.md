# GUIA DE ENTREGA EM GRUPO — Miniprojeto LODLog (30%)

**Quando:** Aula 5 (23/11/2026) — pitch de 10 min + 5 min de Q&A por grupo. A construção e a análise acontecem na Aula 4 (17/11), que termina com um checkpoint sem nota.
**Entregáveis:** (1) pitch ao vivo na Aula 5 · (2) síntese pós-projeto de 1 página entregue no dia do pitch
**Formato do pitch:** até 5 slides (ou 1 slide + prints no Databricks) — "menos é mais" (slide "Pitch do Grupo na Aula 5" da Aula 4)

> **O princípio desta entrega:** o lakehouse de vocês **não é construído do zero** — o pipeline Medallion (`lab4_miniprojeto_starter.py`), a DDL (`lodlog_modelo_dados_free.sql`), o seed (`lodlog_lab2_seed_free.py`) e os diagramas ([`/Diagramas/`](../../../Diagramas/)) chegaram prontos. O que o grupo entrega é a **leitura crítica com evidência**: nós rodamos, inspecionamos, adaptamos ao nosso cenário e provamos o que cada camada faz — e dizemos com franqueza o que defenderíamos e o que contestaríamos neste desenho. Isso é exatamente o que a banca do miniprojeto avalia.

---

## 1. O pitch — 10 min + 5 min Q&A (roteiro com tempos)

| # | Bloco | Tempo | O que mostrar | Critério da rubrica (Aula 4, "Como Você Será Avaliado — Grupo") |
|---|---|---|---|---|
| 1 | **Cenário + pergunta de negócio** | 1 min | "Escolhemos (A) Rotas para atacar os 23% de atraso e R$ 4,2 MM/ano em multas." | Compreensão do cenário — 10% |
| 2 | **Arquitetura comentada** | 2 min | Uma foto do `LODLog_dw_v3.png` (ou `LODLog_op_v3.png`) **com 3 setas suas**: onde entra a sujeira (Bronze), onde ela é barrada (Silver), onde nasce o número do dashboard (Gold). Nada de diagrama novo — a legenda é o trabalho. | Arquitetura das fontes até o consumo — 20% |
| 3 | **Execução do pipeline** | 2 min | Prints do console do starter: linhas Bronze → Silver → Gold (nós e porquês: duplicatas removidas, ranges filtrados, agregação). + 1 linha por fonte na tabela "fonte × camada × batch/streaming/híbrido". | Integração estruturada + semi/não estruturada — 15% |
| 4 | **Análise Gold com número** | 2 min | O melhor resultado das 2 queries analíticas do grupo, com a frase de negócio: "CD Campinas: 91,8% de pontualidade; Sudeste é o pior custo/km." | Análise sobre o data lake, com número — 20% |
| 5 | **Pós-projeto** | 2 min | 1 vantagem · 1 limitação · **1 escolha que defendemos + 1 que contestaríamos** (com o "E se" que vocês testaram na Etapa 2.2, na Aula 4) · 1 lição aprendida. | Pós-projeto e lições — 15% · Apresentação — 5% |
| — | **Folga** | 1 min | Margem para transição e imprevistos — não usar para esticar blocos. | — |
| — | **Q&A** | 5 min | A banca sorteia 1 dos 4 pilares de governança e pergunta sobre ELE no desenho de vocês. | Governança (pilar sorteado) — 15% |

**Regras do pitch**
- Cronômetro rigoroso — cortar é melhor que correr.
- Todo mundo fala ao menos 1 bloco.
- Citem de onde vêm os artefatos ("DDL do curso, adaptamos X") — atribuição é honestidade acadêmica, não fraqueza.
- Se algo quebrou na execução, NARREM o erro e a correção: bug bem contado vale ponto no pós-projeto.

---

## 2. Síntese pós-projeto — 1 página

Substitui relatórios longos de grupo. Quatro seções fixas:

1. **Mapeamento fonte × camada (tabela única):** para cada fonte do cenário de vocês — tipo, formato, volume, frequência, camada Bronze/Silver/Gold correspondente no ambiente executado, e batch/streaming/híbrido com justificativa de 1 linha. *(É o item 2 do checkpoint da Aula 4 — agora preenchido sobre o que RODOU, não sobre o imaginado.)*
2. **A análise que conduzimos:** a query vencedora do bloco 4 + print + interpretação de negócio (2–3 linhas).
3. **Governança sob as 4 lentes:** para cada pilar (qualidade, segurança/LGPD, catálogo/linhagem, ciclo de vida), uma linha: ✔ cobre / ✖ não cobre / ➜ cobriríamos com (ação) no ambiente pronto. Sem parágrafo defensivo — a banca prefere o ✖ assumido com plano.
4. **Avaliação pós-projeto:** vantagens × limitações (2+2 bullets) + "o que mudaríamos se recomeçássemos" (1 parágrafo) + lições.

**Autoavaliação de participação (checkbox obrigatório):** [ ] todos participaram da execução · [ ] todos falaram no pitch · [ ] cada afirmação de arquitetura tem um print/número ao lado.

---

## 3. Preparação mínima — Aula 4 (checkpoint das 22h05) e até a Aula 5

- [ ] Seed + DDL do curso rodados no workspace do grupo (ou fallback: notebook compartilhado de quem rodou)
- [ ] `lab4_miniprojeto_starter.py` executado com Run All + prints salvos
- [ ] As 6 tabelas do starter inspecionadas (1 frase cada: o que entra, o que sai, quem consome)
- [ ] 2 queries analíticas adaptadas ao cenário + 1 de qualidade com anomalias quantificadas
- [ ] 1 "E se" arquitetural testado e registrado (validação removida / append vs merge / PII)
- [ ] Slides montados com prints reais — proibido slide com texto de dicionário (pode terminar até a Aula 5)
- [ ] Ensaio cronometrado: 10 min, todos falam

---

## O que NÃO é exigido (e o que a banca vai valorizar)

| Não precisa | Vai pontuar |
|---|---|
| Desenhar diagrama ER/Star original | Anotar o diagrama pronto e explicar as camadas com setas |
| Escrever DDL do zero | Citar a DDL do curso e dizer o que ela garante/não garante |
| Construir um data lake próprio inexistente | Executar o starter e narrar Bronze→Silver→Gold com números reais |
| Modelo de IA treinado ou features criadas | Dizer quem consome a Gold (dashboard ou modelo) e o que esse consumidor exige dela |
| Slides bonitos | 1 print feio do console que prova uma afirmação |

**Critério de ouro (vale para pitch e síntese):** nenhuma frase de arquitetura sem evidência ao lado. E na hora de defender, usem o vocabulário que a disciplina construiu desde a Aula 2: armadilha, contrato de dados, governança federada leve, Bronze imutável, pântano. A banca sabe quais portas do RPG cada escolha de vocês abre e fecha — mostrem que vocês também sabem.
