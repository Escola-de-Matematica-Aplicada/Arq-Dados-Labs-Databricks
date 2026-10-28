# Por que esta arquitetura? — O dossiê de decisões da LODLog

> **Para que serve este documento.** As aulas mostram *o que* existe (tipos de dado, DW, lake, lakehouse, mesh, cloud, ETL/ELT, governança) e os labs mostram *como* construir. Falta o fio que explica **por que a LODLog escolhe o que escolhe** — e em que condição escolheria outra coisa. Este dossiê é esse fio. Ele é usado nas cinco aulas e é a **fonte de evidência** para as entregas em grupo e individual.
>
> Os fatos marcados com 🆕 são novos no caso: completam o cenário com as restrições que qualquer arquiteto perguntaria antes de desenhar (pessoas, dinheiro, legado, contratos, expansão). Sem eles, nenhuma arquitetura é "certa" ou "errada" — só diferente.

---

## 1. A regra do jogo: toda decisão tem uma cadeia

Nenhuma escolha de arquitetura vale por si. Ela vale porque **responde a uma dor do negócio, dentro das restrições da empresa**. Em toda aula, lab e entrega, a pergunta "por quê?" é respondida com esta cadeia:

```
DOR do negócio  →  PERGUNTA que o negócio quer responder  →  REQUISITO do dado
   (com R$)            (quem pergunta, com que frequência)      (latência, histórico,
                                                                  variedade, confiança)
        →  DECISÃO de arquitetura  →  O QUE PERDEMOS com ela  →  GATILHO de revisão
           (e as opções descartadas)    (o trade-off assumido)     (o fato que muda a resposta)
```

Se um elo falta, a decisão é opinião. Se o "o que perdemos" falta, a decisão é propaganda. Se o gatilho falta, a decisão é dogma.

---

## 2. A LODLog que a arquitetura precisa respeitar

### 2.1 O que já sabíamos

| Fato | Número |
|---|---|
| Frota | 450 veículos com IoT (internet das coisas: sensor embarcado), evento a cada 30 s → ~864 mil eventos/dia, ~26 milhões/mês, ~30 GB/mês brutos |
| Rede | 12 CDs (centros de distribuição) · 3.200 clientes ativos · ~18.000 entregas/mês (~600 pedidos/dia) |
| Faturamento | R$ 380 MM/ano |
| Variedade | ~30% estruturado (ERP — sistema de gestão empresarial —, WMS — gestão de armazéns — e TMS — gestão de transportes), ~60% semiestruturado (JSON de IoT e APIs), ~10% não estruturado (PDFs, e-mails, fotos de comprovante) |
| Dores | atraso em 23% das entregas → R$ 4,2 MM/ano em multas · retrabalho de inventário → R$ 1,8 MM · rota em planilha → +18% de combustível · manutenção corretiva → R$ 2,1 MM/ano · relatórios com 5 dias de atraso |
| Meta | −20% de custo e SLA (nível de serviço prometido) de 95% em 12 meses |

### 2.2 🆕 O que o arquiteto pergunta antes de desenhar

