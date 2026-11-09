# Projeto de Engenharia de Dados para IA e Negocios
## LODLog Transportes e Distribuicao S.A.

> **Disciplina:** Engenharia de Dados para Inteligencia Artificial e Analytics  
> **Curso:** MBA em Inteligencia Artificial para Negocios  
> **Duracao:** 24h (5 aulas de \~3h20min)  
> **Foco:** Arquitetura de dados, modelagem, pipelines ETL/ELT, qualidade e preparacao para ML/IA — com menos dependencia de vendor de nuvem e maior profundidade tecnica em dados.

> ### Aviso para a turma de Arquitetura de Dados e Big Data
>
> Este documento e **material de referencia de uma disciplina irma** (Engenharia de Dados para IA e Analytics).
> Ele esta publicado aqui porque o cenario da LODLog — a empresa, os dados, os numeros e o problema de negocio —
> e o mesmo das duas disciplinas, e vale como fonte de consulta.
>
> **O que NAO se aplica a Arquitetura de Dados e Big Data:** as secoes 12 e 13 (rubrica e entregaveis do
> "Projeto Individual (70% da nota)"). Nesta disciplina a avaliacao e **prova presencial individual (70%) +
> trabalho em grupo (30%)**, e **nao ha entrega individual**. Modelagem dimensional completa (star schema) e
> feature engineering / treino de modelos de ML estao **fora do escopo** desta disciplina — se um modelo aparecer,
> trate-o como consumidor da camada Gold. As regras que valem aqui estao em
> `Aulas/Aula-4/Labs/GUIA-ENTREGA-grupo.md` (trabalho em grupo) e `Aulas/Aula-4/Labs/GUIA-ESTUDO-PROVA.md` (prova).

---

# 1. Cenario de Negocio

## 1.1 A Empresa: LODLog

**LODLog Transportes e Distribuicao S.A.** e uma empresa brasileira de logistica com sede em Campinas/SP, fundada em 2010. Opera com:

- **450 veiculos** de carga (leves, medios e pesados)
- **12 centros de distribuicao** espalhados pelo Brasil
- **3.200 clientes ativos** no setor varejista e industrial
- **\~18.000 entregas/mes**
- **Faturamento anual:** R$ 380 milhoes

## 1.2 O Problema de Negocio

> *"Sabemos que estamos perdendo dinheiro, mas nao sabemos exatamente onde nem por que."*  
> — **Diretor de Operacoes, LODLog**

| Dor | Impacto Estimado |
|-----|-----------------|
| 23% das entregas chegam com atraso | Multas contratuais de R$ 4,2 MM/ano |
| Retrabalho por falta de dados de inventario | +R$ 1,8 MM em horas extras |
| Decisoes de rota baseadas em planilhas Excel | +18% de consumo de combustivel |
| Manutencao corretiva (quebras na estrada) | R$ 2,1 MM/ano em reboque e downtime |
| Relatorios gerenciais entregues com 5 dias de atraso | Perda de janela para decisao tatica |

## 1.3 Objetivo Estrategico com IA

Construir uma **plataforma de dados** que permita a LODLog:

1. **Prever** atrasos, falhas mecanicas e picos de demanda
2. **Prevenir** quebras, rupturas de estoque e multas
3. **Otimizar** rotas, alocacao de frota e reposicao de estoque

**Meta de negocio:** reduzir custos em 20% e aumentar o SLA de entrega para 95% em 12 meses, utilizando modelos de IA alimentados por dados confiaveis e bem estruturados.

---

# 2. Levantamento de Requisitos: Os 5 Vs dos Dados

Antes de projetar qualquer pipeline, o grupo deve responder as perguntas abaixo para cada fonte de dados identificada:

| V | Pergunta Central | Exemplo para a LODLog |
|---|-----------------|----------------------|
| **Valor** | Que insights podem ser extraidos? | Predicao de atraso, score de saude da frota, ranking de eficiencia de CDs |
| **Veracidade** | Quao precisos e confiaveis sao os dados? | Sensores podem falhar; status de pedido pode ser inconsistente entre TMS e WMS |
| **Variedade** | Quais tipos, formatos e fontes? | JSON (IoT), relacional (ERP/WMS/TMS), CSV (APIs externas), semiestruturado |
| **Velocidade** | Qual a frequencia de geracao e ingestao? | IoT a cada 30s; pedidos em tempo real; estoque a cada 15 min; relatorios diarios |
| **Volume** | Qual o tamanho e taxa de crescimento? | \~864k eventos IoT/dia; \~48k movimentacoes WMS/dia; \~3k eventos TMS/dia |

---

# 3. Modelagem de Dados para IA

## 3.1 Modelo Entidade-Relacionamento (Conceitual/Logico)

A LODLog possui dominios de negocio claros. O grupo deve produzir um diagrama ER contendo pelo menos:

- **Frota:** veiculo, motorista, manutencao, sensor_iot
- **Operacao:** pedido, entrega, rota, parada
- **Estoque:** centro_distribuicao, produto, movimentacao_estoque
- **Cliente:** cliente, contrato, sla
- **Financeiro:** custo_rota, multa, fatura

**Requisitos de modelagem:**
- Definir chaves primarias e estrangeiras
- Aplicar normalizacao ate a 3FN para sistemas transacionais
- Documentar cardinalidades (1:1, 1:N, N:M)

## 3.2 Modelo Dimensional (Star Schema) para Analytics

Para alimentar dashboards e modelos de ML, projetar um Star Schema com:

**Tabela Fato:** `fato_entregas`
- `sk_entrega` (surrogate key)
- `sk_data`, `sk_cliente`, `sk_cd_origem`, `sk_cd_destino`, `sk_veiculo`, `sk_motorista`
- `quantidade_volumes`, `peso_total_kg`, `distancia_km`, `tempo_estimado_min`, `tempo_real_min`
- `custo_combustivel`, `custo_pedagio`, `multa_atraso`
- `indicador_atraso` (0/1 — variavel target para ML)

**Dimensoes:**
- `dim_tempo` (granularidade: dia; atributos: dia, mes, ano, dia_semana, feriado, semana_do_ano)
- `dim_cliente` (segmento, regiao, tempo_de_relacionamento_meses)
- `dim_veiculo` (tipo, ano_fabricacao, capacidade_kg, hodometro_atual)
- `dim_motorista` (tempo_empresa, numero_infracoes, score_seguranca)
- `dim_centro_distribuicao` (regiao, estado, capacidade_m3, eficiencia_operacional)

## 3.3 Preparacao de Dados para Machine Learning

O pipeline deve gerar um dataset `ml_feature_store` contendo:

| Feature | Tipo | Origem | Transformacao |
|---------|------|--------|--------------|
| distancia_km | numerica | API Maps | normalizacao min-max |
| peso_carga_kg | numerica | TMS | binning (leve/media/pesada) |
| hora_saida | ciclica | TMS | seno/cosseno |
| temperatura_media_motor | numerica | IoT | media movel 1h |
| ind_chuva | booleana | API Clima | one-hot encoding |
| status_trafego | categorica | API Maps | ordinal encoding |
| historico_atrasos_7d | numerica | fato_entregas | agregacao rolling window |
| dias_ultima_manutencao | numerica | dim_veiculo | diferenca de datas |

---

# 4. Arquitetura do Pipeline de Dados

## 4.1 Visao Conceitual (Agnostica de Vendor)

