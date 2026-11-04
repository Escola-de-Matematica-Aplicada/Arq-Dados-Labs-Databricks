# LAB 3 — Pipelines LODLog: do Desenho à Execução

**Disciplina** Arquitetura de Dados e Big Data
**Aula** 3 — Organização e Manuseio de Dados em Bases Distribuídas
**Duração do Lab** 90 min em aula (20h50–22h20): 3 min de briefing + 30 min de desenho + 35 min de mão na massa no Databricks + 20 min de apresentações + 2 min de síntese
**Entrega (grupo)** Matriz de decisão + diagrama do pipeline + respostas aos 5 exercícios do notebook + pitch de 3 min

> **Como este lab funciona:** em duas metades. Na **primeira (desenho, 30 min)**, o trabalho é o de um arquiteto de dados: olhar as fontes de um domínio da LODLog, decidir como cada uma entra, onde é guardada, como é transformada e quem a consome — e **justificar** cada escolha por latência, custo e facilidade de reprocessar. Na **segunda (mão na massa, 35 min)**, vocês rodam no Databricks um pipeline pronto, em lote e em streaming, até um **motor preditivo** que calcula o risco de atraso de cada entrega — e respondem, com números, às perguntas que um gestor faria. Ninguém precisa saber programar: o notebook já vem pronto; vocês operam, observam e decidem. O que sair daqui é o rascunho do miniprojeto das Aulas 4 e 5.

---

## Antes de começar

- Formem **5 grupos** e sorteiem um domínio por grupo (tabela abaixo).
- Tenham à mão os slides da Aula 3, em especial "Ingestão LODLog — 8 fontes, 5 padrões", "AWS vs Azure vs GCP — por camada" e "Pipeline Fim a Fim LODLog".
- Cenário completo: [`docs/LODLog/The-Lord-Of-Data-Logistics.md`](../../../docs/LODLog/The-Lord-Of-Data-Logistics.md).
- Material: papel/quadro ou qualquer ferramenta de diagrama (draw.io, Excalidraw, Miro, PowerPoint).

| Domínio | Fontes do domínio | Pergunta de negócio que o pipeline precisa responder |
| --- | --- | --- |
| Frota/IoT | Sensores IoT (JSON a cada 30s), API ANTT (eventos de bloqueio) | Quais veículos precisam de manutenção antes de quebrar? |
| Operação/TMS | TMS (status de entregas em tempo real), API Google Maps (5 min) | Quais entregas vão atrasar hoje e por quê? |
| Estoque/WMS | WMS (movimentações a cada 15 min), ERP (pedidos diários) | Onde vai faltar estoque na próxima semana? |
| Financeiro/ERP | ERP (faturamento diário), IBGE (CSV mensal) | Qual a receita e a margem por cliente e por região? |
| Dados Externos | Google Maps, INMET (horário), ANTT, IBGE | Como clima, trânsito e bloqueios explicam os atrasos? |

---

## Parte 1 — Mapear as fontes (5 min)

Para cada fonte do domínio, anotem:

- **Formato:** relacional, JSON, XML, CSV.
- **Frequência e volume:** ex.: IoT 864k eventos/dia; Maps ~60k requisições/dia; ERP ~3k registros/dia.
- **Tipo de dado:** estruturado, semiestruturado ou não estruturado (Aula 1).
- **Quem consome:** dashboard, alerta, modelo de ML, API.

## Parte 2 — Padrão de ingestão (7 min)

Escolham, por fonte, um dos cinco padrões e a ferramenta:

| Padrão | Use quando | Ferramentas típicas |
| --- | --- | --- |
| Batch | a latência de horas é aceitável | Airflow, Glue, Data Factory, `spark.read` |
| Micro-batch | minutos bastam e se quer simplicidade | Spark Structured Streaming com trigger, Auto Loader |
| Streaming | a decisão precisa ser tomada em segundos | Kafka, Kinesis, Event Hubs, Pub/Sub |
| CDC | a fonte é um banco OLTP que não pode ser sobrecarregado | Debezium, DMS |
| API pull/push | a fonte é um serviço externo | Airflow + `requests`, NiFi, webhooks |

**Pergunta de controle:** essa fonte *realmente* precisa de streaming? Qual decisão de negócio piora se ela chegar uma hora depois? (No [dossiê](../../../docs/LODLog/Por-que-esta-arquitetura.md), só 2 das 7 perguntas da LODLog pedem resposta em minutos.)

## Parte 3 — ETL ou ELT (4 min)

- **ELT** (carregar cru na Bronze e transformar no Lakehouse) é o padrão quando há dado semi/não estruturado, volume crescente ou regras que mudam com frequência.
- **ETL** (transformar antes de carregar) só se justifica com volume pequeno, schema estável e governança rígida antes da carga.

Registrem a decisão por fonte e **uma frase de justificativa**.

## Parte 4 — Lambda, Kappa ou híbrido (4 min)

| Opção | Escolham se... |
| --- | --- |
| Lambda | precisam de recálculo completo do histórico **e** de baixa latência, e aceitam manter dois códigos |
| Kappa | as fontes já são logs de eventos e um replay de dias resolve o reprocessamento |
| Híbrido | só parte das fontes precisa de streaming — o restante vai em batch |

