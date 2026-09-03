# Relatório de Validação Narrativa/Contextual dos Labs — Mundo LODLog

**Data:** 03/09/2026 · **Disciplina:** Arquitetura de Dados e Big Data (MBA FGV)
**Escopo:** coerência do conteúdo dos labs (`Aulas/Aula-1..4-5/Labs/`) com o mundo fictício
**LODLog Transportes e Distribuição S.A.** ("The Lord Of Data Logistics"), definido em `Aulas/LODLog/*.md`.

> Este relatório é **complementar** ao `VALIDACAO-LABS.md` (validação técnica/funcional — execução no
> Databricks Free Edition, bugs de SQL). Aqui o foco é **história e números do cenário fictício**: nomes,
> escala do negócio, dores, convenções de ID, regras de negócio — e garantir que nenhum lab confunde a
> LODLog com a **LODGov** (outro mundo fictício, não relacionado, usado só na Aula 2 para o RPG "As Cinco
> Torres Isoladas").

## Método

Leitura integral de `LAB1.md`, `LAB2.md`, `LAB3.md`, `LAB4.md` e dos 4 `AGENTS.md` de cada Aula, cruzando
cada número/nome/convenção citado contra o cânone em `Aulas/LODLog/The-Lord-Of-Data-Logistics.md` e
`Aulas/LODLog/Projeto-Eng-Dados-IA-para-Negocio.md`.

## Cânone de referência (resumo)

- **Empresa:** LODLog Transportes e Distribuição S.A., fictícia (mas realista), HQ Campinas/SP, fundada em 2010.
- **Escala narrativa:** 450 veículos, 12 centros de distribuição, 3.200 clientes ativos, ~18 mil entregas/mês, faturamento R$ 380 milhões/ano.
- **Dataset de laboratório (recorte piloto, não a narrativa completa):** 5 CDs, 50 veículos, ~50 mil entregas acumuladas (2024–2026).
- **Dor central:** *"Sabemos que estamos perdendo dinheiro, mas não sabemos exatamente onde nem por quê."*
- **Convenções de ID:** `TRK-####` (veículo), `MOT-####` (motorista), `CLI-#####` (cliente), `PED-YYYY-######` (pedido), `CD-<CIDADE>` (centro de distribuição).
- **LODGov** é um mundo fictício **separado** (rede de serviços profissionais estilo RPG) — não deve aparecer misturado com fatos da LODLog.

## Resultado — itens conformes

| Item verificado | Onde | Status |
|---|---|---|
| Nome/natureza fictícia da empresa ("fictícia, mas realista") | LAB1.md | ✅ Conforme |
| Escala narrativa 450 veículos / 12 CDs / ~18k entregas/mês | LAB1.md, LAB2.md | ✅ Conforme, citada de forma idêntica nos dois labs |
| Recorte piloto do dataset (5 CDs / 50 veículos / ~50k entregas 2024–2026) rotulado como subconjunto, não como a narrativa completa | LAB2.md, `AGENTS.md` da Aula 2 | ✅ Conforme — texto explicita "a LODLog 'de verdade' tem..." vs. "o banco de laboratório é um recorte piloto" |
| Cenário de crescimento a 3 anos (1.500 veículos/30 CDs/~60k entregas/3 países) | LAB2.md, Atividade 1.2 | ✅ Conforme — apresentado explicitamente como hipótese futura, não como fato atual |
| Frase-dor "estamos perdendo dinheiro, mas não sabemos onde" | LAB1.md, LAB3.md | ✅ Conforme ao cânone |
| Nenhuma mistura de vocabulário/números da LODGov (aventureiros, 470k profissionais, clãs, US$70,5bi) dentro de `Aulas/Aula-X/Labs/` | Todos os labs | ✅ Confirmado via grep — zero ocorrências |
| Nomes de esquema/tabela (`lodlog_op`, `lodlog_dw`, `fato_entregas`, `dim_*`) consistentes com o cânone técnico do `CLAUDE.md` raiz | LAB2.md, LAB3.md, LAB4.md | ✅ Conforme |
| Convenções de ID (`TRK-####`, `CLI-#####`, etc.) | Todos os labs | ➖ N/A — os labs não criam exemplos de ID à mão; trabalham direto sobre os dados gerados pelo seed, então não há risco de violação |

## Divergências encontradas e corrigidas

Estas não são violações do cânone narrativo em si, mas **inconsistências de referência** deixadas pela
migração para o Databricks Free Edition — o tipo de detalhe que quebra a imersão/coerência do material
para quem segue os labs em sequência. Corrigidas nesta sessão:

| # | Arquivo | Problema | Correção aplicada |
|---|---|---|---|
| 1 | `Aulas/Aula-2/Labs/LAB2.md` (Atividade 2.2) | Instrução pedia para editar `lodlog_modelo_dados_v3.sql` (nome do script original, não existe nesta pasta) | Corrigido para `lodlog_modelo_dados_free.sql`, o arquivo real da pasta |
| 2 | `Aulas/Aula-2/Labs/LAB2.md` (Atividade 3.2) | Texto dizia "o script de seed v3 já criou a mini-dimensão..." | Corrigido para referenciar `lodlog_lab3_seed_free.py` |
| 3 | `Aulas/Aula-4-5/Labs/LAB4.md` (Material de Apoio) | Referências apontavam para a pasta raiz original (`Labs/lodlog_modelo_dados_v3.sql`, `Labs/LAB3.md`, `Labs/AGENTS.md`), preservada intacta e não mais usada pelos alunos | Corrigido para os caminhos reais da versão Free Edition: `../../Aula-2/Labs/lodlog_modelo_dados_free.sql`, `../../Aula-3/Labs/LAB3.md`, `../../Aula-3/Labs/AGENTS.md` |
| 4 | `Aulas/Aula-3/Labs/LAB3.md` (Objetivos + Atividade 3.1) | Texto afirmava "9 variáveis explicativas", mas a tabela da view `vw_features_ml` lista apenas 8 features (excluindo o identificador `sk_entrega` e o target `target_atraso`) | Corrigido para "8 variáveis explicativas" nos dois trechos |

## Itens fora de escopo (decisão editorial, não é erro)

- `Aulas/Aula-2/aula-2.md` (slide deck, fora da pasta `Labs/`) usa a LODGov como cenário de RPG separado
  ("As Cinco Torres Isoladas"), explicitamente descrito como "análogo à LODLog em escala maior" — é
  intencional e não contamina os labs executáveis.
- Diferença entre a escala narrativa (450/12/18k) e o dataset de laboratório (5 CDs/50 veículos/~50k) é
  uma decisão editorial já documentada (ver skill `lodlog-databricks-free`), não uma inconsistência.

## Conclusão

O cânone narrativo da LODLog está **coerente e bem replicado** nos 4 labs — números, dor de negócio e
identidade da empresa se repetem sem contradição, e não há contaminação com o mundo LODGov. As 4
divergências encontradas eram puramente **referências de arquivo/contagem defasadas** da migração para o
Free Edition, já corrigidas nos arquivos `LAB2.md`, `LAB3.md` e `LAB4.md`.