| Restrição | Fato proposto | Por que importa para a arquitetura |
|---|---|---|
| **Pessoas** | A área de Dados & BI tem **5 pessoas**: 1 coordenadora de BI (inteligência de negócio), 2 analistas de BI, 1 DBA (administrador de banco de dados) e 1 engenheiro de dados contratado este ano. A TI tem 14 pessoas, com infraestrutura terceirizada. Nos CDs não há ninguém de dados — há um "analista de planilha" por CD. | Uma equipe pequena e central **não sustenta** uma arquitetura federada nem um cluster próprio. Ela precisa de serviço gerenciado e de um único lugar para cuidar. |
| **Dinheiro** | Orçamento de dados aprovado: **R$ 1,6 MM no primeiro ano**. O board exige retorno em até 18 meses. O diesel custa ~R$ 47 MM/ano; os 18% a mais equivalem a ~R$ 7 MM/ano. | Dá para pagar uma plataforma em nuvem e um time enxuto, não um big bang. As dores somam **~R$ 15 MM/ano** (8,1 + ~7 de combustível): o plano precisa capturar uma parte disso cedo. |
| **Legado** | O **ERP** roda on-premises (no data center próprio, SQL Server de 2014) e o **contrato de hosting vence em 14 meses**. O **TMS** (sistema de gestão de transportes) é SaaS (software como serviço) com API e réplica de banco. O **WMS** (sistema de gestão de armazéns) tem **12 instalações em 3 versões diferentes** — por isso o mesmo produto tem SKUs (códigos de produto) diferentes. A telemetria chega por stream do fornecedor de IoT. | Ninguém vai parar 18 mil entregas/mês para reescrever sistemas (fala do CIO). A arquitetura tem de **ler** os sistemas como estão, sem sobrecarregá-los. O vencimento do hosting abre uma janela para ir à nuvem. |
| **Contratos** | Os **40 maiores clientes = 62% do faturamento**. Todos têm SLA de janela de entrega com multa. Em disputa de multa, a LODLog precisa provar o que aconteceu em uma entrega de **até 24 meses atrás**. | O dado de entrega precisa de **histórico imutável e auditável**, não só do "número de hoje". |
| **Regulação** | A LGPD (Lei Geral de Proteção de Dados) cobre a **geolocalização dos motoristas** e o **nome e endereço dos destinatários**. | Segurança e privacidade por camada; o dado pessoal não pode se espalhar em cópias sem dono. |
| **Organização** | Cada gerente de CD tem meta própria e autonomia de ferramenta. **Não há dono de dado formal.** "Entrega" significa uma coisa para o financeiro, outra para o motorista, outra para o cliente e outra para o TMS. | O problema não é só técnico: sem dono e sem definição comum, qualquer arquitetura reproduz a briga dos números. |
| **Horizonte** | O plano estratégico 2028 prevê **30 CDs** (com 2 países da América Latina) e **~2.000 veículos**. | É o gatilho natural para descentralizar (Data Mesh) — *depois*, não agora. |

---

## 3. Das dores aos requisitos

A tabela abaixo é o coração do "por quê". Cada linha transforma uma dor em um requisito de dado; cada requisito empurra a arquitetura numa direção.

| Dor (R$) | Pergunta do negócio | Quem pergunta e quando | Requisito do dado | Implicação para a arquitetura |
|---|---|---|---|---|
| Atraso de 23% → R$ 4,2 MM | Quais entregas de hoje vão atrasar, e por quê? | Torre de controle, **a cada poucos minutos** | Status do TMS em minutos (CDC, captura de mudanças) + IoT + tráfego e clima; previsão ≥ 60 min antes (regra R3) | Streaming **só** nesta faixa; Gold que junta 3 torres |
| Multa contestada | O que aconteceu nesta entrega de 14 meses atrás? | Jurídico e comercial, **por demanda** | Histórico imutável de 24 meses, com versão de cada registro | **Bronze imutável** + histórico (time-travel, a consulta a versões anteriores da tabela, e SCD (dimensão de mudança lenta) Tipo 2) |
| Quebra na estrada → R$ 2,1 MM | Qual caminhão vai quebrar esta semana? | Manutenção, **diário**; alerta crítico em **2 min** (R1) | Temperatura e rpm de 26 mi eventos/mês, faixa válida, sem duplicatas | Lake para volume semiestruturado; streaming para o alerta R1; batch para o modelo |
| Combustível +18% (~R$ 7 MM) | Qual rota custa menos amanhã? | Planejamento, **diário** (D-1) | Histórico de rota × tráfego × clima × peso | **Batch** basta: não precisa de tempo real |
| Inventário → R$ 1,8 MM | Onde vai faltar estoque na próxima semana? | Gerente de CD, **a cada 15 min** | WMS das 12 instalações com o **mesmo SKU** | Padronização na Silver; dado de referência comum (SKU) |
| Relatório em D+5 | Como fechamos a semana? | Diretoria, **semanal** | D+1 confiável, com o mesmo número para todos | Gold com **definição única** de "entrega" e "atraso" (glossário) |
| "Ninguém sabe qual é o número certo" | Os 23% são de quê? | Board | Dado mestre de Cliente e conceito de Entrega com dono | MDM (gestão de dados mestres) do Cliente e governança com papéis |

