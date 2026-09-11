---
name: lodlog-databricks-free
description: Contexto e ferramentas para manter/validar os labs LODLog da disciplina "Arquitetura de Dados e Big Data" (MBA FGV) no Databricks Free Edition — inclui harness de simulação local Spark+Delta, bugs conhecidos e decisões editoriais.
---

# Skill: Labs LODLog no Databricks Free Edition

## Quando usar
Qualquer tarefa neste repositório que envolva: editar/validar labs (`Aulas/Aula-X/Labs/`), o seed de dados, a DDL, o starter do miniprojeto, ou dúvidas sobre o ambiente Databricks Free Edition da disciplina.

## O que foi feito (sessão de 31/08/2026)
Adaptação dos labs da disciplina original (Engenharia de Dados para IA, Databricks **Community Edition** — descontinuado) para a disciplina **Arquitetura de Dados e Big Data** no **Databricks Free Edition**, com linguagem acessível a alunos executivos. Execução simulada localmente (Spark 3.5.3 + Delta 3.2.1): seed completo + todas as queries dos labs + starter do LAB 4. Relatório completo: `Aulas/VALIDACAO-LABS.md`.

## Mapa dos artefatos (versões adaptadas — editar ESTAS, não as de `Labs/`)
- `Aulas/Aula-1/Labs/LAB1.md` — teórico (5 Vs, OLTP/OLAP, IaaS/PaaS/SaaS).
- `Aulas/Aula-2/Labs/LAB2.md` + `lodlog_modelo_dados_free.sql` — arquiteturas + normalização 2FN→3FN + Star Schema (DDL).
- `Aulas/Aula-3/Labs/LAB3.md` + `lodlog_lab3_seed_free.py` + `LAB3_apoio_free.ipynb` — único lab executável obrigatório (SQL avançado, feature store, data quality).
- `Aulas/Aula-4-5/Labs/LAB4.md` + `lab4_miniprojeto_starter.py` — miniprojeto (70%+30% da nota), starter Medallion executável.
- `Labs/` (raiz) = material ORIGINAL preservado; não editar para a nova disciplina.

## Fatos do ambiente Databricks Free Edition (validados)
- Community Edition foi descontinuado. Free Edition: conta em https://www.databricks.com/learn/free-edition, login em https://login.databricks.com; **Serverless only**; **Unity Catalog** (catálogo padrão `workspace`).
- Todo script começa com `USE CATALOG workspace` (no Python, com try/except para tolerar Spark local sem UC).
- PK/FK no Unity Catalog são constraints **informativas** — essencial para o LAB 3 (duplicatas/órfãos continuam entrando).
- `OPTIMIZE ... ZORDER` manual pode conflitar com Predictive Optimization → no seed free está embrulhado em try/except.

## Bugs conhecidos corrigidos nas versões _free_ (NÃO reintroduzir)
1. `dim_tempo.descricao_feriado` toda NULL → `CANNOT_DETERMINE_TYPE` no `createDataFrame`. Fix: preencher "Feriado nacional" nos feriados.
2. `dim_motorista` não tem `nome_motorista`; a coluna é `nome_completo`.
3. `vw_features_ml`: JOIN do histórico deve ser por `sk_entrega` (JOIN por `sk_cliente`+`data_entrega` multiplica linhas: 68.762 em vez de 50.000).
4. Limiar de outlier de atraso: seed injeta 1.001–5.760 min e −1.440…−481 → enunciado usa "> 1.000 min ou < −480 min".
5. `CREATE OR REPLACE TABLE ... AS SELECT` não funciona no catálogo Hive local → usar `DROP TABLE IF EXISTS` + `CREATE TABLE ... USING DELTA AS` (funciona nos dois ambientes).
6. **`/FileStore` (DBFS público) está DESABILITADO no Free Edition com Unity Catalog** — erro real do aluno: `[DBFS_DISABLED] Access is denied on path: /FileStore/bronze/iot/_delta_log`. Padrão correto (aplicado em 2026-09-11, renomeado no mesmo dia a pedido do professor, nos 3 scripts da Aula 2: `lab2-medallion-bronze-silver-gold.py`, `lab2-nosql-simulation.py`, `lab2-rpg-exercicio.py`): criar schema + Volume UC (`CREATE DATABASE IF NOT EXISTS lodlog_volumes` + `CREATE VOLUME IF NOT EXISTS lodlog_volumes.raw`) e gravar em `/Volumes/workspace/lodlog_volumes/raw/...` via constante `VOL` definida FORA do try/except (para existir também em Spark local nas validações do harness). Leitura via `delta.\`{VOL}/...\``. Cuidado: patch programático com `{{VOL}}` dentro de f-string SQL vira texto literal `{VOL}` não-interpolado — conferir o resultado de todo replace. Validado no harness local (pyspark 3.5.3 + delta 3.2.1): os 3 scripts rodam Run-All sem erro de path (o `USE CATALOG workspace` falhando em local é esperado e capturado pelo try/except).

## Decisões editoriais
- Narrativa LODLog canônica: **450 veículos, 12 CDs, ~18 mil entregas/mês** (fictícia); o dataset de lab é um **recorte piloto**: 5 CDs, 50 veículos, ~50 mil entregas (2024–2026). Explicado no LAB2.md.
- Limitação didática aceita: `dias_ultima_manutencao` NULL em ~30 mil linhas (CTE usa só a última manutenção `rn=1`) — os nulos alimentam a discussão de completude do exercício 3.2.1.
- Números de referência da simulação: fato = 50.000 (230 anômalas: 100 dup + 50 neg + 29~30 outliers + 50 órfãos); target 50/50.

## Como revalidar (harness em `tools/`)
```bash
pip install pyspark==3.5.3 delta-spark==3.2.1
cd <pasta-de-trabalho-temporária>
python /workspaces/.skills/lodlog-databricks-free/tools/run_seed.py /workspaces/Aulas/Aula-3/Labs/lodlog_lab3_seed_free.py   # ~1 min
python /workspaces/.skills/lodlog-databricks-free/tools/validate_labs.py                                                     # roda todas as queries dos labs
```
Atenção: os scripts usam `WAREHOUSE` hardcoded apontando para um scratchpad de sessão antiga — ajuste a constante `WAREHOUSE` nos dois arquivos para um diretório novo antes de rodar. O validador divide células `%sql` por `;` — fragmentos só-comentário geram falso ❌ (ignorar).
- `tools/make_free_versions.py` — regenera seed/DDL free a partir dos originais de `Labs/` (transformações programáticas).
- `tools/make_lab3_apoio.py` — regenera `LAB3_apoio_free.ipynb`.

## Pendências / próximos passos possíveis
- Publicar os novos arquivos no repositório GitHub que os alunos importam (`EDIA-Labs-DataBricks`) — os labs referenciam esse Git folder.
- `CLAUDE.md` da raiz ainda descreve a disciplina original (Community Edition, seed v1) — atualizar se a nova disciplina virar a principal.
- Validação em workspace real do Free Edition (a simulação local não cobre quotas Serverless nem UI).
