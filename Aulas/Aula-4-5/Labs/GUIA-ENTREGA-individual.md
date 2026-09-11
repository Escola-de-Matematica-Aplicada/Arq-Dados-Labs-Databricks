# GUIA DE ENTREGA INDIVIDUAL — Miniprojeto LODLog (70%)

**Prazo:** 18/10/2026 (15 dias após a última aula) · **Formato:** PDF, até ~8 páginas (máx. 10)
**Título sugerido do documento:** *"Planejando o pipeline de dados para o data lake da LODLog — [seu nome], [cenário A/B/C/D]"*

> **O princípio desta entrega:** você NÃO precisa (nem deve) escrever a DDL do zero nem inventar um banco imaginário. Os scripts, o seed, os diagramas e o pipeline Medallion foram **entregues prontos** no curso. Sua nota vem de **usar esses artefatos com evidência** (prints, números, queries executadas) e de **avaliar criticamente** as escolhas de arquitetura que eles representam. Copiar o SQL do starter sem explicá-lo vale ~0; adaptar 10 linhas e justificar por quê vale muito.

---

## Estrutura obrigatória do relatório (seções 1–8)

Cada seção indica o peso na rubrica (slide 30 da Aula 4-5) e o que "pronto" você pode usar.

### 1. Cenário e pergunta de negócio — 10%
- Qual sub-cenário você escolheu (A Rotas / B Manutenção / C Estoque / D Fraude) — igual ou diferente do grupo.
- A pergunta de negócio em 1 frase + o valor em jogo (multas R$ 4,2 MM, downtime R$ 2,1 MM, horas extras R$ 1,8 MM — do cenário LODLog).
- ❌ Não precisa de justificativa longa: 3–5 linhas bastam, desde que liguem dado → dinheiro.

### 2. Mapeamento de fontes (3–5, internas + externas) — 15%
Tabela no formato abaixo, usando as fontes REAIS da LODLog (Aulas 1 e 4-5):

| Fonte | Tipo (estrut./semi/não) | Formato | Volume | Frequência | Camada de chegada |
|---|---|---|---|---|---|
| ex.: IoT da frota | Semiestruturado | JSON | ~864k eventos/dia | 30s | Bronze (imutável) |

- Inclua **≥1 interna** (ERP/WMS/TMS/IoT) e **≥1 externa** (Maps/INMET/ANTT/IBGE).
- Evidência que diferencia: uma linha dizendo *onde esse dado já vive hoje no lab* (ex.: TMS → `lodlog_op.pedido`/`entrega`, criado pelo seed que você rodou).

### 3. Análise dos 5 Vs por fonte — 20% (o peso maior — atenção)
Para CADA fonte da seção 2, um parágrafo curto (3–4 linhas) respondendo as perguntas de negócio dos Vs, da Aula 1:
- **Volume** → quanto custa guardar/reprocessar? • **Velocidade** → quão rápido o negócio precisa reagir? • **Variedade** → lake ou warehouse? • **Veracidade** → em que camada a confiança é validada (as 4 camadas edge/stream/cross/trust)? • **Valor** → qual decisão/dinheiro isso destrava?
- Dica de banca: "cada V com um número do lab" vale mais que definição de dicionário. Ex.: *"IoT 864k/d → particionar por data_evento reduz scan de X para Y linhas (testei no starter)."*

### 4. Arquitetura proposta — 15%
- **Data Lake ou Lakehouse?** + justificativa em 6–10 linhas ligando a escolha ao tamanho/maturidade da LODLog (a matriz decisória da Aula 2 é sua; os slides 26–27 são a referência).
- Diagrama Bronze→Silver→Gold: **anote o diagrama pronto** ([`/Diagramas/LODLog_dw_v3.png`](../../../Diagramas/LODLog_dw_v3.png)) ou desenhe um esquema simples de blocos — o exigido é a legenda, não a arte.
- Justifique batch vs streaming por fluxo (tabela do LAB4) e ETL/ELT; cite quando Lambda/Kappa/híbrido se aplica (Aula 3).