**Leitura executiva:** só **duas** perguntas exigem resposta em minutos (atraso e alerta do motor). Todo o resto vive bem com D-1 ou 15 min. Essa é a primeira razão para **não** pagar tempo real em tudo.

---

## 4. As seis forças que decidem

Toda decisão abaixo é justificada por uma ou mais destas forças. Nas entregas, cite-as pelo nome.

| Força | Na LODLog | Empurra para |
|---|---|---|
| **F1 — Variedade** | 60% do dado é semiestruturado e cresce mais rápido que o resto | Lake ou lakehouse, não DW (data warehouse) sozinho |
| **F2 — Latência seletiva** | 2 de 7 perguntas pedem minutos; o resto, D-1 | Híbrido: streaming estreito, batch largo |
| **F3 — Confiança e auditoria** | Multas e disputas de até 24 meses; 40 clientes = 62% da receita | Bronze imutável, histórico, qualidade medida |
| **F4 — Equipe e custo** | 5 pessoas, R$ 1,6 MM, retorno em 18 meses | Centralizar, serviço gerenciado, nada de big bang |
| **F5 — Legado e mudança** | ERP com hosting vencendo; WMS em 3 versões; ninguém para a operação | Ler sem sobrecarregar (CDC, réplica); nuvem na janela do hosting |
| **F6 — Governança e significado** | Sem dono; "entrega" com 4 significados; LGPD | Dono e steward (guardião do dado), glossário, contratos de dados, segurança por camada |

---

## 5. A cadeia de decisões, aula a aula

Cada decisão segue o mesmo formato (um ADR, registro de decisão de arquitetura). A aula indicada é onde ela é discutida e onde o aluno encontra a evidência.

### Aula 1 — D0: Por que a LODLog precisa de um ambiente analítico separado dos sistemas?

- **Contexto.** O BI da LODLog hoje consulta o ERP à noite e junta o WMS por planilha enviada pelos CDs. Por isso o relatório sai em D+5: cada CD manda num dia, num formato.
- **Opções.** (a) Continuar consultando os sistemas transacionais. (b) Criar um ambiente analítico separado.
- **Decisão.** (b). Sistemas OLTP (de transação do dia a dia) existem para registrar a entrega, não para responder "por que atrasou". Perguntar a eles em volume derruba o sistema que fatura.
- **Forças.** F5, F3.
- **O que perdemos.** Uma cópia a mais para manter, e um atraso entre o fato e o dado analítico.
- **Evidência.** Lab 1: classificar as 8 fontes por tipo, 5 Vs e ingestão.
- **Gatilho de revisão.** Não há: é uma decisão estrutural.

### Aula 2 — D1: Lakehouse centralizado, e não DW, lake puro ou Data Mesh

- **Contexto.** F1 (60% semiestruturado), F4 (5 pessoas), F3 (auditoria) e o desejo de BI **e** IA no mesmo dado.
- **Opções e por que não, *para a LODLog de hoje*:**

| Opção | Por que não agora |
|---|---|
| **Data Warehouse** | Resolveria o relatório D+5 do ERP, mas deixaria de fora o IoT (60% do dado) e a manutenção preditiva (R$ 2,1 MM). |
| **Data Lake puro** | Guardaria tudo barato, mas sem transações e sem qualidade vira pântano. Com 5 pessoas e sem dono de dado, o pântano é o destino provável. |
| **Data Mesh** | Exige times de dados nos domínios. Os CDs não têm ninguém de dados (F4, F6). Federar agora seria federar o caos — a armadilha da Porta 1 do RPG. |
| **Data Fabric** | É uma camada de integração e catálogo sobre muitas plataformas. A LODLog ainda não tem muitas plataformas para integrar: tem silos. |