```
+-------------------+     +-------------------+     +-------------------+
|   FONTES DE DADOS |     |    INGESTAO       |     |   ARMAZENAMENTO   |
|                   |     |                   |     |   RAW/BRONZE      |
|  Sensores IoT     |---->|  Streaming /      |---->|  Data Lake /      |
|  ERP / WMS / TMS  |---->|  Batch / CDC      |---->|  Object Storage   |
|  APIs Externas    |---->|  API Connectors   |---->|  (JSON/CSV/Avro)  |
|  Planilhas        |---->|  File Ingestion   |     |                   |
+-------------------+     +-------------------+     +-------------------+
                                                        |
                        +-------------------+           v
                        |   ORQUESTRACAO    |     +-------------------+
                        |   (DAGs / Jobs)   |     |   TRUSTED/SILVER  |
                        |                   |     |                   |
                        |  Dependencias,    |<----|  Data Warehouse   |
                        |  Retry, Alerts    |     |  ou Lakehouse     |
                        +-------------------+     |  (Parquet/Delta)  |
                                |                 +-------------------+
                                v                         |
                        +-------------------+             v
                        |   CONSUMO         |     +-------------------+
                        |                   |     |   REFINED/GOLD    |
                        |  BI / Dashboards  |<----|                   |
                        |  ML / APIs        |     |  Agregacoes,      |
                        |  Alertas / Apps   |     |  Features, KPIs   |
                        +-------------------+     +-------------------+
```

## 4.2 Camadas Medallion

### Bronze (Raw)
- Dados ingeridos sem transformacao
- Schema flexivel (schema-on-read)
- Particionamento por data de ingestao (`ano/mes/dia`)
- Retencao: 90 dias (ou conforme politica de governanca)

### Silver (Trusted)
- Deduplicacao (ex: mesmo `veiculo_id` + `timestamp` unico)
- Validacao de schema (campos obrigatorios presentes)
- Limpeza (outliers, formatos inconsistentes)
- Enriquecimento (joins com dimensoes de referencia)
- Conversao para formato colunar (Parquet/Delta) com compressao
- Historico completo (SCD Tipo 2 onde necessario)

### Gold (Refined)
- Agregacoes de negocio prontas para consumo
- Feature store para ML
- Views materializadas para BI
- Dados anonimizados para conformidade LGPD

## 4.3 Batch vs Streaming

| Caracteristica | Batch | Streaming |
|----------------|-------|-----------|
| Latencia | Horas/dias | Segundos/minutos |
| Exemplo LODLog | Fechamento financeiro, ranking semanal | Alerta de temperatura do motor, atraso critico |
| Tecnologias tipicas | Spark SQL, dbt, Airflow | Spark Streaming, Kafka, Flink |
| Custo | Menor | Maior |

**Recomendacao para o projeto:** proponha um pipeline hibrido. Streaming para alertas operacionais; batch para analytics e treinamento de modelos.

---

# 5. Fontes de Dados Detalhadas

## 5.1 IoT — Sensores na Frota

Cada veiculo emite eventos a cada 30 segundos:

```json
{
  "veiculo_id": "TRK-0342",
  "timestamp": "2025-07-14T14:32:05Z",
  "latitude": -22.9068,
  "longitude": -47.0626,
  "velocidade_kmh": 87.4,
  "rpm_motor": 2100,
  "temperatura_motor_c": 94.2,
  "nivel_combustivel_pct": 61.0,
  "peso_carga_kg": 8200,
  "status_freio": "normal",
  "hodometro_km": 124530
}
```

- **Volume:** \~864.000 eventos/dia
- **Variedade:** semiestruturado JSON
- **Veracidade:** sensores podem falhar; exigir validacao de range

## 5.2 Sistemas Transacionais

**ERP:** dados financeiros, faturamento, contratos  
**WMS (Warehouse Management System):** nivel de estoque, posicao no galpao, movimentacoes

```json
{
  "cd_id": "CD-CAMPINAS",
  "produto_sku": "ELE-TV-55P",
  "quantidade_disponivel": 142,
  "quantidade_reservada": 38,
  "posicao_galpao": "A-12-3",
  "ultima_movimentacao": "2025-07-14T11:00:00Z"
}
```

**TMS (Transportation Management System):** pedidos, rotas, alocacao de veiculos

```json
{
  "pedido_id": "PED-2025-084321",
  "cliente_id": "CLI-00891",
  "origem_cd": "CD-CAMPINAS",
  "destino_endereco": "Rua das Flores, 200, Sao Paulo/SP",
  "prazo_entrega": "2025-07-15T18:00:00Z",
  "peso_total_kg": 1250,
  "volumes": 34,
  "prioridade": "alta",
  "veiculo_alocado": "TRK-0342",
  "motorista_id": "MOT-0091"
}
```

