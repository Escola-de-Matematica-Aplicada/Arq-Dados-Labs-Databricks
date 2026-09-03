# LAB 3 — SQL Avançado e Pipeline de Feature Engineering

**Disciplina** Arquitetura de Dados e Big Data
**Aula** 3 — Organização e Manuseio de Dados em Bases Distribuídas (29 de setembro de 2026)
**Duração do Lab** ~1h30 (em aula)
**Entrega** Queries SQL + view de Feature Store + relatório de qualidade de dados

> **Para quem é este lab:** Você é um profissional que já entende o cenário (Aulas 1–2) e agora precisa **extrair valor dos dados** usando SQL avançado. Este é o **único lab executável obrigatório** da disciplina — você vai escrever queries, criar views e detectar problemas reais nos dados, tudo no Databricks Free Edition.

---

## Antes de começar

1. Crie sua conta gratuita no **Databricks Free Edition** em [databricks.com/learn/free-edition](https://www.databricks.com/learn/free-edition) (não precisa de cartão de crédito) e faça login em [login.databricks.com](https://login.databricks.com).
2. No painel lateral esquerdo, selecione **Workspace** → **Create** → **Git folder** e adicione o endereço do repositório do curso: `https://github.com/Escola-de-Matematica-Aplicada/EDIA-Labs-DataBricks.git`
   *(alternativa: baixe os arquivos e use **Workspace → Import**).*
3. Execute os notebooks, nesta ordem (o compute **Serverless** já vem selecionado — não é preciso configurar nada):
   - `Aulas/Aula-2/Labs/lodlog_modelo_dados_free.sql` (se ainda não executou)
   - `Aulas/Aula-3/Labs/lodlog_lab3_seed_free.py` (levará ~3 min para rodar)
4. Após o seed terminar com sucesso, abra o notebook **`Aulas/Aula-3/Labs/LAB3_apoio_free`** para desenvolver as atividades.
5. Na primeira célula, execute:
   ```sql
   USE CATALOG workspace;
   USE lodlog_dw;
   SHOW TABLES;
   ```

> 💡 *O script carrega ~50 mil entregas fictícias nos schemas `lodlog_op` e `lodlog_dw`, dentro do catálogo `workspace` (o Free Edition usa Unity Catalog — pense nele como o "prédio" onde moram os schemas). Demora uns 3 minutos.*

---

## Objetivos de Aprendizagem

Ao final deste lab, você será capaz de:

1. **Escrever consultas SQL avançadas** — JOINs de múltiplas tabelas, agregações e filtragens pós-agrupamento.
2. **Aplicar Window Functions** — médias móveis, rankings, percentis e NTILE para análise de séries temporais.
3. **Construir uma Feature Store** — uma view consolidada que alimenta modelos de IA com 9 variáveis explicativas e a variável resposta.
4. **Auditar dados** — detectar duplicatas, valores negativos, outliers e quebras de integridade referencial usando SQL.

---

## Parte 1 — Análise Exploratória com SQL (25 min)

> 💡 *Antes de construir qualquer coisa, você precisa conhecer os dados. Estas queries são como o "raio-X" do negócio — revelam padrões que a diretoria precisa ver.*

### Atividade 1.1: Conhecendo os Dados do DW (10 min, individual)

Execute e interprete as três queries abaixo. Escreva **uma frase curta** de interpretação sobre o que o resultado revela para a gestão da LODLog.

**Query 1: Volume de entregas e atrasos por mês**
```sql
SELECT DATE_TRUNC('month', data_entrega) AS mes,
       COUNT(*) AS total_entregas,
       SUM(CASE WHEN minutos_atraso > 0 THEN 1 ELSE 0 END) AS entregas_atrasadas
FROM fato_entregas
GROUP BY 1
ORDER BY 1;
```

**Sua Interpretação:**

**Query 2: Ranking de Centros de Distribuição por eficiência operacional**
```sql
SELECT cd.codigo AS cd_origem,
       ROUND(AVG(fe.minutos_atraso), 2) AS atraso_medio_min,
       ROUND(SUM(fe.custo_combustivel + fe.custo_pedagio), 2) AS custo_total_operacional,
       COUNT(DISTINCT fe.sk_veiculo) AS frota_alocada
FROM fato_entregas fe
INNER JOIN dim_centro_distribuicao cd ON fe.sk_cd_origem = cd.sk_cd
WHERE fe.data_entrega >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY cd.codigo
ORDER BY atraso_medio_min ASC;
```

**Sua Interpretação:**

**Query 3: Correlação entre distância e custo de combustível**
```sql
SELECT corr(distancia_km, custo_combustivel) AS correlacao_distancia_custo
FROM fato_entregas
WHERE data_entrega >= CURRENT_DATE - INTERVAL '30 days';
```

**Sua Interpretação:**

> 💬 *Se a correlação é alta e positiva: quanto mais longe, mais caro. Isso confirma o que o financeiro já desconfiava?*

### Atividade 1.2: Sua Primeira Query Analítica (15 min, individual)

Escreva uma consulta SQL para responder à seguinte pergunta da diretoria comercial:

**"Qual o percentual de entregas no prazo por cliente nos últimos 90 dias, considerando apenas clientes com mais de 10 entregas realizadas no período?"**

**Dicas de implementação:**
- Faça um `INNER JOIN` entre `fato_entregas` e `dim_cliente` (usando as surrogate keys).
- Filtre a data: `fe.data_entrega >= CURRENT_DATE - INTERVAL '90 days'`.
- Use `GROUP BY` na coluna `razao_social` do cliente.
- Filtre os grupos com `HAVING COUNT(*) > 10`.
- Calcule o percentual de pontualidade: entrega "no prazo" se `minutos_atraso = 0` (ou `indicador_atraso = 0`). Divida o volume pontual pelo total e multiplique por 100.
- Ordene do menor percentual (piores clientes) para o maior.

```sql
-- Escreva sua query de pontualidade aqui e execute no Databricks
```

> 💡 *A diretoria quer saber quem são os clientes que mais atrasam. Se um cliente tem 15 entregas e 14 no prazo, a pontualidade é 93%. Se outro tem 50 entregas e 40 no prazo, são 80%. Quem é o problema?*

---

## Parte 2 — Window Functions e Séries Temporais (25 min)

> 💡 *Window Functions são como cálculos em Excel, mas muito mais poderosos: permitem calcular uma métrica para cada linha considerando as linhas "ao redor" dela — sem agrupar e perder detalhes.*

### Atividade 2.1: Média Móvel de Atrasos por CD (10 min, individual)

> *Métricas de tempo de atraso diário são "ruidosas" (variam muito de um dia para outro). Para suavizar as tendências, a gerência pediu a **média móvel de 7 dias** de atrasos, agrupada por centro de distribuição.*

Escreva a query que retorne o CD (código), a data da entrega, o atraso individual da linha e a média móvel das últimas 7 linhas daquele mesmo CD (ordenadas por data).

**Dica Spark SQL:**
```sql
AVG(minutos_atraso) OVER (
  PARTITION BY sk_cd_origem
  ORDER BY data_entrega
  ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
)
```

```sql
-- Escreva sua query de média móvel aqui
```

> 💬 *Se a média móvel de um CD está subindo semana a semana, o que isso significa para a operação?*

### Atividade 2.2: Ranking de Eficiência da Frota (10 min, individual)

Analise o custo de combustível por quilômetro rodado de cada motorista nos últimos 30 dias. A query deve:

1. Agrupar as entregas por `sk_motorista` para obter o custo por km (`SUM(custo_combustivel) / NULLIF(SUM(distancia_km), 0)`).
2. Classificar os motoristas em **quartis (1 a 4)** usando `NTILE(4)`.
3. Calcular o **percentil exato** de eficiência usando `PERCENT_RANK()`.

**Estrutura sugerida:**
```sql
WITH custo_por_motorista AS (
  SELECT sk_motorista,
         SUM(custo_combustivel) / NULLIF(SUM(distancia_km), 0) AS custo_por_km
  FROM fato_entregas
  WHERE data_entrega >= CURRENT_DATE - INTERVAL '30 days'
  GROUP BY sk_motorista
)
SELECT m.nome_completo AS nome_motorista,
       c.custo_por_km,
       NTILE(4) OVER (ORDER BY c.custo_por_km ASC) AS quartil,
       PERCENT_RANK() OVER (ORDER BY c.custo_por_km ASC) AS percentil
FROM custo_por_motorista c
INNER JOIN dim_motorista m ON c.sk_motorista = m.sk_motorista;
```

```sql
-- Escreva sua query de ranking de motoristas aqui
```

> 💬 *Quartil 1 = motorista mais eficiente (gasta menos por km). Quartil 4 = menos eficiente. Isso ajuda a gerência a decidir onde focar.*

### Atividade 2.3: Discussão Analítica (5 min, em grupo)

Debatem: do ponto de vista de arquitetura de banco de dados, por que as **Window Functions** são mais eficientes no Spark SQL do que subqueries correlacionas clássicas?

> 💡 *Dica: pense em quantas vezes o banco precisa "ler" os dados. Com subquery, ele lê várias vezes. Com Window Function, lê uma única vez.*

---

## Parte 3 — Feature Engineering em SQL (30 min)

> 💡 *Cientistas de dados precisam de dados no formato certo para treinar modelos de IA. O seu trabalho aqui é criar uma "vitrine" de dados — uma view que já vem pronta, com todas as variáveis de que o modelo precisa. Isso se chama **Feature Store**.*

### Atividade 3.1: Crie a View de Feature Store `vw_features_ml` (20 min, em grupo)

Os cientistas de dados precisam treinar um modelo preditivo de probabilidade de atraso. O modelo exige que cada linha represente uma entrega com um conjunto unificado de **9 variáveis explicativas (features)** e a **variável resposta (target)**.

Criem a view `vw_features_ml` sob o banco `lodlog_dw` com as seguintes variáveis:

| Nome da Feature | Tipo/Origem | Fórmula / Lógica em SQL |
|---|---|---|
| `sk_entrega` | Identificador | Chave surrogate da entrega (já existe em `fato_entregas`) |
| `distancia_km` | Numérica (Fato) | `distancia_km` (da fato) |
| `peso_total_kg` | Numérica (Fato) | `peso_total_kg` (da fato) |
| `hora_saida` | Numérica (Derivada) | `hour(hora_saida)` |
| `dia_semana` | Numérica (Derivada) | `dayofweek(data_entrega)` (1 = Domingo, 7 = Sábado) |
| `eh_feriado` | Booleana (Dimensão) | Coluna `flag_feriado` da `dim_tempo` (requer JOIN) |
| `temperatura_media_motor` | Numérica (IoT) | Coluna `temperatura_media_motor` (já na fato) |
| `historico_atrasos_7d` | Janela (Móvel) | Média móvel de atraso do mesmo cliente nos últimos 7 dias |
| `dias_ultima_manutencao` | Diferença (Histórica) | Diferença em dias entre `data_entrega` e a data da última manutenção do veículo |
| `target_atraso` | Variável Resposta | `indicador_atraso` (0 = no prazo, 1 = atrasado) |

**Estrutura da view:**
```sql
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
  SELECT veiculo_id, data_conclusao,
         ROW_NUMBER() OVER (PARTITION BY veiculo_id ORDER BY data_conclusao DESC) as rn
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
LEFT JOIN manut_veiculo mv ON fe.sk_veiculo = mv.veiculo_id AND mv.rn = 1 AND mv.data_conclusao <= fe.data_entrega;
```

> 💡 *Ao criar essa view, você está fazendo o trabalho que o cientista de dados precisaria fazer manualmente. É o "Feature Store" — a ponte entre os dados brutos e o modelo de IA.*

### Atividade 3.2: Valide a Feature Store (10 min, individual)

Execute as queries de validação na view recém-criada:

1. **Completude:** Há registros com dados de manutenção nulos? O que isso indica?
```sql
SELECT COUNT(*) FROM vw_features_ml WHERE dias_ultima_manutencao IS NULL;
```

2. **Distribuição do Target:** O dataset está balanceado?
```sql
SELECT target_atraso, COUNT(*) AS volume,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 2) AS pct
FROM vw_features_ml
GROUP BY 1;
```

> 💬 *Se 90% das entregas são "no prazo" e só 10% "atrasadas", o modelo precisa de cuidado para não prever "tudo no prazo" e acertar 90% das vezes sem ser útil.*

3. **Correlação com o target:** A quilometragem está correlacionada com o atraso?
```sql
SELECT corr(distancia_km, target_atraso) AS correlacao_dist_target FROM vw_features_ml;
```

---

## Parte 4 — Qualidade de Dados via SQL (15 min)

> 💡 *Na vida real, os dados sempre têm problemas. O seu papel como profissional de dados é **caçar os erros antes que o erro caçe você**. Estas queries vão detectar anomalias que foram propositalmente inseridas no banco.*

### Atividade 4.1: Auditoria Automática de Dados (10 min, individual)

O notebook de seed introduziu anomalias na tabela `fato_entregas` para simular problemas reais de pipelines. Escrevam consultas SQL que detectem:

1. **Registros Duplicados:** Encontrem registros com o mesmo `pedido_id` (deveria ser único por grain).
```sql
-- Escreva sua query para encontrar pedido_id duplicados
```

2. **Valores Inválidos / Negativos:** Detectem registros com campos físicos negativos (distância, peso ou custos).
```sql
-- Escreva sua query para valores negativos
```

3. **Outliers de Tempo:** Identifiquem registros com atrasos absurdamente altos (> 1.000 min, ou seja, mais de ~16h) ou adiantamentos fisicamente impossíveis (adiantados mais de 8h, isto é, < −480 min).
```sql
-- Escreva sua query para outliers de atraso/adiantamento
```

4. **Inconsistência de Integridade (Orfãos):** Identifiquem entregas na fato que apontam para clientes (`sk_cliente`) inexistentes no cadastro (`dim_cliente`).
```sql
-- Escreva sua query de auditoria referencial (Anti-Join)
```

### Atividade 4.2: Conexão com o Trabalho em Grupo (5 min)

Para cada tipo de anomalia identificada:

- **Qual a causa provável?** (erro de ingestão? sistema de origem enviou errado? pipeline quebrou?)
- **Como você limparia isso nas camadas Bronze e Silver** do seu pipeline?

> 💡 *Na arquitetura Medallion (que vocês viram na Aula 2): a camada Bronze guarda tudo como veio (raw). A Silver é onde você limpa. Se um dado nasce errado, você descobre na Silver e corrige — sem perder o raw original.*

---

## ---- fim da parte obrigatória ----

## Material de Apoio e Referências

- **Conteúdo da Aula 3** (`aula-3.md`): Cloud IaaS/PaaS/SaaS, Hadoop/Spark/Hive, pipelines ETL/ELT, Lambda/Kappa, arquitetura em camadas.
- **Syllabus** (`syllabus.md`): seção Módulo 3.
- **Modelo de dados**: `../../Aula-2/Labs/lodlog_modelo_dados_free.sql` (DDL adaptada ao Free Edition).
- **Seed de dados**: `lodlog_lab3_seed_free.py` (nesta pasta — gera os ~50 mil registros com anomalias).
- **Notebook de apoio**: `LAB3_apoio_free.ipynb` (nesta pasta).
- **Referência**: `AGENTS.md` — regras do ambiente Databricks Free Edition.

**Dica do Professor:** Este é o único lab executável. O importante não é a query perfeita — é o raciocínio analítico por trás dela. Se um aluno escreveu a query e obteve resultado, ele aprendeu.

---

## Notas para o Facilitador

| Item | Detalhe |
|------|---------|
| **Duração total** | ~1h30 (90 min) |
| **Teoria** | Pipelines, ETL/ELT, Window Functions (~30 min) |
| **Prática** | Queries SQL, Feature Store, Data Quality (~60 min) |
| **Entrega** | Queries executadas + view `vw_features_ml` criada + relatório de anomalias |
| **Próxima aula** | 03/10 — Módulo 4: Miniprojeto de Data Lake (sessão dupla) |

**Próximo passo:** Aula 4-5 é o **miniprojeto** (70% individual + 30% grupo). Baseia-se em tudo o que foi visto aqui: dados, arquitetura, queries e quality.