- **Decisão.** Lakehouse (lake com garantias de warehouse) num único workspace, com camadas Bronze/Silver/Gold.
- **O que perdemos.** Autonomia dos CDs (o Diretor de Frota vai reclamar) e risco de gargalo na equipe central.
- **Evidência.** RPG "As Cinco Torres Isoladas" (as consequências de cada porta) e Lab 2 (pipeline Medallion).
- **Gatilho de revisão.** 30 CDs e 2 países (plano 2028) **e** times de dados nos domínios → evoluir para Data Mesh com governança federada.

### Aula 2 — D2: Bronze imutável

- **Contexto.** F3: disputas de multa de até 24 meses; os 40 maiores clientes são 62% da receita.
- **Decisão.** O dado entra na Bronze como veio e **nunca é alterado**. A limpeza acontece na Silver.
- **O que perdemos.** Armazenamento (pouco: ~30 GB/mês de IoT) e disciplina para não "consertar" na Bronze.
- **Evidência.** Lab 2 e seed do Lab 4: contagem de linhas Bronze → Silver → Gold; time-travel do Delta.
- **Gatilho de revisão.** Se a LGPD exigir apagar o dado de um titular, a imutabilidade cede por regra (pseudonimização, retenção).

### Aula 2 — D3: MDM consolidado do Cliente

- **Contexto.** O mesmo cliente aparece com códigos e razões sociais diferentes no ERP, no TMS e no WMS. Sem saber quem é o cliente, não dá para dizer **qual** cliente sofre os 23% de atraso nem cobrar a multa certa.
- **Opções.** Registro (só um índice de-para), hub transacional (o MDM vira o sistema de cadastro) ou **consolidado** (o MDM monta o registro de ouro a partir dos sistemas, sem mudar quem cadastra).
- **Decisão.** Consolidado, na Silver/Gold.
- **Por quê.** F5: ninguém muda o processo de cadastro de 3 sistemas em 12 meses. F4: é o estilo que uma equipe pequena consegue operar.
- **O que perdemos.** A causa-raiz (o cadastro ruim) continua na origem. O consolidado corrige o sintoma.
- **Evidência.** Seed do Lab 4, Etapa 7B e TODO 5.
- **Gatilho de revisão.** Quando o cadastro de cliente ganhar um dono e um processo único → hub transacional.

### Aula 3 — D4: Nuvem gerenciada (PaaS), e não Hadoop no data center próprio

- **Contexto.** O hosting do ERP vence em 14 meses (F5); a equipe tem 5 pessoas (F4); o volume é modesto (~30 GB/mês de IoT), mas com picos (chuva, fim de mês).
- **Opções.** Cluster Hadoop próprio (IaaS, infraestrutura como serviço, ou data center) · plataforma gerenciada em nuvem (PaaS, plataforma como serviço) · só SaaS de BI.
- **Decisão.** PaaS. Hadoop próprio exige um time que a LODLog não tem, e se paga pelo pico teórico. Só SaaS de BI não processa IoT.
- **O que perdemos.** Dependência de fornecedor e custo variável que precisa de vigilância (FinOps, a gestão financeira do custo de nuvem).
- **Evidência.** Aula 3: custos e armadilhas da nuvem; Lab 3 no Databricks Free Edition.
- **Gatilho de revisão.** Exigência de dado em território nacional sem região do provedor no país, ou volume que torne o custo variável maior que o fixo.

### Aula 3 — D5: Streaming estreito, batch largo

- **Contexto.** F2: só o alerta do motor (R1, 2 min), o veículo parado (R2, 30 min) e a previsão de atraso (R3, 60 min antes) pedem minutos.
- **Opções.** Tudo batch · tudo streaming (Kappa, um único fluxo contínuo) · **híbrido**.
- **Decisão.** Híbrido: streaming para IoT e status do TMS nas regras R1–R3; batch para rota (D-1), financeiro, IBGE e treino de modelos.
- **O que perdemos.** Dois caminhos para manter, com o risco de o número do painel em tempo real divergir do relatório (o problema clássico da arquitetura Lambda).
- **Evidência.** Lab 3: ingestão do TMS em lote e da telemetria em streaming, até o motor preditivo.
- **Gatilho de revisão.** Se a maioria das perguntas passar a exigir minutos (ex.: cliente pedindo rastreio ao vivo em contrato), migrar para Kappa.