- **Volume WMS:** \~48.000 registros/dia
- **Volume TMS:** \~3.000 registros/dia

## 5.3 Dados Externos

| Fonte | Tipo | Frequencia | Volume Estimado |
|-------|------|-----------|-----------------|
| API Google Maps / HERE | Trafego em tempo real | A cada 5 min (veiculos em rota) | \~60.000 requisicoes/dia |
| API INMET / Open-Meteo | Clima e previsao de chuvas | A cada hora | \~1.500 chamadas/dia |
| API ANTT | Alertas de bloqueio de rodovias | Event-driven | \~20 eventos/dia (media) |
| Base IBGE | Dados geograficos de CEP/municipio | Mensal | Base completa \~500 MB |

---

# 6. Transformacao e Qualidade de Dados

## 6.1 Pipeline de Limpeza (Silver)

Para cada fonte, aplicar:

1. **Validacao de schema:** todos os campos obrigatorios presentes?
2. **Deduplicacao:** eliminar registros duplicados por chave natural
3. **Validacao de range:** velocidade entre 0-200 km/h; temperatura motor entre 50-150 C
4. **Padronizacao de codigos:** `status` do pedido mapeado para dominio unico (`concluido`, `em_processamento`, `cancelado`)
5. **Conversao de moedas:** todos os precos para BRL (ou USD) usando taxa do dia
6. **Enriquecimento geografico:** CEP -> cidade, estado, regiao via base IBGE

## 6.2 Framework de Qualidade (baseado no DAMA-DMBOK)

| Dimensao | Definicao | Metrica para LODLog |
|----------|-----------|---------------------|
| **Completude** | Dados obrigatorios estao preenchidos? | % de registros IoT com todos os campos |
| **Acuracia** | Dados refletem a realidade? | % de coordenadas GPS dentro do territorio brasileiro |
| **Consistencia** | Dados sao uniformes entre sistemas? | % de pedidos com mesmo status no TMS e no WMS |
| **Atualidade** | Dados estao atualizados? | Tempo medio entre geracao do evento IoT e disponibilidade na Silver |
| **Unicidade** | Nao ha registros duplicados? | Taxa de duplicacao na camada Bronze |
| **Validade** | Dados obedecem ao formato esperado? | % de timestamps em ISO 8601 valido |

## 6.3 Scorecard de Qualidade

O grupo deve propor um scorecard que consolide as dimensoes acima em um unico indicador (0-100) por fonte de dados e por pipeline.

---

# 7. Casos de Uso de IA/ML para Negocios

O projeto deve prever **pelo menos 2 casos de uso de IA** alimentados pelo pipeline de dados:

## 7.1 Modelo 1 — Predicao de Atraso de Entrega

- **Tipo:** Classificacao binaria (+ regressao para minutos de desvio)
- **Input:** distancia da rota, horario de saida, peso da carga, clima, trafego historico, historico de atrasos do cliente
- **Output:** probabilidade (%) de atraso; estimativa de minutos de desvio
- **Algoritmo sugerido:** XGBoost ou Random Forest
- **Feature store:** usar `ml_feature_store` da camada Gold
- **Impacto de negocio:** reducao de multas contratuais; acionamento proativo do cliente

## 7.2 Modelo 2 — Manutencao Preditiva da Frota

- **Tipo:** Classificacao (risco de falha nos proximos N dias)
- **Input:** temperatura media do motor, RPM medio, vibracao, hodometro, dias desde ultima manutencao, historico de quebras
- **Output:** score de risco 0-100; recomendacao de acao
- **Algoritmo sugerido:** Random Forest com series temporais (ou Isolation Forest para deteccao de anomalias)
- **Impacto de negocio:** reducao de downtime e custos de reboque

## 7.3 Modelo 3 — Previsao de Demanda de Estoque (opcional)

- **Tipo:** Serie temporal
- **Input:** historico de pedidos por SKU/CD, sazonalidade, eventos (feriados, promocoes), tendencia
- **Output:** quantidade sugerida de reposicao por SKU por CD para os proximos 7 dias
- **Algoritmo sugerido:** Prophet, ARIMA ou LSTM
- **Impacto de negocio:** reducao de rupturas e excesso de estoque

