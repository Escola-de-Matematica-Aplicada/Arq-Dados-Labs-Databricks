# GUIA DE ENTREGA INDIVIDUAL — Aprofundamento de cenário da LODLog (70%)

**Prazo:** 08/12/2026 (15 dias após a última aula — Aula 5, 23/11) · **Formato:** PDF, 4–6 páginas (+ anexo técnico opcional)
**Título do documento:** *"Aprofundamento de cenário da LODLog — [seu nome] — Cenário [A/B/C/D]"*

> **O princípio desta entrega:** você parte do cenário que seu grupo construiu e defendeu (A — Rotas, B — Manutenção preditiva, C — Estoque, D — Fraude em faturamento) e o **aprofunda sozinho**, em duas camadas: primeiro, o **núcleo de arquitetura** que a disciplina exige; depois, a **conexão transformadora** — como essa arquitetura eleva a maturidade em dados da LODLog e se encaixa na arquitetura empresarial dela. Escreva para convencer um board, com evidência ao lado de cada afirmação.

---

## Parte A — Núcleo de arquitetura (obrigatório · 55%)

1. **Cenário e fontes — 15%**
   O cenário escolhido e a pergunta de negócio que ele responde. Mapeie **3 a 5 fontes**, internas (ERP, WMS, TMS, IoT) e externas (Maps, INMET, ANTT, IBGE), em uma tabela: tipo (estruturado/semi/não estruturado), formato, volume, frequência e quem consome.

2. **Os 5 Vs das fontes — 15%**
   Volume, Velocidade, Variedade, Veracidade e Valor para as fontes mapeadas, cada V com um número (do cenário LODLog ou da execução do grupo). Veracidade é onde a maioria perde ponto: diga onde o dado mente (sensor com defeito, TMS × WMS divergentes) e qual camada barra.

3. **Arquitetura proposta — 25%**
   Data Lake ou Lakehouse com camadas **Bronze / Silver / Gold**: o que entra em cada camada, as regras de qualidade da Silver e quem consome a Gold. **Justifique batch × streaming fonte a fonte** — que decisão de negócio piora se o dado chegar uma hora depois? Diga também ETL ou ELT e por quê.

## Parte B — Conexão transformadora (obrigatório · 35%)

4. **Maturidade em dados e arquitetura empresarial — 25%**
   Onde a LODLog está hoje (silos, planilhas, relatórios atrasados — as "cinco torres" da Aula 2) e aonde a arquitetura do item 3 a leva. Conecte com a arquitetura empresarial: que **capacidade de negócio** do cenário (ex.: "garantir entrega no prazo", "manter a frota disponível") passa a ser medida, prevista ou automatizada? Que papéis de governança (dono de dados, steward) e que contratos de dados isso exige? *Opcional: um parágrafo comparando com a empresa onde você trabalha.*

5. **Decisão e trade-off — 10%**
   Qual das 5 portas do RPG da Aula 2 — ou a **Ponte dos Contratos** (contratos de dados + dono por domínio com padrões mínimos + governança federada leve + Bronze descentralizado e Silver/Gold centralizados) — você defenderia para a LODLog, e por quê. Diga **uma escolha que você defende e uma que contestaria** no desenho do seu grupo.

## Comunicação executiva (10%)

Linguagem de board: decisão, risco e valor antes de tecnologia; sem jargão não explicado; uma figura vale mais que um parágrafo.

---

## Anexo técnico (opcional)

Se quiser ir além, **suba o data lake do seu cenário** — ingestão, armazenamento, governança e análise — no **Databricks Free Edition** (partindo do `lab4_miniprojeto_starter.py` e do notebook do Lab 3) ou no **AWS Academy**. Até 4 páginas de prints: tabelas por camada, uma query de qualidade, uma análise sobre a Gold e a data de execução.

O anexo não é necessário para a nota máxima; ele **conta como evidência** dos itens 2 e 3 (números reais no lugar de estimativas).

---

## Checklist

- [ ] Cenário (A/B/C/D) e pergunta de negócio em 1 parágrafo
- [ ] Tabela com 3–5 fontes, internas e externas
- [ ] 5 Vs com um número cada; Veracidade com a camada que barra o problema
- [ ] Bronze/Silver/Gold descritas; batch × streaming justificado fonte a fonte; ETL ou ELT
- [ ] Maturidade hoje × depois, ligada a uma capacidade de negócio da LODLog
- [ ] Papéis de governança e contratos de dados necessários
- [ ] Porta escolhida (ou Ponte dos Contratos), com 1 escolha defendida e 1 contestada
- [ ] 4–6 páginas, PDF, linguagem executiva
- [ ] (Opcional) Anexo técnico com prints do Databricks ou do AWS Academy

**Fora do escopo:** modelagem dimensional completa e feature engineering/treino de modelos de ML — são objeto de outras disciplinas. Se citar um modelo, trate-o como **consumidor da Gold** (como o motor preditivo do Lab 3).

**Critério de ouro:** toda afirmação de arquitetura com uma evidência ao lado — número, print ou fato do cenário. Na dúvida entre novidade e franqueza, escolha franqueza: "não testei X; testaria Y" é resposta de executivo.