### Aula 3 — D6: CDC para o TMS e o ERP, e não cópia completa

- **Contexto.** F5: o ERP antigo não aguenta `SELECT *` no horário comercial; o TMS tem réplica.
- **Decisão.** CDC (captura de mudanças: lê o log do banco e traz só o que mudou).
- **O que perdemos.** Complexidade de configuração e de mudança de esquema.
- **Evidência.** Aula 3: padrões de ingestão; matriz de decisão do Lab 3.
- **Gatilho de revisão.** Se o ERP for substituído por um SaaS com API de eventos, trocar CDC por eventos.

### Aula 3 — D7: ELT dentro do lakehouse

- **Contexto.** A regra de negócio vai mudar muito no primeiro ano (o que é "entrega", o que é "atraso"). F3 pede o dado original guardado.
- **Decisão.** ELT: carregar bruto e transformar dentro da plataforma. Mudou a regra? Reprocessa a partir da Bronze.
- **O que perdemos.** Custo de processamento repetido e o risco de dado pessoal bruto parado na Bronze (resolvido com acesso restrito, D8).
- **Gatilho de revisão.** Dado sensível que não pode nem entrar bruto → ETL com mascaramento na ingestão.

### Aula 4 — D8: Governança federada leve, com contratos de dados na Silver

- **Contexto.** F6: sem dono de dado; 4 significados para "entrega"; LGPD. O RPG mostrou as duas armadilhas: governança-primeiro paralisa (Porta 5) e ninguém-governa vira pântano (Portas 2 e 3).
- **Decisão.** A **Ponte dos Contratos** (a porta oculta do RPG): a plataforma é central, mas cada domínio tem um **dono** e um **steward** nomeados, e a Silver só aceita dado que cumpre um **contrato** (esquema, regras de qualidade, SLA de atualização, linhagem). O glossário define "entrega" e "atraso" uma única vez.
- **O que perdemos.** Velocidade no começo: cada fonte nova passa a ter contrato.
- **Evidência.** Aula 4 (4 pilares, glossário "o que é uma entrega?") e TODO 4 do seed.
- **Gatilho de revisão.** Quando os domínios tiverem times próprios, a governança deixa de ser leve e vira federada de fato (D1 → Mesh).

### Aula 4 — D9: O dado crítico é a entrega com o prazo prometido — e o endereço do cliente

- **Contexto.** A entrega com o prazo alimenta o SLA de 95%, os R$ 4,2 MM de multa e o faturamento. Sem endereço válido, a entrega atrasa por motivo que nenhum modelo de rota resolve.
- **Decisão.** Tratar Entrega e Cliente/Endereço como elementos críticos de dados: regras de qualidade com limite, dono, steward e registro de ouro.
- **O que perdemos.** Esforço de governança concentrado em poucos dados — os outros esperam.
- **Evidência.** Seed do Lab 4, Etapa 7B, TODO 5 e scorecard de qualidade.

### Aula 5 — D10: O roteiro e os gatilhos

| Quando acontecer… | …revise a decisão | …na direção de |
|---|---|---|
| 30 CDs, 2 países e times de dados nos domínios | D1, D8 | Data Mesh com governança federada |
| Aquisição de uma transportadora com outra nuvem | D1, D4 | Data Fabric (catálogo e integração sobre plataformas) |
| Contratos exigindo rastreio ao vivo para todos | D5 | Kappa |
| Cadastro de cliente com dono e processo único | D3 | MDM hub transacional |
| ERP trocado por SaaS com eventos | D6 | Eventos no lugar de CDC |

---

## 6. "E se a LODLog fosse outra?" — contra-cenários

Para provar que entendeu o porquê, o aluno muda **um fato** e mostra que a resposta muda. Cada contra-cenário muda uma força.