## 7.4 Regras de Negocio e Alertas

Propor alertas baseados em thresholds (nao necessariamente ML):

| Regra | Condicao | Acao |
|-------|----------|------|
| R1 | Temperatura motor > 105 C por > 2 min | Notificar motorista + abrir OS de manutencao |
| R2 | Veiculo parado > 30 min em rota (fora de CD) | Alertar supervisor de frota |
| R3 | Previsao de atraso > 60 min E prioridade = "alta" | Acionar atendimento + notificar cliente |
| R4 | Nivel estoque < estoque_minimo * 1,2 | Gerar requisicao automatica de reposicao |

---

# 8. Visualizacao e Storytelling com Dados

## 8.1 Dashboard Operacional (atualizado a cada 15 min)

Painel para supervisores de frota e operadores de CD:

```
+-------------------------------------------------------------+
|  LODLog — Painel Operacional — 14/07/2025 14:32            |
+-------------+-------------+---------------------------------+
| Entregas    | Em rota     | Alertas ativos                  |
| 847 / 923   | 312 veiculos| 🔴 3 atrasos criticos           |
| 91,8% prazo | 45 no CD    | 🟡 8 riscos de manutencao       |
+-------------+-------------+---------------------------------+
```

## 8.2 Dashboard Executivo (atualizado diariamente)

Painel para C-Level e gerentes:

- Custo por km por regiao
- Evolucao do SLA de entrega (meta: 95%)
- Projeao de gastos com manutencao
- Ranking de CDs por eficiencia
- ROI do projeto de dados (custo evitado vs investimento)

## 8.3 Ferramentas Sugeridas

- **Power BI** ou **Tableau** para dashboards de negocio
- **SQL** (views materializadas na camada Gold) como fonte unica de verdade
- **Python + matplotlib/seaborn** para analises exploratorias (EDA)

---

# 9. Governanca, Seguranca e Compliance

## 9.1 LGPD / GDPR

O pipeline deve considerar:

- **Classificacao de dados:** quais dados sao pessoais? (ex: nome do motorista, endereco do cliente)
- **Anonimizacao / pseudonimizacao:** aplicar na camada Gold para dados de consumo
- **Consentimento e finalidade:** garantir que dados pessoais so sejam usados para os propositos informados
- **Direito ao esquecimento:** processo para delecao de dados pessoais sob solicitacao
- **Retencao:** politica de tempo de retencao por camada e por sensibilidade

## 9.2 Linhagem de Dados (Data Lineage)

Documentar o rastreamento desde a origem ate o consumo:

```
sensor_iot (JSON) -> Bronze (raw_iot) -> Silver (trusted_frota)
                                      -> Gold (feature_temperatura_media)
                                      -> Modelo ML (manutencao preditiva)
```

## 9.3 Papéis e Responsabilidades

| Papel | Responsabilidade no Pipeline |
|-------|------------------------------|
| Engenheiro de Dados | Modelagem, pipeline ETL/ELT, qualidade |
| Cientista de Dados | Feature engineering, treinamento de modelos |
| Analista de Negocio | Requisitos, validacao de KPIs, dashboards |
| DBA / Admin de Dados | Performance, backup, seguranca |
| Data Steward | Qualidade, metadados, governanca de dominio |
| Product Owner de Dados | Priorizacao, valor de negocio, backlog |

---

# 10. Arquiteturas Analiticas Modernas (Contexto)

O grupo deve posicionar sua solucao no espectro de arquiteturas modernas:

| Arquitetura | Quando usar | Exemplo LODLog |
|-------------|------------|----------------|
| **Data Warehouse** | Dados estruturados, BI tradicional, SQL padrao | Relatorios gerenciais historicos |
| **Data Lake** | Dados brutos, variedade alta, schema-on-read | Armazenamento de eventos IoT em JSON |
| **Data Lakehouse** | Unifica lake + warehouse; transacoes ACID; ML + BI | **Recomendada para o projeto** |
| **Data Mesh** | Multiplos dominios, times descentralizados, data products | Escala futura: cada CD como dominio autonomo |

