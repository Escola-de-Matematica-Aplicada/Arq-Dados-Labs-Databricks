# GUIA DE ENTREGA EM GRUPO — Miniprojeto LODLog (30%)

**Quando:** apresentação na própria sessão dupla (Aulas 4-5, 03/10) — pitch de 5 min + 2 min de Q&A por grupo
**Entregáveis:** (1) pitch ao vivo · (2) síntese pós-projeto de 1 página entregue ao final da noite
**Formato do pitch:** até 5 slides (ou 1 slide + prints no Databricks) — "menos é mais" (slide 31 da aula)

> **O princípio desta entrega:** o lakehouse de vocês **não é construído do zero** — o pipeline Medallion (`lab4_miniprojeto_starter.py`), a DDL (`lodlog_modelo_dados_free.sql`), o seed (`lodlog_lab2_seed_free.py`) e os diagramas ([`/Diagramas/`](../../../Diagramas/)) chegaram prontos. O que o grupo entrega é a **leitura crítica com evidência**: nós rodamos, inspecionamos, adaptamos ao nosso cenário e provamos o que cada camada faz — e dizemos com franqueza o que defenderíamos e o que contestaríamos neste desenho. Isso é exatamente o que a banca do miniprojeto avalia.

---

## 1. O pitch — 5 min + 2 min Q&A (roteiro com tempos)

| # | Bloco | Tempo | O que mostrar | Critério da rubrica (slide 30) |
|---|---|---|---|---|
| 1 | **Cenário + pergunta de negócio** | 30s | "Escolhemos (A) Rotas para atacar os 23% de atraso e R$ 4,2 MM/ano em multas." | Compreensão do cenário — 10% |
| 2 | **Arquitetura comentada** | 60s | Uma foto do `LODLog_dw_v3.png` (ou `LODLog_op_v3.png`) **com 3 setas suas**: onde entra a sujeira (Bronze), onde ela é barrada (Silver), onde nasce o número do dashboard (Gold). Nada de diagrama novo — a legenda é o trabalho. | Modelagem ER+Star — 20% |
| 3 | **Execução do pipeline** | 60s | Prints do console do starter: linhas Bronze → Silver → Gold (nós e porquês: duplicatas removidas, ranges filtrados, agregação). + 1 linha por fonte na tabela "fonte × camada × batch/streaming/híbrido". | Pipeline — 20% |
| 4 | **Análise Gold com número** | 60s | O melhor resultado das 2 queries analíticas do grupo, com a frase de negócio: "CD Campinas: 91,8% de pontualidade; Sudeste é o pior custo/km." | Casos de IA/análise — 20% |
| 5 | **Pós-projeto** | 60s | 1 vantagem · 1 limitação · **1 escolha que defendemos + 1 que contestaríamos** (com o "e se" que vocês testaram na Etapa 2.2) · 1 lição aprendida. | Qualidade+LGPD+linhagem — 15% · Apresentação — 10% |
| — | **Q&A** | 120s | A banca sorteia 1 dos 4 pilares de governança e pergunta sobre ELE no desenho de vocês. | Extras (SQL/protótipo) — 5% |

**Regras do pitch**
- Cronômetro rigoroso — cortar é melhor que correr.
- Todo mundo fala ao menos 1 bloco.
- Citem de onde vêm os artefatos ("DDL do curso, adaptamos X") — atribuição é honestidade acadêmica, não fraqueza.
- Se algo quebrou na execução, NARREM o erro e a correção: bug bem contado vale pontos de "Extras".

---

## 2. Síntese pós-projeto — 1 página (entregar ao fim da noite)

Substitui relatórios longos de grupo. Quatro seções fixas:

1. **Mapeamento fonte × camada (tabela única):** para cada fonte do cenário de vocês — tipo, formato, volume, frequência, camada Bronze/Silver/Gold correspondente no ambiente executado, e batch/streaming/híbrido com justificativa de 1 linha. *(É o entregável 2 do briefing da aula — agora preenchido sobre o que RODOU, não sobre o imaginado.)*
2. **A análise que conduzimos:** a query vencedora do bloco 4 + print + interpretação de negócio (2–3 linhas).
3. **Governança sob as 4 lentes:** para cada pilar (qualidade, segurança/LGPD, catálogo/linhagem, ciclo de vida), uma linha: ✔ cobre / ✖ não cobre / ➜ cobriríamos com (ação) no ambiente pronto. Sem parágrafo defensivo — a banca prefere o ✖ assumido com plano.
4. **Avaliação pós-projeto:** vantagens × limitações (2+2 bullets) + "o que mudaríamos se recomeçássemos" (1 parágrafo) + lições.

**Autoavaliação de participação (checkbox obrigatório):** [ ] todos participaram da execução · [ ] todos falaram no pitch · [ ] cada afirmação de arquitetura tem um print/número ao lado.

---

## 3. Preparação mínima na noite (antes do pitch)

- [ ] Seed + DDL do curso rodados no workspace do grupo (ou fallback: notebook compartilhado de quem rodou)
- [ ] `lab4_miniprojeto_starter.py` executado com Run All + prints salvos
- [ ] As 6 tabelas do starter inspecionadas (1 frase cada: o que entra, o que sai, quem consome)
- [ ] 2 queries analíticas adaptadas ao cenário + 1 de qualidade com anomalias quantificadas
- [ ] 1 "E se" arquitetural testado e registrado (validação removida / append vs merge / PII)
- [ ] Slides montados com prints reais — proibido slide com texto de dicionário

---

## O que NÃO é exigido (e o que a banca vai valorizar)

| Não precisa | Vai pontuar |
|---|---|
| Desenhar diagrama ER/Star original | Anotar o diagrama pronto e explicar as camadas com setas |
| Escrever DDL do zero | Citar a DDL do curso e dizer o que ela garante/não garante |
| Construir um data lake próprio inexistente | Executar o starter e narrar Bronze→Silver→Gold com números reais |
| Modelo de IA treinado | Explicar a ponte Gold→features→variável resposta |
| Slides bonitos | 1 print feio do console que prova uma afirmação |

**Critério de ouro (vale para pitch e síntese):** nenhuma frase de arquitetura sem evidência ao lado. E na hora de defender, usem o vocabulário que a disciplina construiu desde a Aula 2: armadilha, contrato de dados, governança federada leve, Bronze imutável, pântano. A banca sabe quais portas do RPG cada escolha de vocês abre e fecha — mostrem que vocês também sabem.