### 5. Qualidade SQL — 20%
Você **cita** a DDL pronta e **analisa**; os scripts executados por você vêm do curso:
- **DDL (citada):** liste ≥3 tabelas do seu cenário (ex.: `lodlog_silver.iot_eventos`, `lodlog_gold.resumo_diario_frota`, `lodlog_dw.fato_entregas`) com 1 frase cada: o que é, em que camada vive, por que existe. Copie os CREATE relevantes como anexo **com atribuição** ao script do curso.
- **2 queries analíticas:** adaptadas do `LAB3_apoio_free.ipynb`/starter ao SEU cenário, com print do resultado + 1 frase de interpretação de negócio cada.
- **1 query de qualidade:** detecte anomalias propositais do seed (duplicatas, negativos, outliers, FK quebrada) — quantidade encontrada + "em qual camada isso deveria ser barrado e por quê".

### 6. Conexão com IA — 15%
- Que modelo preditivo seu lakehouse alimentaria (atraso? falha? ruptura? fraude?) e qual a **variável resposta** (ex.: `indicador_atraso` na `fato_entregas`).
- Quais features da sua camada Gold/`vw_features_ml` entrariam no modelo e por quê.
- 1 parágrafo de MLOps (Aula 4-5): como o time-travel/reproducibilidade da Bronze ajuda a recriar o dataset de treino.
- Honestidade vale ponto: NÃO é preciso treinar modelo — é preciso explicar a ponte dado→modelo.

### 7. Governança aplicada à sua arquitetura — dentro dos 15% da seção 4
Marque com ✔/✖/— os **10 mandamentos** (slide 19 da aula) no seu desenho: quais sua proposta garante, quais ficam para a próxima fase, e o que isso custaria se ignorado (LGPD, swamp, custo de scan).

### 8. Avaliação pós-projeto e lições — dentro dos 5% de comunicação
- Vantagens e limitações da arquitetura adotada (2+2 bullets, cada um com motivo).
- O que você mudaria se recomeçasse + 1 lição aprendida da EXECUÇÃO real (um número ou erro que você viu rodando os scripts vale mais que generalização).

---

## Como evidenciar o uso dos artefatos prontos (requisito)

Em toda a seção 1, inclua **um anexo "Ambiente e artefatos"** com: print do `SHOW TABLES` dos seus schemas, datas de execução do seed/starter, e link/caminho dos arquivos usados (`lodlog_modelo_dados_free.sql`, `lodlog_lab2_seed_free.py`, `lab4_miniprojeto_starter.py`, diagramas). Isso prova autoria da execução — o resto é análise.

## Checklist final antes de submeter (AVA FGV)

- [ ] 3–5 fontes mapeadas, ≥1 interna + ≥1 externa, com camada de chegada
- [ ] 5 Vs com número do lab (não só definição)
- [ ] Arquitetura escolhida + justificada contra a matriz decisória
- [ ] DDL **citada com atribuição** (≥3 tabelas, 1 frase cada) — não reescrita
- [ ] 2 queries analíticas com print + interpretação de negócio
- [ ] 1 query de qualidade com anomalias quantificadas + camada que deveria barrar
- [ ] Ponte dado→modelo de IA + 1 parágrafo de MLOps
- [ ] 10 mandamentos marcados ✔/✖
- [ ] Pós-projeto honesto (2 vantagens, 2 limitações, 1 lição com evidência)
- [ ] Anexo de execução (prints, datas, caminhos) · ≤10 páginas · PDF

**Critério de ouro:** toda afirmação de arquitetura com uma evidência ao lado — número, query, print ou linha de DDL. Na dúvida entre novidade e franqueza, escolha franqueza: "não testei X; testaria Y" é resposta de executivo, não de aluno.
