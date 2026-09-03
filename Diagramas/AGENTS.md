# Contexto da Pasta: Diagramas

Pasta de artefatos visuais do projeto EDIA — LODLog. Contém diagramas do modelo de dados analítico (Star Schema DW) e operacional (ER 3FN).

## Principais arquivos
- `LODLog_dw_v3.png` — Diagrama do **modelo dimensional analítico** (Star Schema): `fato_entregas` + dimensões (`dim_tempo`, `dim_cliente` SCD2, `dim_veiculo` SCD2, `dim_motorista` SCD2, `dim_centro_distribuicao` SCD1, `dim_cat_atraso`).
- `LODLog_op_v3.png` — Diagrama do **modelo operacional** (ER 3FN): domínios cliente/endereco/contrato, frota/veiculo/motorista/manutencao/telemetria, estoque/produto, pedido/item_pedido/entrega.

## Regras e padrões
- Formato: PNG (imagens exportadas do Databricks ou ferramenta de modelagem).
- Referência visual para os labs e miniprojeto — não devem ser editados in-place sem atualizar o SQL/seed.

## Informações relevantes
- Os diagramas ilustram a arquitetura de duas camadas: `lodlog_op` (3FN transacional) e `lodlog_dw` (Star Schema analítico).
- LODLog = empresa fictícia de logística (450 veículos, 5 CDs, ~50k entregas/mês) — cenário central da disciplina.
- Usados em LAB2 (modelagem) e LAB4 (apresentação do miniprojeto).