| Contra-cenário | O fato que muda | A arquitetura que passa a fazer sentido | Por quê |
|---|---|---|---|
| **LODLog Contábil** | Sem IoT; a dor é só o relatório financeiro em D+5 | Data Warehouse | F1 desaparece: tudo é estruturado e a pergunta é histórica |
| **LODLog 2028** | 30 CDs, 2 países, cada país com time de dados | Data Mesh | F4 e F6 mudam: há gente nos domínios para ser dona do dado |
| **LODLog + aquisição** | Compra de uma transportadora com outra nuvem e outro ERP | Data Fabric sobre as duas plataformas | F5 muda: o problema passa a ser integrar plataformas, não silos |
| **LODLog Tempo Real** | Contrato com rastreio ao vivo para todos os clientes | Kappa (tudo em streaming) | F2 muda: a maioria das perguntas passa a ser em minutos |
| **LODLog Enxuta** | Orçamento de R$ 300 mil e nenhum engenheiro de dados | Integração incremental com SaaS de BI ligado direto às fontes, sem construir lago, começando pelo dado crítico | F4 radicaliza: só cabe uma versão mínima da Porta 3 (integrar sem mover dado), com o risco dela assumido — sem histórico, a disputa de multa fica sem prova |

---

## 7. Como isto entra nas entregas

### 7.1 Formato de um registro de decisão (ADR) — 1/3 de página

```
DECISÃO: ______________________________________________
DOR que ela ataca (R$ ou %): _________  FORÇAS: F_, F_
OPÇÕES consideradas: (a) ____  (b) ____  (c) ____
ESCOLHEMOS ____ PORQUE ____________________________________
O QUE PERDEMOS: ____________________________________________
EVIDÊNCIA (print/número do notebook ou fato do dossiê): ______
GATILHO: revisaríamos se ____________________________________
```

### 7.2 Em grupo (30%)

- **Pitch, bloco 2 (arquitetura comentada):** além das 3 setas (onde entra a sujeira, onde é barrada, onde nasce o número), **um ADR** da decisão mais importante para o cenário do grupo, com "o que perdemos".
- **Síntese de 1 página:** a seção 1 (fonte × camada) ganha uma coluna **"por que esta ingestão"** ligada a uma força (F1–F6).

### 7.3 Individual (70%)

- **Parte B.4 (vantagens e limitações):** **três ADRs** do cenário — um de armazenamento (D1/D2), um de movimento (D4–D7) e um de governança (D3/D8/D9) — e **um contra-cenário** da seção 6 mostrando que a resposta muda.
- **Parte D.9 (maturidade):** o roteiro com os **gatilhos** da seção 5 (D10) para o cenário do aluno.

---

## 8. Mapa para o professor: onde o porquê aparece em cada aula

| Aula | Momento | O que entra |
|---|---|---|
| 1 | Depois de "LODLog — Dores de Negócio" | Slide **"O que o arquiteto pergunta antes de desenhar"** (seção 2.2) e a tabela dor → requisito (seção 3). Lab 1: nova coluna "que pergunta do negócio esta fonte responde e com que pressa?". |
| 2 | Antes da "Matriz Decisória" | As 6 forças (seção 4) e D1 com a tabela "por que não, para a LODLog de hoje". No RPG, as consequências de cada porta são narradas **pelas forças** (ex.: "Porta 1 cai em F4: os CDs não têm ninguém de dados"). |
| 3 | Fechamento da teoria ("Pipeline fim a fim") | D4–D7 em um slide de ADRs. Lab 3: a matriz de decisão ganha a coluna "por que não a alternativa". |
| 4 | "Lakehouse LODLog — Posicionando a Solução" | Trocar a recomendação afirmada pela cadeia de decisões D1–D9. Teste de "E se" ligado aos gatilhos. |
| 5 | "Linha Narrativa — M1 → M4" | Trocar por "Dor → Decisão → Gatilho": cada módulo com a decisão que tomou e o gatilho que a reverte. Ponte para as ADRs da entrega individual. |
