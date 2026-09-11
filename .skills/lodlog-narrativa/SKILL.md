---
name: lodlog-narrativa
description: Cânone narrativo/contextual do mundo fictício da LODLog (e da LODGov, mundo separado) e checklist para validar coerência de história/números nos labs em Aulas/Aula-X/Labs/. Use quando o pedido for "validar os labs de acordo com o mundo/cenário/narrativa da LODLog", checar coerência do case fictício, ou revisar se um lab novo/editado respeita o cânone.
---

# Skill: Validação narrativa/contextual dos Labs LODLog

## Quando usar

Qualquer tarefa que envolva:
- Validar/revisar `Aulas/Aula-X/Labs/*.md` (ou `AGENTS.md` dessas pastas) contra a história e os números do
  cenário fictício da LODLog.
- Escrever um lab novo, exercício ou exemplo que precise citar a empresa, escala do negócio, dores de
  negócio ou convenções de ID da LODLog.
- Checar se algo confundiu a LODLog com a **LODGov** (mundo fictício diferente, não relacionado).

Esta skill é **complementar** à `lodlog-databricks-free` (que cobre a adaptação técnica dos labs para o
Databricks Free Edition — bugs de SQL, ambiente, Unity Catalog). Esta aqui cobre **história e números do
mundo fictício**, não execução de código.

## Cânone da LODLog (resumo condensado)

Fonte completa: `Aulas/LODLog/The-Lord-Of-Data-Logistics.md` e `Aulas/LODLog/Projeto-Eng-Dados-IA-para-Negocio.md`.

