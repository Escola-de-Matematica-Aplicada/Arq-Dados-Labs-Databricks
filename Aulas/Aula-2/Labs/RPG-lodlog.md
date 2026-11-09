# RPG "As Cinco Torres Isoladas" — O Cenário da LODLog

**Disciplina** Arquitetura de Dados e Big Data — Aula 2
**Formato** Dinâmica em grupo, síncrona, sem mestre — 55 min, incluindo a síntese técnica
**Papel de vocês** O CTO da LODLog (e sua equipe de arquitetura)
**Material de origem** Cenário baseado em [`Aulas/LODLog/The-Lord-Of-Data-Logistics.md`](../../../docs/LODLog/The-Lord-Of-Data-Logistics.md)

> ⚠️ **Sigilo do jogo:** este documento contém o cenário, as portas e as regras — mas NÃO as armadilhas de cada porta nem a pontuação. As consequências da sua escolha só são reveladas DEPOIS que o grupo defende a porta. Não leia os notebooks do professor, não procure os comentários do `lab2-rpg-exercicio.py`. A descoberta é o aprendizado.

---

## 1. A Empresa: LODLog Transportes e Distribuição S.A.

Empresa brasileira de logística, sede em Campinas/SP, fundada em 2010:

| | |
|---|---|
| Frota | **450 veículos** de carga (leves, médios e pesados), cada um com dispositivo IoT |
| Rede | **12 centros de distribuição** pelo Brasil |
| Clientes | **3.200 ativos** (varejo e indústria) |
| Operação | **\~18.000 entregas/mês** (\~600 pedidos/dia, 5 eventos de status cada) |
| Faturamento | **R$ 380 milhões/ano** |

### A frase que abriu a crise

> *"Sabemos que estamos perdendo dinheiro, mas não sabemos exatamente onde nem por quê."*
> — Diretor de Operações, LODLog

As dores em números:

| Dor | Impacto estimado |
|---|---|
| 23% das entregas chegam com atraso | Multas contratuais de **R$ 4,2 MM/ano** |
| Retrabalho por falta de dados de inventário | **+R$ 1,8 MM** em horas extras |
| Decisões de rota em planilhas Excel | **+18%** de consumo de combustível |
| Manutenção corretiva (quebras na estrada) | **R$ 2,1 MM/ano** em reboque e downtime |
| Relatórios gerenciais com 5 dias de atraso | Perda da janela de decisão tática |

**Objetivo estratégico declarado pela diretoria:** arquitetar (e saber explicar) uma plataforma de dados em tempo real que permita **prever, prevenir e otimizar** a operação — reduzindo custos em **20%** e elevando o SLA de entrega a **95% em 12 meses**.

---

## 2. As Torres Isoladas: por que o dado não conversa com o dado

A LODLog gera dados de 8 fontes diferentes — e cada uma vive no seu próprio mundo, com suas chaves, formatos e donos:

| Torre (domínio) | Sistemas | O que produz | Volume |
|---|---|---|---|
| **Frota / IoT** | Sensores embarcados | JSON a cada 30s: GPS, velocidade, rpm, temperatura do motor, nível de combustível, peso da carga | **\~864 mil eventos/dia** |
| **Operação / TMS** | Transporte | Pedidos e 5 eventos de status (criação → alocação → coleta → trânsito → entrega) | \~3.000 registros/dia |
| **Estoque / WMS** | Armazém (12 CDs) | Entradas, saídas, picking, transferência | \~48.000 registros/dia |
| **Financeiro / ERP** | Gestão | Pedidos, faturamento, contratos, notas | extraído via API/CDC |
| **Dados Externos** | Google Maps · INMET · ANTT · IBGE | Tráfego (\~60k req/dia), clima (1.500 chamadas/dia), bloqueios de rodovia (\~20/dia, picos de 100), geografia | contínuo + trimestral |

Os payloads são heterogêneos (JSON de sensores com campos que variam por veículo), as chaves não batem entre sistemas (o código de caminhão TRK-0342 no TMS ≠ placa no ERP ≠ id no WMS) e cada domínio grava "do seu jeito". As regras de negócio que a diretoria sonha em automatizar —