**Recomendacao:** para o escopo do trabalho, proponha uma arquitetura **Lakehouse** (camadas Bronze/Silver/Gold) com possibilidade de evolucao para **Data Mesh** caso a LODLog cresca.

---

# 11. MLOps e Integracao entre Engenharia de Dados e IA

O projeto deve explicitar como engenharia de dados habilita ML:

```
+----------------+     +------------------+     +------------------+
|  ENGENHARIA    |     |   FEATURE STORE  |     |   CIENCIA / ML   |
|  DE DADOS      |---->|  (camada Gold)   |---->|                  |
|                |     |                  |     |  Treinamento     |
|  Bronze/Silver |     |  Features        |     |  Validacao       |
|  Qualidade     |     |  versionadas,    |     |  Deploy modelo   |
|  Governanca    |     |  documentadas    |     |  Monitoramento   |
+----------------+     +------------------+     +------------------+
                              |
                              v
                       +------------------+
                       |  MONITORAMENTO   |
                       |  Data Drift      |
                       |  Model Drift     |
                       |  Qualidade       |
                       +------------------+
```

**Entregaveis de MLOps (conceituais):**
- Definicao de feature store na camada Gold
- Processo de retreinamento (periodico ou triggerado por drift)
- Log de predicoes para auditoria
- Monitoramento de data drift (mudanca na distribuicao dos dados de entrada)

---

# 12. Entregaveis do Projeto em Grupo (30% da nota)

## 12.1 Proposta Tecnica (max. 15 paginas)

1. **Resumo Executivo** (1 pagina)
2. **Cenario de Negocio** (1 pagina)
3. **Levantamento dos 5 Vs** (1-2 paginas)
4. **Modelagem de Dados:**
   - Diagrama ER (conceitual/logico)
   - Star Schema proposto
5. **Arquitetura do Pipeline:**
   - Diagrama de fluxo de dados (origem -> consumo)
   - Justificativa das camadas Bronze/Silver/Gold
   - Decisao batch vs streaming
6. **Qualidade de Dados:**
   - Dimensoes avaliadas
   - Scorecard proposto
7. **Casos de Uso de IA:**
   - Pelo menos 2 modelos descritos com inputs, outputs e algoritmos
   - Feature store proposta
8. **Governanca e LGPD:**
   - Classificacao de dados
   - Politica de retencao e anonimizacao
9. **Visualizacao:**
   - Mockup dos dashboards operacional e executivo
10. **Roadmap:** proximos passos e evolucao para Data Mesh

## 12.2 Apresentacao Executiva (15 minutos)

Estrutura sugerida:
- Introducao (1 min)
- Problema de negocio (2 min)
- Arquitetura e modelagem (4 min)
- Casos de uso de IA (4 min)
- Governanca e qualidade (2 min)
- Resultados esperados e ROI (2 min)

## 12.3 Rubrica de Avaliacao do Grupo

| Criterio | Peso | O que avaliar |
|----------|------|--------------|
| Compreensao do cenario | 10% | Problema claro, dados relevantes, impacto mensuravel |
| Modelagem de dados | 20% | ER bem formado, star schema adequado, chaves corretas |
| Arquitetura do pipeline | 20% | Fluxo coerente, camadas justificadas, batch/streaming bem escolhidos |
| Qualidade e governanca | 15% | Dimensoes de DQ, LGPD, linhagem documentada |
| Casos de uso de IA | 20% | Features claras, algoritmos justificados, valor de negocio |
| Apresentacao | 10% | Clareza, storytelling, respostas as perguntas |
| Extras tecnicos | 5% | SQL de criacao de tabelas, queries analiticas, prototipo |

---

# 13. Entregaveis do Projeto Individual (70% da nota)

> Baseado no documento **"Os elementos de uma atividade de dados"**

## 13.1 Relatorio Executivo (max. 10 paginas)

Titulo: **"Planejando o Pipeline de Dados para IA na LODLog"**

