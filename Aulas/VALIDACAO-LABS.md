# Relatório de Validação dos Labs — Databricks Free Edition

**Data:** 31/08/2026 · **Disciplina:** Arquitetura de Dados e Big Data (MBA FGV)
**Método:** simulação de execução em ambiente local Spark 3.5.3 + Delta Lake 3.2.1 (equivalente funcional do runtime do Databricks Free Edition), executando o seed completo e **todas** as queries dos labs, incluindo os gabaritos dos exercícios.

## Resumo

| Lab | Aula | Executável? | Status |
|-----|------|-------------|--------|
| LAB 1 — Mapeamento do Ecossistema | 1 | Não (atividade em grupo) | ✅ Revisado (texto e coerência) |
| LAB 2 — Modelagem para Analytics | 2 | Parcial (DDL + queries) | ✅ Queries validadas · DDL adaptada (`lodlog_modelo_dados_free.sql`) |
| LAB 3 — SQL Avançado + Feature Store | 3 | **Sim** (lab principal) | ✅ 20/20 queries validadas (`lodlog_lab3_seed_free.py`, `LAB3_apoio_free.ipynb`) |
| LAB 4 — Miniprojeto Data Lake | 4-5 | Sim (starter) | ✅ Pipeline Bronze→Silver→Gold executado de ponta a ponta (`lab4_miniprojeto_starter.py`) |

## Números da simulação (seed Free)

- Seed completo em **~1 min** local (esperar ~3 min no Serverless do Free Edition).
- `lodlog_op`: 14 tabelas (49.770 entregas, 149.371 itens, 42.702 movimentações, 49.770 eventos de telemetria).
- `lodlog_dw`: `fato_entregas` = **50.000 linhas** (49.770 limpas + 230 anômalas), `dim_tempo` = 1.004, demais dims OK.
- Anomalias detectáveis pelas queries do LAB 3: **100** pedidos duplicados, **50** valores negativos, **29** outliers de atraso (1 caiu fora do limiar por sorteio — aceitável), **50** órfãos de `sk_cliente`.
- `vw_features_ml`: **50.000 linhas** (1 por entrega), target balanceado 50,2% / 49,8%.
- Starter LAB 4: Bronze IoT 5.118 → Silver 4.949 (169 linhas de sujeira removidas — material de discussão em aula); Gold com 2 tabelas + query de insight.

## Bugs encontrados e corrigidos (nas versões *_free*)

1. **Seed quebrava na `dim_tempo`** — coluna `descricao_feriado` 100% `NULL` causa `CANNOT_DETERMINE_TYPE` no `createDataFrame`. Corrigido preenchendo "Feriado nacional" nos feriados. *(O original `Labs/lodlog_lab3_seed_v3.py` mantém o bug.)*
2. **LAB 3, Atividade 2.2** — a query de ranking usava `m.nome_motorista`, coluna que não existe em `dim_motorista` (o nome é `nome_completo`). Corrigido no `LAB3.md` e no notebook de apoio.
3. **Gabarito da `vw_features_ml` multiplicava linhas** — o `LEFT JOIN` do histórico por `(sk_cliente, data_entrega)` gerava 68.762 linhas em vez de 50.000 (clientes com >1 entrega no mesmo dia). Corrigido: o CTE `hist_cliente` agora expõe `sk_entrega` e o JOIN é 1:1 pela chave da entrega.
4. **Limiar de outlier inconsistente** — o texto do LAB 3 pedia atraso "> 1440 min", mas o seed injeta outliers a partir de 1.001 min. Texto alinhado para "> 1.000 min ou < −480 min".
5. **Números do cenário divergentes** — LAB 1 dizia "12 CDs / 18 mil entregas/mês" e LAB 2 "5 CDs / 50k entregas/mês". Padronizado: narrativa = 450 veículos, 12 CDs, ~18 mil entregas/mês; o **dataset** de laboratório é um recorte piloto (5 CDs, 50 veículos, ~50 mil entregas 2024–2026), agora explicado no LAB 2.
6. **LAB 1 chamava a LODLog de "empresa real"** — corrigido para "empresa fictícia (mas bem realista)".

## Adaptações ao Databricks Free Edition

- O **Community Edition foi descontinuado**; todos os labs agora apontam para o Free Edition: conta em https://www.databricks.com/learn/free-edition, login em https://login.databricks.com, compute **Serverless** (não há criação de cluster), **Unity Catalog** habilitado.
- Todos os scripts começam com `USE CATALOG workspace` (com fallback tolerante no Python) — no Free Edition os schemas `lodlog_op`/`lodlog_dw`/`lodlog_bronze|silver|gold` vivem no catálogo `workspace`.
- `OPTIMIZE ... ZORDER` no seed agora é tolerante a falhas (o Free Edition tem Predictive Optimization em tabelas gerenciadas).
- No Unity Catalog as constraints `PRIMARY KEY`/`FOREIGN KEY` da DDL são **informativas** (não fiscalizadas) — o que preserva o exercício de caça a duplicatas/órfãos do LAB 3.

## Limitação conhecida (decisão didática, não corrigida)

- Na `vw_features_ml`, `dias_ultima_manutencao` fica `NULL` em ~30 mil linhas porque o CTE pega apenas a **última** manutenção do veículo (`rn = 1`) e exige que ela seja anterior à entrega — se a última manutenção for posterior, o histórico anterior é ignorado. O exercício 3.2.1 usa exatamente esses nulos para discussão de completude; um "as-of join" correto é sugestão de extensão avançada para a Aula 4-5.

## Arquivos originais

Os arquivos da disciplina original (Engenharia de Dados para IA, Community Edition) foram **preservados intactos** em `/workspaces/Labs/`. As versões adaptadas vivem em `Aulas/Aula-X/Labs/`.
