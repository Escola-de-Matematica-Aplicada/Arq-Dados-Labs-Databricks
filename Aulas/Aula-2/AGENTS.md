# Contexto da Pasta: Aula 2 — Ferramentas para Gerenciamento de Dados Distribuídos

**Aula 2** do Módulo 2 (28 de setembro de 2026). NoSQL, DW/Lake/Lakehouse/Mesh/Fabric, Arquitetura Medallion (Bronze/Silver/Gold), zonas Zaloni e RPG "As Cinco Torres Isoladas".

## Principais arquivos
- `aula-2.md` — Conteúdo completo do slide deck (≈597 linhas): NoSQL (KV/Documento/Coluna/Grafo), evolução DW→Lake→Lakehouse, Data Mesh vs Data Fabric, matriz decisória, Medallion/Zaloni, RPG com 5 portas + porta secreta, lab Medallion ao vivo.
- `../../../Labs/lodlog_modelo_dados_v3.sql` e `lodlog_lab3_seed_v3.py` — Scripts de referência para o lab.

## Regras e padrões
- Mesma estrutura slide-deck com `<!-- Slide number: N -->` e validação GraphRAG `[DRIFT-xx]`.
- RPG "As Cinco Torres Isoladas" — 5 portas arquiteturais com armadilhas; porta secreta = contratos de dados + governança federada leve.
- **Alternativa/reforço:** se o RPG for abertura (30–40 min), o restante é lab técnico de mapeamento para Medallion.
- Materiais de apoio originais em `docs/Aulas-de-outros-cursos/Aula 8 Arquitetura de Dados/`.

## Informações relevantes
- Aula conecta o "quê" (Aula 1) ao "onde guardar" (arquiteturas).
- Conexão direta com LAB2 (modelagem ER + Star Schema) e LAB4 (miniprojeto lakehouse).
- Porta secreta sintetiza: **Bronze descentralizado / Silver-Gold centralizado** com contratos.
- Conceitos-chave: poliglota persistence, lakehouse = infra + Medallion = padrão organizacional.