### Secao 1: Cenario Selecionado (1 pagina)
Escolha um dos sub-cenarios da LODLog:
- (A) Otimizacao de rotas de entrega
- (B) Predicao de falhas na frota
- (C) Gestao de estoque e reposicao
- (D) Deteccao de fraudes em faturamento

### Secao 2: Fontes de Dados Potenciais (2 paginas)
- Liste 3-5 fontes de dados (internas e externas)
- Para cada fonte: formato, tipo (estruturado/semiestruturado/nao estruturado), frequencia
- Mapeamento para as camadas Bronze/Silver

### Secao 3: Os 5 Vs (2 paginas)
- Valor: que insights e modelos de IA sao viaveis?
- Veracidade: quais desafios de qualidade voce antecipa?
- Variedade: quantos formatos e fontes diferentes?
- Velocidade: qual a cadencia ideal de ingestao e processamento?
- Volume: estimativa de tamanho e crescimento

### Secao 4: Arquitetura Proposta (2 paginas)
- Diagrama simplificado do pipeline individual
- Escolha de ETL vs ELT e justificativa
- Tecnologias sugeridas (pode mencionar vendor, mas deve justificar)

### Secao 5: Queries SQL (2 paginas)
- DDL para criar pelo menos 3 tabelas (fato + 2 dimensoes)
- 2 queries analiticas que respondam perguntas de negocio
- 1 query de qualidade (ex: detectar registros duplicados ou nulos)

### Secao 6: Consideracoes de IA (1 pagina)
- Qual modelo de ML seria alimentado por esse pipeline?
- Quais features seriam extraidas da camada Gold?
- Como garantir qualidade dos dados para o modelo?

## 13.2 Apresentacao (5 minutos)

Sintese dos achados e recomendacoes para a LODLog.

## 13.3 Rubrica de Avaliacao Individual

| Criterio | Peso |
|----------|------|
| Clareza do cenario escolhido | 10% |
| Mapeamento de fontes de dados | 15% |
| Analise dos 5 Vs | 20% |
| Arquitetura coerente e justificada | 15% |
| Qualidade do SQL (DDL + queries) | 20% |
| Conexao com IA / valor de negocio | 15% |
| Apresentacao e comunicacao | 5% |

---

# 14. Exemplo de SQL para Referencia

## 14.1 DDL — Criacao das Tabelas

```sql
-- Dimensoes
CREATE TABLE dim_veiculo (
    sk_veiculo INT PRIMARY KEY,
    veiculo_id VARCHAR(20) NOT NULL,
    placa VARCHAR(10),
    tipo_veiculo VARCHAR(20), -- leve, medio, pesado
    ano_fabricacao INT,
    capacidade_kg DECIMAL(10,2),
    hodometro_atual INT,
    data_inclusao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_tempo (
    sk_data INT PRIMARY KEY,
    data DATE NOT NULL,
    dia INT,
    mes INT,
    ano INT,
    trimestre INT,
    dia_semana INT,
    nome_dia_semana VARCHAR(15),
    feriado BOOLEAN DEFAULT FALSE,
    semana_do_ano INT
);

-- Tabela Fato
CREATE TABLE fato_entregas (
    sk_entrega BIGINT PRIMARY KEY,
    sk_data INT REFERENCES dim_tempo(sk_data),
    sk_cliente INT REFERENCES dim_cliente(sk_cliente),
    sk_veiculo INT REFERENCES dim_veiculo(sk_veiculo),
    sk_motorista INT REFERENCES dim_motorista(sk_motorista),
    sk_cd_origem INT REFERENCES dim_centro_distribuicao(sk_cd),
    sk_cd_destino INT REFERENCES dim_centro_distribuicao(sk_cd),
    pedido_id VARCHAR(30) NOT NULL,
    quantidade_volumes INT,
    peso_total_kg DECIMAL(10,2),
    distancia_km DECIMAL(8,2),
    tempo_estimado_min INT,
    tempo_real_min INT,
    custo_combustivel DECIMAL(10,2),
    multa_atraso DECIMAL(10,2),
    indicador_atraso INT, -- 0 = no prazo, 1 = atrasado (TARGET ML)
    data_inclusao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 14.2 Query Analitica — Eficiencia por CD

```sql
SELECT
    dcd.regiao,
    dcd.estado,
    COUNT(*) AS total_entregas,
    ROUND(AVG(fe.distancia_km), 2) AS distancia_media_km,
    ROUND(AVG(fe.tempo_real_min * 1.0 / NULLIF(fe.tempo_estimado_min, 0)), 2) AS eficiencia_tempo,
    ROUND(SUM(fe.custo_combustivel) / SUM(fe.distancia_km), 2) AS custo_por_km,
    ROUND(SUM(fe.multa_atraso), 2) AS total_multas