- SE `temperatura_motor > 105 °C` por 2 min → abrir OS de manutenção
- SE veículo parado > 30 min em rota → alertar supervisor
- SE `previsão_atraso > 60 min` E prioridade alta → avisar o cliente
- SE `nivel_estoque < mínimo × 1,2` → repor no WMS

— **todas exigem dados de duas ou mais torres ao mesmo tempo**. Hoje, nenhuma consegue.

### O conflito na sala do board

| C-Level | A fala |
|---|---|
| **Diretor de Operações** | "Sabemos que estamos perdendo dinheiro, mas não sabemos exatamente onde nem por quê." |
| **Diretor Comercial** | "Preciso do status de entrega dos meus 3.200 clientes em tempo real, não 5 dias depois!" |
| **CDO** | "Sem governança, cada CD grava os dados do seu jeito — tudo vira pântano!" |
| **CIO** | "Não podemos parar 450 veículos e 18 mil entregas/mês para reescrever tudo!" |
| **Diretor de Frota e Manutenção** | "Cada CD escolhe suas próprias ferramentas de rota — autonomia não se negocia!" |

Todos têm razão. Esse é o problema: **não existe escolha sem trade-off.**

### As restrições que nenhuma porta pode ignorar

| Restrição | Fato |
|---|---|
| Pessoas | 5 pessoas em Dados & BI; ninguém de dados nos 12 CDs |
| Dinheiro | R$ 1,6 MM no 1º ano, retorno em até 18 meses |
| Legado | ERP no data center próprio, hosting vencendo em 14 meses; WMS em 3 versões |
| Contratos | 40 clientes = 62% da receita; disputa de multa de até 24 meses |
| Horizonte | Plano 2028: 30 CDs, 2 países, \~2.000 veículos |

Defendam a porta de vocês **pelas forças** que ela atende e pelas que ela sacrifica (F1 variedade, F2 latência, F3 confiança, F4 equipe e custo, F5 legado, F6 governança). Detalhes no dossiê ["Por que esta arquitetura?"](../../../docs/LODLog/Por-que-esta-arquitetura.md).

---

## 3. As Cinco Portas — Escolham o futuro da LODLog

Cada grupo defende **uma porta** como se fosse o plano diretor de dados da empresa. A "ideia central" está aqui; a **armadilha oculta** de cada porta o professor revela só depois da defesa.

| Porta | Nome no RPG | Arquitetura por trás | A promessa |
|---|---|---|---|
| **1** | Conselho Federado dos Domínios | Data Mesh puro | Cada domínio (frota, estoque, financeiro...) é dono do seu dado como um **produto de dados** com SLA próprio. Autonomia total, velocidade por domínio. |
| **2** | Lago Único do Conhecimento | Data Lake / Lakehouse centralizado | Tudo num só lago governado (Delta). Uma equipe central, um catálogo, uma verdade — BI e ML no mesmo lugar, custo de storage baixo. |
| **3** | Colheita Silenciosa | Data Fabric sobre os silos, sem blueprint | Sem mover dado nem construir lago: uma camada de catálogo e virtualização conecta WMS, TMS, ERP e IoT onde eles estão, fonte por fonte. Quick wins para a diretoria ver resultado já. |
| **4** | Grande Ressaca | Big bang para um Data Warehouse corporativo | Modelar de uma vez, de cima para baixo, o DW da empresa inteira e migrar todos os relatórios no mesmo projeto. Uma só verdade, em tabelas dimensionais, acabando com a dívida de um só golpe. |
| **5** | Tribunal das Leis | Governança antes da tecnologia | Nenhuma linha de código até que padrões, políticas, LGPD e dicionários de dados estejam aprovados. Ordem primeiro, entrega depois. |

### Como o jogo pontua

Após a defesa de cada grupo (2 min), o professor narra as **consequências** da sua porta na história da LODLog e cada porta recebe nota de **-4 a +4** em três eixos:

- **Resiliência** — o plano sobrevive ao crescimento, a falhas e a trocas de diretoria?
- **Visão** — ele enxerga os próximos 3 anos (e os 30 CDs da expansão latino-americana) ou só o trimestre?
- **Influência** — você consegue vender esse plano para os 5 C-Levels que brigam na sala do board?

