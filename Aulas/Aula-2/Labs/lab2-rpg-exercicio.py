# Databricks notebook source
import random
# LAB 2 — RPG "As Cinco Torres Isoladas" (template executável)
# Version: free (Unity Catalog: Volume `workspace.lodlog_volumes.raw` em vez de /FileStore, descontinuado)
# Execute: Workspace > Import > Run All
# ============================================
# DINÂMICA: 5 grupos, 1 porta cada. Cada porta = 1 arquitetura com armadilha.
# Scores: Resiliência / Visão / Influência (-4 a +4 por eixo).
# PORTA SECRETA: contratos + governança federada leve (não está na lista!).
# ============================================

# COMMAND ----------
# CÉLULA 1 — Setup
VOL = "/Volumes/workspace/lodlog_volumes/raw"  # Volume UC = substituto do /FileStore (descontinuado)
try:
    spark.sql("USE CATALOG workspace")
    spark.sql("CREATE DATABASE IF NOT EXISTS lodlog_volumes")
    spark.sql("CREATE VOLUME IF NOT EXISTS lodlog_volumes.raw")
    print("✅ Catálogo workspace — RPG pronto")
except Exception as e:
    print(f"⚠️  {e}")

# COMMAND ----------
# CÉLULA 2 — As 5 Portas (arquiteturas) com scores nos 3 eixos
portas = [
    {"porta": 1, "nome": "Conselho Federado dos Domínios", "arquitetura": "Data Mesh puro",
     "ideia": "Autonomia total por domínio (frota, estoque, financeiro)",
     "armadilha": "Coordenação cara, padrões divergem, sem contratos = caos",
     "resiliencia": -2, "visao": 3, "influencia": 0},
    {"porta": 2, "nome": "Lago Único do Conhecimento", "arquitetura": "Lake/Lakehouse centralizado",
     "ideia": "Tudo num só lago governado com Delta",
     "armadilha": "Gargalo central, fila de TI, domínios perdem agilidade",
     "resiliencia": 2, "visao": 1, "influencia": -1},
    {"porta": 3, "nome": "Colheita Silenciosa", "arquitetura": "Data Fabric sobre os silos, sem blueprint",
     "ideia": "Integrar sem mover dado, quick wins sem plano mestre",
     "armadilha": "Sem histórico nem dono: a camada virtual só espelha os silos",
     "resiliencia": -1, "visao": -2, "influencia": 2},
    {"porta": 4, "nome": "Grande Ressaca", "arquitetura": "Big bang para um Data Warehouse corporativo",
     "ideia": "Modelar o DW da empresa inteira de uma vez",
     "armadilha": "IoT e texto livre não cabem no esquema; anos até o primeiro relatório",
     "resiliencia": -4, "visao": -3, "influencia": -2},
    {"porta": 5, "nome": "Tribunal das Leis", "arquitetura": "Governança antes da tecnologia",
     "ideia": "Governança perfeita primeiro",
     "armadilha": "Paralisia por análise, resistência, sem entrega tangível",
     "resiliencia": 1, "visao": -4, "influencia": -3},
]

df_portas = spark.createDataFrame(portas)
df_portas.write.format("delta").mode("overwrite").save(f"{VOL}/rpg/portas")
print("✅ 5 portas registradas")
df_portas.show(truncate=False)

# COMMAND ----------
# CÉLULA 3 — Simulação: grupo escolhe uma porta (input = número da porta)
# PROFESSOR: alterar o valor abaixo para simular a escolha do grupo
porta_escolhida = 2  # ← altere aqui para testar (1-5)

escolha = spark.sql(f"SELECT * FROM delta.`{VOL}/rpg/portas` WHERE porta = {porta_escolhida}").collect()[0]
total = escolha.resiliencia + escolha.visao + escolha.influencia

print(f"\n🏢 GRUPO ESCOLHEU: Porta {escolha.porta} — {escolha.nome}")
print(f"   Arquitetura: {escolha.arquitetura}")
print(f"   Ideia central: {escolha.ideia}")
print(f"   Armadilha: {escolha.armadilha}")
print(f"   Scores → Resiliência:{escolha.resiliencia}  Visão:{escolha.visao}  Influência:{escolha.influencia}  | TOTAL: {total:+d}")

# COMMAND ----------
# CÉLULA 4 — Consequências narradas (dependem da escolha)
consequencias = {
    1: "Os 5 CDs começam a publicar dados cada um num formato. Em 3 meses, ninguém sabe qual é 'a versão verdadeira' do cliente. O CMO pede visão 360 — não tem como entregar sem contratos.",
    2: "O lake central engole tudo, mas a fila de TI cresce. O time de frota espera 3 semanas por um relatório novo. A agilidade prometida virou gargalo.",
    3: "Cada domínio resolve seu pedaço. O TMS usa CDC, o WMS usa batch, o IoT usa streaming — 3 formatos, 3 pipelines, 0 integração. Dívida técnica explode no M3.",
    4: "Tudo foi reescrito. Na semana de go-live, o ERP novo não conversa com o WMS antigo. A operação para 48h. Custo: R$ 2M em multas de atraso.",
    5: "O comitê de governança aprova 14 documentos de padrão. Nenhum pipeline foi construído. O CIO perde a paciência e contrata soluções pontuais — volta ao início.",
}
print(f"\n📢 CONSEQUÊNCIA NARRADA:\n{consequencias[porta_escolhida]}")

# COMMAND ----------
# CÉLULA 5 — Pista para a PORTA SECRETA (professor revela após discussão)
print("""
🔑 A PORTA SECRETA — "Ponte dos Contratos"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Nenhuma das 5 portas tem score alto nos 3 eixos simultaneamente.
A síntese de maior pontuação é:

  • CONTRATOS DE DADOS: acordo formal produtor ↔ consumidor
    (schema, qualidade, SLA, responsabilidades, versionamento)
  • GOVERNANÇA FEDERADA LEVE: decide no nível mais próximo do dado;
    central só quando impacto sistêmico; monitora, não controla.
  • IMPLEMENTAÇÃO: Bronze descentralizado (cada domínio ingere seu raw)
    + Silver/Gold centralizado com Delta + catálogo + registry.

  LODLog hoje = Lakehouse centralizado (porta 2 evoluída).
  LODLog em 30 CDs = Data Mesh + contratos (porta 1 + porta secreta).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

# COMMAND ----------
# CÉLULA 6 — Votação final: qual porta escolheriam AGORA?
print("Após conhecer a porta secreta, votem novamente.")
print("Porta 2 (Lakehouse) é a escolha natural para LODLog hoje.")
print("Porta 1 (Mesh) faz sentido se LODLog escalar para 30+ CDs.")
print("Porta secreta = escolha número 6 — não estava na lista original!")