FROM fato_entregas fe
JOIN dim_centro_distribuicao dcd ON fe.sk_cd_origem = dcd.sk_cd
JOIN dim_tempo dt ON fe.sk_data = dt.sk_data
WHERE dt.ano = 2025 AND dt.mes = 7
GROUP BY dcd.regiao, dcd.estado
ORDER BY eficiencia_tempo ASC;
```

## 14.3 Query de Qualidade — Deteccao de Duplicatas

```sql
SELECT
    pedido_id,
    COUNT(*) AS ocorrencias,
    MIN(data_inclusao) AS primeira_inclusao,
    MAX(data_inclusao) AS ultima_inclusao
FROM fato_entregas
WHERE sk_data >= 20250701
GROUP BY pedido_id
HAVING COUNT(*) > 1
ORDER BY ocorrencias DESC
LIMIT 20;
```

## 14.4 Query de Feature — Dataset para ML

```sql
SELECT
    fe.sk_entrega,
    fe.distancia_km,
    fe.peso_total_kg,
    dv.capacidade_kg,
    dv.hodometro_atual,
    dt.dia_semana,
    dt.feriado,
    dm.score_seguranca,
    dm.tempo_empresa,
    -- feature agregada: historico de atrasos do cliente nos ultimos 30 dias
    COALESCE(hist.atrasos_30d, 0) AS historico_atrasos_cliente_30d,
    fe.indicador_atraso AS target
FROM fato_entregas fe
JOIN dim_veiculo dv ON fe.sk_veiculo = dv.sk_veiculo
JOIN dim_tempo dt ON fe.sk_data = dt.sk_data
JOIN dim_motorista dm ON fe.sk_motorista = dm.sk_motorista
LEFT JOIN (
    SELECT sk_cliente, SUM(indicador_atraso) AS atrasos_30d
    FROM fato_entregas f2
    WHERE f2.sk_data BETWEEN 20250601 AND 20250630
    GROUP BY sk_cliente
) hist ON fe.sk_cliente = hist.sk_cliente
WHERE fe.sk_data BETWEEN 20250701 AND 20250731;
```

---

# 15. Checklist Final para Entrega

## Projeto em Grupo
- [ ] Diagrama ER (conceitual e logico)
- [ ] Star Schema com fato e dimensoes
- [ ] Diagrama de arquitetura do pipeline
- [ ] Definicao das camadas Bronze/Silver/Gold
- [ ] Analise dos 5 Vs para cada fonte
- [ ] Framework de qualidade com metricas
- [ ] 2+ casos de uso de IA documentados
- [ ] Feature store proposta
- [ ] Mockup de dashboards
- [ ] Consideracoes de LGPD e governanca
- [ ] Roadmap de evolucao

## Projeto Individual
- [ ] Cenario escolhido e justificado
- [ ] 3-5 fontes de dados mapeadas
- [ ] Analise completa dos 5 Vs
- [ ] DDL SQL para 3+ tabelas
- [ ] 2 queries analiticas de negocio
- [ ] 1 query de qualidade
- [ ] Conexao clara entre pipeline e modelo de IA

---

> **Nota do Professor:** Este projeto nao exige implantacao em ambiente de producao. O foco e a **capacidade de projetar** uma solucao de engenharia de dados coerente, tecnicamente fundamentada e alinhada a geracao de valor com IA. Todo modelo, query e decisao arquitetural deve ser justificavel em termos de negocio.
