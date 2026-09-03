# -*- coding: utf-8 -*-
"""Gera Aulas/Aula-3/Labs/LAB3_apoio_free.ipynb (importável no Databricks Free Edition)."""
import json

def md(s):  return {"cell_type": "markdown", "metadata": {}, "source": s}
def code(s): return {"cell_type": "code", "metadata": {}, "source": s,
                     "outputs": [], "execution_count": None}

cells = [
md("""# LAB 3 — Material de Apoio (Databricks Free Edition)

**Disciplina:** Arquitetura de Dados e Big Data · **Cenário:** LODLog Transportes e Distribuição S.A.

## Antes de tudo
1. Este notebook roda no **Databricks Free Edition** (login em https://login.databricks.com) com compute **Serverless** — você não precisa configurar nada.
2. Execute primeiro os notebooks `lodlog_modelo_dados_free.sql` (Aula 2) e `lodlog_lab3_seed_free.py` (~3 min) — eles criam e populam os schemas `lodlog_op` e `lodlog_dw`.
3. No Free Edition os dados vivem no catálogo `workspace` (Unity Catalog). A primeira célula abaixo aponta para o lugar certo.

> 💡 **Como usar:** as células já prontas são o "raio-X" guiado — execute e escreva sua interpretação. As células com `-- TODO` são suas: complete a query usando as dicas do enunciado (`LAB3.md`)."""),

code("""%sql
-- Célula 1 — Aponta para o catálogo e schema corretos e lista as tabelas
USE CATALOG workspace;
USE lodlog_dw;
SHOW TABLES;"""),

md("""## Parte 1 — Análise Exploratória
*Traduzindo: antes de decidir, a diretoria precisa enxergar o padrão. Execute cada query e escreva 1 frase de interpretação de negócio.*"""),

code("""%sql
-- Query 1: Volume de entregas e atrasos por mês
SELECT DATE_TRUNC('month', data_entrega) AS mes,
       COUNT(*) AS total_entregas,
       SUM(CASE WHEN minutos_atraso > 0 THEN 1 ELSE 0 END) AS entregas_atrasadas
FROM fato_entregas
GROUP BY 1
ORDER BY 1;"""),

code("""%sql
-- Query 2: Ranking de Centros de Distribuição (CD) por eficiência operacional
SELECT cd.codigo AS cd_origem,
       ROUND(AVG(fe.minutos_atraso), 2) AS atraso_medio_min,
       ROUND(SUM(fe.custo_combustivel + fe.custo_pedagio), 2) AS custo_total_operacional,
       COUNT(DISTINCT fe.sk_veiculo) AS frota_alocada
FROM fato_entregas fe
INNER JOIN dim_centro_distribuicao cd ON fe.sk_cd_origem = cd.sk_cd
WHERE fe.data_entrega >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY cd.codigo
ORDER BY atraso_medio_min ASC;"""),

code("""%sql
-- Query 3: Correlação entre distância percorrida e custo de combustível
SELECT corr(distancia_km, custo_combustivel) AS correlacao_distancia_custo
FROM fato_entregas
WHERE data_entrega >= CURRENT_DATE - INTERVAL '30 days';"""),

code("""%sql
-- TODO · Atividade 1.2 — Percentual de entregas no prazo por cliente (últimos 90 dias,
-- só clientes com mais de 10 entregas). Complete a query:
SELECT dc.razao_social,
       COUNT(*) AS total_entregas
       -- , calcule aqui o percentual de pontualidade (indicador_atraso = 0)
FROM fato_entregas fe
INNER JOIN dim_cliente dc ON fe.sk_cliente = dc.sk_cliente
WHERE fe.data_entrega >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY dc.razao_social
-- HAVING ...
-- ORDER BY ...
;"""),

md("""## Parte 2 — Window Functions
*Traduzindo: cálculos "em janela" — cada linha enxerga as vizinhas, sem perder o detalhe. É o Excel com esteroides.*"""),

code("""%sql
-- TODO · Atividade 2.1 — Média móvel de 7 linhas de atraso por CD.
-- Dica de estrutura:
--   AVG(minutos_atraso) OVER (
--     PARTITION BY sk_cd_origem
--     ORDER BY data_entrega
--     ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
--   )
SELECT 1;  -- substitua pela sua query"""),

code("""%sql
-- Atividade 2.2 — Ranking de eficiência dos motoristas (custo por km, últimos 30 dias)
WITH custo_por_motorista AS (
  SELECT sk_motorista,
         SUM(custo_combustivel) / NULLIF(SUM(distancia_km), 0) AS custo_por_km
  FROM fato_entregas
  WHERE data_entrega >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY sk_motorista
)
SELECT m.nome_completo AS nome_motorista,
       ROUND(c.custo_por_km, 4) AS custo_por_km,
       NTILE(4) OVER (ORDER BY c.custo_por_km ASC) AS quartil,
       ROUND(PERCENT_RANK() OVER (ORDER BY c.custo_por_km ASC), 3) AS percentil
FROM custo_por_motorista c
INNER JOIN dim_motorista m ON c.sk_motorista = m.sk_motorista
ORDER BY custo_por_km ASC;"""),

md("""## Parte 3 — Feature Store para IA
*Traduzindo: uma "vitrine" de dados prontos para o cientista de dados treinar o modelo de predição de atraso — 9 variáveis explicativas + o alvo.*"""),

code("""%sql
CREATE OR REPLACE VIEW lodlog_dw.vw_features_ml AS
WITH hist_cliente AS (
    SELECT sk_entrega, sk_cliente, data_entrega,
           AVG(minutos_atraso) OVER (
             PARTITION BY sk_cliente
             ORDER BY data_entrega
             ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
           ) AS hist_7d
    FROM fato_entregas
),
manut_veiculo AS (
    -- Última manutenção concluída de cada veículo
    SELECT veiculo_id,
           data_conclusao,
           ROW_NUMBER() OVER (PARTITION BY veiculo_id ORDER BY data_conclusao DESC) AS rn
    FROM lodlog_op.manutencao
    WHERE status = 'Concluída'
)
SELECT
    fe.sk_entrega,
    fe.distancia_km,
    fe.peso_total_kg,
    hour(fe.hora_saida) AS hora_saida,
    dayofweek(fe.data_entrega) AS dia_semana,
    dt.flag_feriado AS eh_feriado,
    fe.temperatura_media_motor,
    ROUND(h.hist_7d, 2) AS historico_atrasos_7d,
    DATEDIFF(fe.data_entrega, mv.data_conclusao) AS dias_ultima_manutencao,
    fe.indicador_atraso AS target_atraso
FROM fato_entregas fe
INNER JOIN dim_tempo dt ON fe.sk_data = dt.sk_tempo
LEFT JOIN hist_cliente h ON fe.sk_entrega = h.sk_entrega  -- grain 1:1 (por entrega)
LEFT JOIN manut_veiculo mv ON fe.sk_veiculo = mv.veiculo_id AND mv.rn = 1 AND mv.data_conclusao <= fe.data_entrega;"""),

code("""%sql
-- Validação 1 · Completude: entregas sem manutenção anterior registrada
SELECT COUNT(*) AS registros_sem_manutencao FROM vw_features_ml WHERE dias_ultima_manutencao IS NULL;"""),

code("""%sql
-- Validação 2 · Balanceamento do target
SELECT target_atraso, COUNT(*) AS volume,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) AS pct
FROM vw_features_ml
GROUP BY 1;"""),

code("""%sql
-- Validação 3 · Correlação da distância com o atraso
SELECT corr(distancia_km, target_atraso) AS correlacao_dist_target FROM vw_features_ml;"""),

md("""## Parte 4 — Qualidade de Dados (caça às anomalias)
*O seed inseriu de propósito 230 registros com problemas em `fato_entregas`. Sua missão: encontrá-los com SQL — como um auditor faria.*"""),

code("""%sql
-- TODO · 4.1a — Duplicatas: entregas com o mesmo pedido_id (deveria ser único)
-- Dica: GROUP BY pedido_id ... HAVING COUNT(*) > 1
SELECT 1;  -- substitua pela sua query"""),

code("""%sql
-- TODO · 4.1b — Valores negativos em campos físicos (distancia_km, peso_total_kg, custo_combustivel)
SELECT 1;  -- substitua pela sua query"""),

code("""%sql
-- TODO · 4.1c — Outliers de tempo: atraso > 1000 min ou adiantamento < -480 min
SELECT 1;  -- substitua pela sua query"""),

code("""%sql
-- TODO · 4.1d — Órfãos: entregas apontando para sk_cliente inexistente em dim_cliente
-- Dica: LEFT JOIN dim_cliente ... WHERE dc.sk_cliente IS NULL  (anti-join)
SELECT 1;  -- substitua pela sua query"""),

md("""---
### Entrega do LAB 3
1. Queries das Partes 1, 2 e 4 executadas com interpretação de 1 frase cada.
2. View `vw_features_ml` criada e validada.
3. Relatório curto: quantas anomalias de cada tipo você encontrou e como as trataria nas camadas Bronze/Silver.

> 🧭 **Próxima parada:** Aula 4-5 — miniprojeto do data lake (a nota da disciplina). Tudo que você fez aqui será reutilizado lá."""),
]

nb = {
  "nbformat": 4, "nbformat_minor": 5,
  "metadata": {"language_info": {"name": "python"},
               "application/vnd.databricks.v1+notebook": {"dashboards": [], "language": "python",
                 "notebookName": "LAB3_apoio_free", "widgets": {}}},
  "cells": cells,
}
open("/workspaces/Aulas/Aula-3/Labs/LAB3_apoio_free.ipynb", "w", encoding="utf-8").write(json.dumps(nb, ensure_ascii=False, indent=1))
print("LAB3_apoio_free.ipynb OK")