- **Empresa:** LODLog Transportes e Distribuição S.A. — fictícia, mas realista (nunca chamar de "empresa
  real"). HQ em Campinas/SP, fundada em 2010.
- **Escala narrativa (usar sempre estes números para o "mundo real" da LODLog):** 450 veículos, 12 centros
  de distribuição (CDs), 3.200 clientes ativos, ~18 mil entregas/mês, faturamento R$ 380 milhões/ano.
- **Dataset de laboratório (recorte piloto — é um subconjunto, não a narrativa completa):** 5 CDs do
  corredor Sudeste–Sul, 50 veículos, ~50 mil entregas acumuladas (2024–2026). Qualquer lab que cite os
  dois cenários deve deixar explícito que um é a narrativa e o outro é o dataset técnico reduzido.
- **Dor central (citação canônica):** *"Sabemos que estamos perdendo dinheiro, mas não sabemos exatamente
  onde nem por quê."* — Diretor de Operações, LODLog.
- **Tabela de dores/impacto** (usar se um lab citar números de impacto financeiro):
  - 23% das entregas atrasadas → multas de R$ 4,2 MM/ano
  - Retrabalho por falta de dados de inventário → +R$ 1,8 MM em horas extras
  - Rotas por planilha Excel → +18% de consumo de combustível
  - Manutenção corretiva → R$ 2,1 MM/ano em reboque/downtime
  - Relatórios gerenciais 5 dias atrasados → perda de janela de decisão
- **Meta de negócio:** reduzir custos em 20% e elevar SLA de entrega para 95% em 12 meses.
- **Convenções de ID** (se um lab inventar exemplos, devem seguir este padrão):
  `TRK-####` (veículo), `MOT-####` (motorista), `CLI-#####` (cliente), `PED-YYYY-######` (pedido),
  `CD-<CIDADE>` (ex.: `CD-CAMPINAS`).
  Nota: os labs atuais (LAB1–LAB4) não inventam exemplos de ID à mão — trabalham direto sobre os dados
  gerados pelo seed — então esse item raramente é uma fonte real de erro, mas vale checar se um lab novo
  incluir exemplos.
- **Regras de negócio (R1–R4)**, se replicadas em exercícios:
  - R1: temperatura do motor > 105°C por > 2 min → alerta + OS de manutenção
  - R2: veículo parado > 30 min fora do CD → alerta ao supervisor de frota
  - R3: atraso previsto > 60 min E prioridade "alta" → notifica atendimento/cliente
  - R4: estoque < mínimo × 1.2 → gera requisição de reposição automática no WMS
- **Sem elenco de personagens estilo LOTR** — o trocadilho é só no nome da empresa; não inventar
  personagens/nomes próprios "fantásticos" para a LODLog.
- **Esquema técnico** (`lodlog_op`/`lodlog_dw`, `fato_entregas`, `dim_*`) já está descrito e validado
  tecnicamente em `/workspaces/CLAUDE.md` e na skill `lodlog-databricks-free` — aqui só se checa se o
  texto/narrativa em volta dessas tabelas não contradiz os fatos.

## Cânone da LODGov (mundo separado — não confundir com a LODLog)

Fonte: `Aulas/LODLog/LODGov - Abertura de cenário.md`. É um exercício de RPG de **governança de dados**
usado no módulo de arquitetura (ex.: "As Cinco Torres Isoladas" em `Aulas/Aula-2/aula-2.md`), **sem
relação narrativa** com a LODLog:
- Rede de serviços profissionais fictícia, ~470.000 "aventureiros" (profissionais), >150 países,
  faturamento US$ 70,5 bilhões, estrutura de "clãs aliados", 5 "escolas de magia" (linhas de serviço).
- Se um lab da LODLog (pasta `Aulas/Aula-X/Labs/`) citar qualquer um desses números/termos, é
  contaminação cruzada — reportar como erro. É esperado que a LODGov apareça **apenas** no slide deck da
  Aula 2 (`aula-2.md`), fora da pasta `Labs/`, como cenário de RPG alternativo/análogo.

## Checklist de validação (processo repetível)

Para cada lab (`LAB*.md`) e `AGENTS.md` correspondente:
1. Nome/natureza da empresa está correto e dito como fictícia?
2. Números de escala narrativa (450/12/3.200/18k/R$380MM) batem com o cânone quando citados?
3. Se o lab também citar o dataset piloto (5 CDs/50 veículos/~50k), está claramente rotulado como
   subconjunto técnico, não como a narrativa completa?
4. Convenções de ID (se houver exemplos inventados) seguem o padrão `TRK-####`/`MOT-####`/`CLI-#####`/
   `PED-YYYY-######`/`CD-<CIDADE>`?
5. Números de dor/impacto de negócio, meta de negócio e regras R1–R4, se citados, batem com o cânone?
6. `grep -rniE "aventureiro|470\.000|clãs|LODGov|US\$ ?70,5|guilda"` na pasta `Labs/` não retorna nada
   (nenhuma contaminação com LODGov).
7. Referências de arquivo dentro do texto (nomes de `.sql`/`.py`/`.ipynb` citados) apontam para os
   arquivos reais que existem na pasta — migração para Free Edition deixou nomes antigos (`_v3`) presos
   em alguns textos; sempre confirmar que o arquivo citado existe no caminho dito.
8. Contagens explícitas no texto (nº de features, nº de fontes, nº de tabelas) batem com a tabela/lista
   que o próprio lab define a seguir.

## Relatórios já produzidos

- `Aulas/VALIDACAO-LABS.md` — validação **técnica/funcional** (execução no Databricks Free Edition, bugs
  de SQL corrigidos). Não é sobre narrativa.
- `Aulas/VALIDACAO-NARRATIVA-LODLOG.md` — validação **narrativa/contextual** (esta skill), com o resultado
  completo da sessão de 03/09/2026: cânone 100% coerente nos 4 labs, sem contaminação com LODGov; 4
  divergências de **referência de arquivo/contagem** (não de história) encontradas e corrigidas:
  1. `LAB2.md` citava `lodlog_modelo_dados_v3.sql` em vez de `lodlog_modelo_dados_free.sql`.
  2. `LAB2.md` citava "seed v3" em vez do seed Free Edition (`lodlog_lab2_seed_free.py`).
  3. `LAB4.md` apontava para a pasta raiz original (`Labs/...`) em vez dos arquivos migrados em
     `Aula-2/Labs/` e `Aula-3/Labs/`.
  4. `LAB3.md` dizia "9 variáveis explicativas" na Feature Store, mas a tabela definia 8 — corrigido.

## Como reinvocar esta skill numa sessão futura

- Pedidos como "valide os labs de acordo com o mundo/cenário da LODLog", "os labs estão coerentes com a
  narrativa da LODLog?", ou "revise a LODLog nos labs" devem casar com a `description` acima e carregar
  esta skill automaticamente.
- Também é possível apontar direto: "usa a skill em `/workspaces/.skills/lodlog-narrativa/SKILL.md`".
- Antes de reusar qualquer número/arquivo citado aqui como verdade atual, confirme que o arquivo/cânone
  ainda existe como descrito — os docs de `Aulas/LODLog/*.md` são a fonte primária, este SKILL.md é um
  resumo condensado.