---

## 4. A Porta Oculta

> 🚪 *Há uma sexta porta na sala. Ela não está na lista. Ninguém a recebe de graça.*

Regras da caçada:

- A porta oculta **só é revelada pelo professor** quando um grupo conseguir **propô-la** com os próprios argumentos — pistas progressivas serão dadas ao longo dos 15 min de rodada de consequências, para quem souber escutar.
- Ela **não é uma sexta arquitetura** no mesmo sentido das outras cinco. Pensem no que as falhas das cinco portas têm em comum: o que faltou à Porta 1 para a autonomia não virar caos? O que faltou à Porta 2 para o lago central não virar gargalo? O que faltou à Porta 5 para a governança não virar paralisia?
- Dica retirada da teoria da aula: a resposta envolve trilhar o que **Data Mesh** responde ("*quem* é dono dos dados?") junto com o que **Data Fabric** responde ("*como* os dados fluem e são governados?") — eles são **complementares, não concorrentes**. E envolve decidir o que fica descentralizado e o que fica centralizado **em cada camada Medallion**, não na arquitetura inteira de uma vez.

O grupo que abrir a porta oculta narra para a turma o que viu do outro lado — e a turma inteira decide no voto final: **qual porta vocês escolheriam agora, com o que sabem?**

---

## 5. Síntese Técnica (depois do jogo — 17 min)

A gamificação termina, o aprendizado começa a virar artefato. Cada grupo mapeia os domínios da LODLog para o Medallion **com o contrato mínimo da Silver**:

| Domínio | Fontes | Bronze (raw) | Silver (limpo, com contrato) | Gold (consumo) |
|---|---|---|---|---|
| Frota/IoT | JSON 30s + ANTT | JSON bruto particionado por data | Delta validado (vel 0–200, temp 50–150), dedup, lineage | `fato_iot_hora` — médias por veículo/hora |
| Operação/TMS | Pedidos + eventos CDC | JSON CDC bruto | Delta com SLA e `atraso_min` calculados | `fato_entregas` + `%` atraso, multas |
| Estoque/WMS | Movimentações 15min | CSV bruto | Delta SCD2, SKUs (códigos de produto) uniformizados | `fato_estoque` — giro, ruptura |
| Financeiro | ERP + IBGE | CSV diário bruto | Parquet tipado, FKs validadas | `fato_faturamento` + enriquecimento IBGE |

**Entregável do grupo:** 1 slide com (a) a porta que defenderam (ou a oculta, se a abriram), (b) justificativa batch × streaming por domínio, e (c) o **contrato mínimo** que exigiriam na Silver da frota: schema + regras de qualidade + SLA de atualização + lineage.

Esse slide é o ensaio geral do miniprojeto das Aulas 4 e 5 (trabalho em grupo, 30%) — onde vocês vão CONSTRUIR no Databricks o lakehouse que aqui apenas defenderam — e das questões dissertativas da prova, que cobram a mesma defesa por escrito.

---

## Cronômetro da Dinâmica (55 min)

| Fase | Tempo |
|---|---|
| Formar 5 grupos (um por porta) e ler o cenário | 3 min |
| Discussão interna: como nossa porta resolve as dores dos 5 C-Levels? | 10 min |
| Defesas (1min30 por grupo) + consequências narradas pelo professor | 12 min |
| Rodada da porta oculta: pistas progressivas até alguém propô-la | 10 min |
| Votação final: qual porta escolheríamos agora? | 3 min |
| Síntese técnica Medallion + contratos (seção 5) | 17 min |

---

## Referências

- Cenário completo: [`Aulas/LODLog/The-Lord-Of-Data-Logistics.md`](../../../docs/LODLog/The-Lord-Of-Data-Logistics.md)
- Lab de execução desta aula: [`LAB2.md`](LAB2.md) e [`lab2-rpg-exercicio.py`](lab2-rpg-exercicio.py)
- Slides da Aula 2 e plano de ensino (Módulo 2): no eClass
- Leituras: Dehghani (2022) *Data Mesh*; Serra (2024) *Deciphering Data Architectures*, cap. 3–5.
