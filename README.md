# Arquitetura de Dados e Big Data — Labs (MBA FGV)

Material dos laboratórios da disciplina **Arquitetura de Dados e Big Data**, todos construídos sobre
o mesmo estudo de caso: a **LODLog Transportes e Distribuição S.A.**, uma transportadora fictícia
com frota conectada por sensores IoT, sistemas ERP, WMS e TMS e APIs externas.

Plataforma: **Databricks Free Edition** — crie sua conta em
https://www.databricks.com/learn/free-edition (gratuito, sem cartão; compute Serverless e Unity Catalog).

## Como usar

1. No Databricks: **Workspace → Create → Git folder** e cole a URL deste repositório
   (ou importe arquivo por arquivo: Workspace → Import).
2. Abra o lab da aula (`LABn.ipynb` é o roteiro em formato de notebook; `LABn.md` é a mesma coisa para ler no GitHub).
3. Os notebooks `.py` executam com **Run All**.

| Aula | Lab | O que você faz | Executável |
|---|---|---|---|
| 1 | [LAB 1](Aulas/Aula-1/Labs/LAB1.md) | Diagnóstico do cenário: tipos de dados, OLTP × OLAP, 5 Vs, modelos de nuvem | não |
| 2 | [LAB 2](Aulas/Aula-2/Labs/LAB2.md) + [RPG](Aulas/Aula-2/Labs/RPG-lodlog.md) | Escolher uma arquitetura (5 portas) e lidar com as consequências; Medallion na prática | sim — rode antes o seed `lodlog_lab2_seed_free.py` |
| 3 | [LAB 3](Aulas/Aula-3/Labs/LAB3.md) | Desenhar o pipeline por domínio e executá-lo, em lote e streaming, até o motor preditivo | sim — `lab3_pipeline_motor_preditivo.py` |
| 4–5 | [LAB 4](Aulas/Aula-4/Labs/LAB4.md) | Miniprojeto: construir e avaliar o data lake do seu cenário | sim — `lab4_miniprojeto_starter.py` |

**Avaliação:** [guia do trabalho em grupo (30%)](Aulas/Aula-4/Labs/GUIA-ENTREGA-grupo.md) ·
[guia de estudo da prova (70%)](Aulas/Aula-4/Labs/GUIA-ESTUDO-PROVA.md)

**Descoberta:** [as 26 perguntas da sessão de desenho de arquitetura (ADS)](docs/ref/ADS-questionario-serra.md),
distribuídas pelos cinco labs — a Ficha ADS do grupo vira o quadro branco do miniprojeto.

**Cenário:** [The Lord of Data Logistics](docs/LODLog/The-Lord-Of-Data-Logistics.md) ·
[por que esta arquitetura? (dossiê de decisões)](docs/LODLog/Por-que-esta-arquitetura.md) ·
[diagramas do modelo de dados](Diagramas/)

> Ordem importante: o seed da Aula 2 (`Aulas/Aula-2/Labs/lodlog_lab2_seed_free.py`) cria as tabelas
> `lodlog_op` e `lodlog_dw` usadas no LAB 2, no notebook de apoio do LAB 3 e no LAB 4.
> Os notebooks do LAB 3 e do LAB 4 geram os próprios dados e rodam sozinhos.