Justifiquem por **custo** (streaming fica sempre ligado) e **latência** exigida pelo consumo.

## Parte 5 — Matriz ferramenta × camada (6 min)

Preencham uma linha por fonte. Escolham **uma** plataforma para o domínio (AWS, Azure, GCP ou Hadoop/Spark local) e expliquem por quê.

| Fonte | Ingestão (padrão + ferramenta) | ETL/ELT | Bronze → Silver/Gold | Processamento | Latência alvo | Arquitetura | Por que não a alternativa (força) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| (ex.: IoT) | Streaming: Kafka + Structured Streaming | ELT | JSON → Delta particionado por data | Spark + `MERGE` no Delta | Segundos | Kappa | Batch: o alerta do motor exige 2 min (F2) |
| (ex.: ERP) | Batch diário: Airflow + JDBC | ELT | Parquet → Delta | Spark SQL + dbt | Horas | Batch puro | Streaming: o relatório D-1 basta e streaming fica sempre ligado (F2, F4) |
| | | | | | | | |
| | | | | | | | |

**Plataforma escolhida e justificativa** (lembrem a decisão D4: 5 pessoas e o hosting do ERP vencendo em 14 meses): ____________________________________________

## Parte 6 — Diagrama (4 min)

Desenhem o pipeline do domínio com as cinco caixas abaixo e as setas entre elas, uma faixa por fonte:

```
Fonte → Ingestão → Bronze (cru) → Silver (validado) → Gold (consumo) → Consumidor
                    └──────────── Orquestração (Airflow / job contínuo) ────────────┘
```

O pitch de 3 min é preparado depois da Parte 7, já com os números do notebook.

---

## Parte 7 — Mão na massa: do evento ao score de risco (35 min)

O notebook [`lab3_pipeline_motor_preditivo.py`](lab3_pipeline_motor_preditivo.py) executa, em escala de laboratório, o pipeline do domínio **Operação/Frota**: entregas do TMS chegam em **lote** (CSV diário) e a telemetria IoT em **streaming** (micro-lotes JSON); as duas passam por Bronze → Silver → Gold, e um **motor preditivo pronto** (modelo `risco_atraso` v1.2, entregue pelo time de Ciência de Dados) lê a Gold e calcula a probabilidade de atraso de cada entrega.

1. **Rodar (10 min):** Databricks Free Edition → Workspace → Import → `lab3_pipeline_motor_preditivo.py` → **Run All** (~2 min, Serverless). Não precisa ter rodado nada antes: o notebook gera os próprios dados.
2. **Observar (10 min):** anotem os números de cada etapa — linhas na Bronze e na Silver (quantas foram barradas e por quê), entregas na Gold, alertas do motor por CD.
3. **Responder (15 min):** os 5 exercícios do fim do notebook — limiar de alerta como decisão de negócio, lote × streaming, qualidade, reprocessamento e ferramenta por camada. Cada resposta com um número do notebook.

> Vocês **não** criam features nem treinam o modelo — isso é tema das disciplinas de Ciência de Dados. O modelo aqui é um **consumidor** da Gold, como um dashboard: o que importa para a arquitetura é a Gold ser confiável, documentada e chegar a tempo.

**Pitch de 3 min (prepare enquanto os outros apresentam):** (1) qual fonte é a mais crítica e por quê; (2) onde está o streaming e por que ele vale o custo — com o número de alertas do motor; (3) como reprocessar se a regra da Silver mudar.

---

## Apresentação relâmpago (20 min) e síntese (3 min)

- 4 min por grupo: 3 min de pitch + 1 pergunta da turma.
- Perguntas-guia do professor:
  - Onde está o gargalo de Veracidade?
  - Onde o egress ou o lock-in doem?
  - O que reprocessar se a regra da Silver mudar?
  - Quando o streaming não vale o custo?

---

## Critérios de avaliação (formativa)

| Critério | O que se espera |
| --- | --- |
| Coerência | padrão de ingestão, latência alvo e ferramenta batem entre si |
| Evidência | as respostas dos exercícios do notebook citam números da execução |
| Custo | streaming só onde a latência paga; formatos abertos; particionamento |
| Reprocessamento | Bronze imutável e caminho claro para refazer Silver/Gold |
| Justificativa | cada escolha tem uma frase de "porque" ligada à pergunta de negócio |

---

## Conexão com o trabalho

- **Trabalho individual (70%, até 08-dez):** a matriz e o diagrama de hoje cobrem a parte "arquitetura proposta com Bronze/Silver/Gold e justificativa batch vs streaming".
- **Miniprojeto em grupo (30%, apresentação na Aula 5):** o grupo vai construir no Databricks Free Edition uma versão simplificada do pipeline desenhado aqui.

## Material opcional

- [`LAB3_apoio_free.ipynb`](LAB3_apoio_free.ipynb) — consultas SQL guiadas no Databricks Free Edition sobre o modelo LODLog; é a referência de SQL usada na Aula 4.

---
