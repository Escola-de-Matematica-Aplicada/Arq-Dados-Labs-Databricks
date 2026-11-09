The Lord Of Data Logistics - LODLog Transportes e Distribuição S.A.

Empresa fictícia para servir de linha de base para o trabalho em grupo.

Consideramos essa linha de base a título da grande diversidade de perfis alunos.

# Visão Geral da Empresa LODLog

A LODLog Transportes e Distribuição S.A. é uma empresa brasileira de logística com sede em Campinas/SP, fundada em 2010. Opera com:

* 450 veículos de carga (leves, médios e pesados)
* 12 centros de distribuição espalhados pelo Brasil
* 3.200 clientes ativos no setor varejista e industrial
* \~18.000 entregas/mês
* Faturamento anual: R$ 380 milhões

# O Problema de Negócio

“Sabemos que estamos perdendo dinheiro, mas não sabemos exatamente onde nem por quê.” — Diretor de Operações, LODLog Dores identificadas pelo negócio:

| Dor | Impacto Estimado |
| --- | --- |
| 23% das entregas chegam com atraso | Multas contratuais de R$ 4,2 MM/ano |
| Retrabalho por falta de dados de inventário | +R$ 1,8 MM em horas extras |
| Decisões de rota baseadas em planilhas Excel | +18% de consumo de combustível |
| Manutenção corretiva (quebras na estrada) | R$ 2,1 MM/ano em reboque e downtime |
| Relatórios gerenciais entregues com 5 dias de atraso | Perda de janela para decisão tática |

# Objetivo Estratégico

Arquitetar (e explicar) uma plataforma de dados em tempo real que permita à LODLog prever, prevenir e otimizar suas operações logísticas — reduzindo custos em 20% e aumentando o SLA de entrega para 95% em 12 meses.

# Fontes de Dados (Camada de Entrada)

## Dados de IoT — Sensores na Frota

Cada veículo possui um dispositivo embarcado que emite eventos a cada 30 segundos:

{
 "veiculo\_id": "TRK-0342",
 "timestamp": "2025-07-14T14:32:05Z",
 "latitude": -22.9068,
 "longitude": -47.0626,
 "velocidade\_kmh": 87.4,
 "rpm\_motor": 2100,
 "temperatura\_motor\_c": 94.2,
 "nivel\_combustivel\_pct": 61.0,
 "peso\_carga\_kg": 8200,
 "status\_freio": "normal",
 "hodometro\_km": 124530
}

Volume estimado: 450 veículos × 2 eventos/min × 60 min × 16h = \~864.000 eventos/dia

## Dados de Sistemas Transacionais (ERP / WMS / TMS)

Extraídos via API REST ou CDC (Change Data Capture) dos sistemas legados:

### Nível de estoque (WMS):

{
 "cd\_id": "CD-CAMPINAS",
 "produto\_sku": "ELE-TV-55P",
 "quantidade\_disponivel": 142,
 "quantidade\_reservada": 38,
 "posicao\_galpao": "A-12-3",
 "ultima\_movimentacao": "2025-07-14T11:00:00Z"
}

Volume estimado: 12 CDs × \~4.000 movimentações/dia (recebimento, picking, expedição, transferência) = \~48.000 registros/dia (\~38 MB/dia em JSON) 9

### Notas:

WMS Warehouse Management System

É um software que gerencia operações de warehouse/centro de distribuição, Controlando:

* **Inventário** — níveis de estoque em tempo real
* **Localização** — onde cada item está armazenado
* **Movimentação** — entradas, saídas, transferências
* **Processamento de pedidos** — picking, packing, shipping

No contexto do seu trabalho, o WMS aparece como uma das **fontes de dados transacionais** (junto com ERP e TMS), de onde se extraem dados de nível de estoque para o pipeline de dados.

Exemplo:

\*\*Nível de estoque (WMS):\*\*
{"produto": "...", "estoque\_atual": 150, "estoque\_minimo": 100, ...}

E a regra de negócio: SE nivel\_estoque\_CD < estoque\_minimo × 1.2 → Gerar requisição automática de reposição no **WMS**

### Pedido de entrega (TMS):

{
 "pedido\_id": "PED-2025-084321",
 "cliente\_id": "CLI-00891",
 "origem\_cd": "CD-CAMPINAS",
 "destino\_endereco": "Rua das Flores, 200, São Paulo/SP",
 "prazo\_entrega": "2025-07-15T18:00:00Z",
 "peso\_total\_kg": 1250,
 "volumes": 34,
 "prioridade": "alta",
 "veiculo\_alocado": "TRK-0342",
 "motorista\_id": "MOT-0091"
}

Volume estimado: \~600 pedidos/dia × 5 eventos de status (criação → alocação → coleta → trânsito → entrega) = \~3.000 registros/dia (\~3,5 MB/dia em JSON) 10

### Notas:

**TMS** = **Transportation Management System** (Sistema de Gestão de Transporte)

Gerencia operações logísticas de movimentação de cargas:

* **Planejamento de rotas** — otimização de entregas
* **Rastreamento de veículos** — localização em tempo real
* **Gestão de frotas** — veículos, motoristas, combustíveis
* **Otimização de carga** — cubagem, peso, compatibilidade
* **Custos de transporte** — fretes, pedágios, indicadores KPI

No contexto do trabalho, o TMS aparece como fonte de dados para rastrear os **veículos do transporte de carga** — funcionando em conjunto com **AWS IoT Core** para captação de dados em tempo real (por exemplo).

## Dados Externos

|  |  |  |  |
| --- | --- | --- | --- |
| Fonte | Tipo | Frequência | Volume Estimado |
| API Google Maps | Tráfego em tempo real | Contínuo | \~60.000 requisições/dia (312 veículos em rota × a cada 5 min × 16h); \~480 MB/dia |
| API INMET / Open-Meteo | Clima e previsão de chuvas | A cada hora | \~1.500 chamadas/dia (62 localidades: 12 CDs + 50 trechos de rota); \~4,5 MB/dia |
| API ANTT | Alertas de bloqueio de rodovias | Event-driven | \~20 eventos/dia (média), picos de 100 em chuvas fortes; \~40 KB/dia |
| Base IBGE | Dados geográficos de CEP/município | Trimestral | Base completa \~500 MB; atualização trimestral (PNADC) \~10 MB; consultas ad-hoc \~5 MB/dia |

## Ideias para visão executiva

Custo por km por região

Evolução do SLA de entrega (meta: 95%)

Projeção de gastos com manutenção

Ranking de CDs por eficiência

## Ideias para alertas em tempo real

Regra 1: SE temperatura\_motor > 105°C por mais de 2 minutos

→ Notificar motorista via App + Abrir OS de manutenção no ERP

Regra 2: SE veiculo parado por > 30 min em rota

→ Alertar supervisor de frota via SNS

Regra 3: SE previsão\_atraso > 60 min E pedido.prioridade = "alta"

→ Acionar equipe de atendimento + Notificar cliente via e-mail

Regra 4: SE nivel\_estoque\_CD < estoque\_minimo × 1.2

→ Gerar requisição automática de reposição no WMS
