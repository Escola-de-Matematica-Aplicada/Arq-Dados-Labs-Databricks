# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC # LAB 4 — Seed do Miniprojeto: o Data Lake da LODLog (70% pronto · 30% do grupo)
# MAGIC ### Databricks Free Edition · Arquitetura Medallion (Bronze → Silver → Gold)
# MAGIC
# MAGIC **Como este notebook funciona.** Ele já traz **70% do data lake pronto e explicado**: sete fontes
# MAGIC da LODLog (estruturadas, semiestruturadas e não estruturadas), todas carregadas na Bronze, quatro
# MAGIC delas tratadas na Silver, uma Gold de referência, um exemplo de análise e de governança e o tratamento
# MAGIC do **dado mais crítico da empresa — o cliente e seu endereço** (MDM, Etapa 7B).
# MAGIC Os **30% restantes são do grupo** e estão marcados com **🟨 TODO**. São cinco, todos curtos:
# MAGIC
# MAGIC | TODO | O que o grupo faz | Onde | Tempo sugerido |
# MAGIC |---|---|---|---|
# MAGIC | **1** | Leva **uma fonte semi/não estruturada** até a Silver, decidindo as regras de qualidade | Etapa 4 | 20 min |
# MAGIC | **2** | Constrói a **Gold do seu cenário**, escrevendo a métrica-chave | Etapa 5 | 20 min |
# MAGIC | **3** | Escreve a **pergunta de negócio** e a **interpretação** da análise (a consulta já vem pronta) | Etapa 6 | 15 min |
# MAGIC | **4** | Aplica **governança** na Gold do grupo (dono, PII, retenção, regra de qualidade) e define **2 termos do glossário** | Etapa 7 | 20 min |
# MAGIC | **5** | Decide o **registro de ouro do cliente**: de onde vem o endereço oficial e o que é um endereço válido | Etapa 7B | 25 min |
# MAGIC
# MAGIC A **Etapa 8** confere sozinha o que falta e imprime os números para o pitch.
# MAGIC
# MAGIC **Como executar:**
# MAGIC 1. Login no Databricks Free Edition — https://login.databricks.com (compute Serverless).
# MAGIC 2. Workspace › Import › este arquivo › **Run All** (~2 min). Ele roda inteiro mesmo antes dos TODOs —
# MAGIC    as partes do grupo só ficam "em branco" até vocês preencherem.
# MAGIC 3. Preencham os TODOs **na ordem** e rodem de novo a partir da célula editada (ou Run All).
# MAGIC
# MAGIC > 💡 *Vocês não precisam escrever pipeline do zero. O trabalho de vocês é o de um líder de dados:
# MAGIC > decidir regras, escolher a métrica que responde ao negócio, interpretar o número e assumir a governança.*

# COMMAND ----------

# MAGIC %md
# MAGIC ## 🟨 Decisão inicial do grupo — o cenário
# MAGIC
# MAGIC | Cenário | Pergunta de negócio (do caso LODLog) | Fonte extra recomendada para o TODO 1 |
# MAGIC |---|---|---|
# MAGIC | **A — Rotas de entrega** | Como reduzir os 23% de atraso e as multas de R$ 4,2 MM/ano? | `clima` (API externa, JSON) |
# MAGIC | **B — Manutenção preditiva** | Como evitar quebras e R$ 2,1 MM/ano em reboque? | `ocorrencias` (texto livre dos motoristas) |
# MAGIC | **C — Estoque e reposição** | Como evitar ruptura e +R$ 1,8 MM em horas extras? | `clima` (API externa, JSON) |
# MAGIC | **D — Fraude em faturamento** | Como detectar divergências entre TMS e ERP? | `ocorrencias` (texto livre dos motoristas) |

# COMMAND ----------

# 🟨 TODO (decisão do grupo): escolha o cenário — "A", "B", "C" ou "D"
CENARIO = None

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 0 — Catálogo e schemas (pronto)
# MAGIC
# MAGIC Um schema por camada espelha as **zonas do data lake** vistas na Aula 2: a Bronze guarda o dado
# MAGIC como chegou, a Silver o dado confiável e a Gold o dado pronto para o consumo.

# COMMAND ----------

CATALOG = "workspace"
try:
    spark.sql(f"USE CATALOG {CATALOG}")
    print(f"Catálogo ativo: {CATALOG}")
except Exception as e:
    print(f"Aviso: seguindo com o catálogo padrão ({str(e).splitlines()[0]})")

for camada in ["lodlog_bronze", "lodlog_silver", "lodlog_gold"]:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {camada}")
print("Schemas prontos: lodlog_bronze · lodlog_silver · lodlog_gold")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 1 — As sete fontes da LODLog (pronto)
# MAGIC
# MAGIC Na vida real cada fonte chega por um caminho diferente — a telemetria IoT por **streaming** (como no
# MAGIC Lab 3), os sistemas internos por **batch/CDC**, a API de clima por chamadas diárias. Aqui nós
# MAGIC **geramos** os dados, mas com o formato e a sujeira do mundo real: campos faltando, duplicatas,
# MAGIC valores absurdos, chaves órfãs e texto livre.
# MAGIC
# MAGIC | # | Fonte | Sistema | Tipo de dado | Ingestão típica |
# MAGIC |---|---|---|---|---|
# MAGIC | 1 | Telemetria da frota | IoT | **semiestruturado** (JSON) | streaming |
# MAGIC | 2 | Entregas | TMS | estruturado | batch / CDC |
# MAGIC | 3 | Faturas | ERP | estruturado | batch diário |
# MAGIC | 4 | Posição de estoque | WMS | estruturado | batch diário |
# MAGIC | 5 | Clima por CD | API externa (INMET) | **semiestruturado** (JSON) | batch diário |
# MAGIC | 6 | Ocorrências dos motoristas | App do motorista | **não estruturado** (texto livre) | micro-batch |
# MAGIC | 7 | Cadastro de clientes | ERP + TMS + CRM (planilha) | estruturado + **texto livre** (endereço do TMS) | batch diário |
# MAGIC
# MAGIC > Os dados têm **padrões escondidos** que a análise do grupo pode descobrir — não leia o código
# MAGIC > gerador procurando a resposta; descubra pelos dados, como faria na empresa.

# COMMAND ----------

import json
import random
from datetime import date, datetime, timedelta

random.seed(2026)
BASE = date(2026, 8, 1)
DIAS = 60
CDS = {1: "São Paulo", 2: "Campinas", 3: "Rio de Janeiro", 4: "Belo Horizonte", 5: "Curitiba"}
_perfil = random.Random(7)                       # perfis de comportamento da frota e da carteira
VEICULOS_ATENCAO = set(_perfil.sample(range(1, 51), 3))
CLIENTES_ATENCAO = set(_perfil.sample(range(1, 201), 2))

# chuva "verdadeira" por CD e dia — base comum para clima, atrasos e rupturas
chuva = {}
for cd in CDS:
    for d in range(DIAS):
        mm = random.choice([0, 0, 0, 0, 0, 2, 5, 12, 25, 45, 70])
        chuva[(cd, d)] = round(mm * (1.5 if cd == 3 else 1.0) * random.uniform(0.8, 1.2), 1)

# ── Fonte 1 · IoT (JSON) ──
iot_raw = []
for _ in range(20_000):
    v = random.randint(1, 50)
    ts = datetime(2026, 8, 1, 5) + timedelta(minutes=random.randint(0, 60 * 24 * DIAS - 1))
    temp = random.gauss(104, 7) if v in VEICULOS_ATENCAO else random.gauss(92, 5)
    ev = {"veiculo_id": v, "ts": ts.strftime("%Y-%m-%dT%H:%M:%S"),
          "gps": {"lat": round(random.uniform(-30.0, -19.0), 6), "lon": round(random.uniform(-51.5, -43.0), 6)},
          "velocidade_kmh": round(random.uniform(0, 110), 1),
          "temperatura_motor_c": round(temp, 1),
          "nivel_combustivel_pct": round(random.uniform(5, 100), 1)}
    r = random.random()
    if r < 0.02:
        ev.pop("temperatura_motor_c")            # sensor falhou
    elif r < 0.03:
        ev["velocidade_kmh"] = 977.0             # leitura absurda
    elif r < 0.05:
        iot_raw.append(json.dumps(ev))           # evento duplicado
    iot_raw.append(json.dumps(ev))

# ── Fonte 2 · TMS entregas (estruturado, chega como texto de um extrato) ──
tms_raw = []
for eid in range(1, 6_001):
    cd = random.randint(1, 5)
    d = random.randint(0, DIAS - 1)
    v = random.randint(1, 50)
    prevista = BASE + timedelta(days=d)
    p_atraso = 0.12 + (0.35 if chuva[(cd, d)] > 30 else 0) + (0.20 if v in VEICULOS_ATENCAO else 0)
    status = random.choices(["Entregue", "Cancelado", "Em rota"], [0.93, 0.04, 0.03])[0]
    entrega = None
    if status == "Entregue":
        entrega = prevista + timedelta(days=random.randint(1, 3) if random.random() < p_atraso else 0)
    valor = round(random.uniform(120, 4800), 2)
    if random.random() < 0.005:
        valor = -valor                           # valor negativo (erro de digitação)
    linha = (str(eid), f"PED-2026-{eid:06d}", str(random.randint(1, 200)), str(cd), str(v),
             str(random.randint(1, 80)), prevista.isoformat(), entrega.isoformat() if entrega else "",
             status, f"{valor:.2f}", f"{random.uniform(8, 420):.1f}")
    tms_raw.append(linha)
    if random.random() < 0.01:
        tms_raw.append(linha)                    # reenvio duplicado do extrato

# ── Fonte 7 · Cadastro de clientes em três sistemas: o dado crítico da LODLog ──
# Gerador próprio (_cad) para não alterar as demais fontes.
_cad = random.Random(11)
_TIPOS = {"Rua": ["Rua", "R.", "R", "RUA"], "Avenida": ["Avenida", "Av.", "AV", "Avda."],
          "Travessa": ["Travessa", "Tv.", "Trav."], "Alameda": ["Alameda", "Al.", "AL"]}
_RUAS = ["das Flores", "XV de Novembro", "Brasil", "Sete de Setembro", "Tiradentes", "dos Andradas",
         "Rio Branco", "Getúlio Vargas", "Santos Dumont", "da Liberdade", "Marechal Deodoro",
         "Dom Pedro II", "das Palmeiras", "São João", "Barão de Mauá", "Duque de Caxias"]
_BAIRROS = ["Centro", "Vila Nova", "Jardim América", "Santa Cecília", "Boa Vista", "Distrito Industrial",
            "Bela Vista", "São Cristóvão"]
_CIDADES = {1: ("São Paulo", "SP", ["São Paulo", "Sao Paulo", "SAO PAULO", "S. Paulo", "Sampa"], (1000, 5999)),
            2: ("Campinas", "SP", ["Campinas", "CAMPINAS", "Cps"], (13000, 13139)),
            3: ("Rio de Janeiro", "RJ", ["Rio de Janeiro", "RIO DE JANEIRO", "Rio de Jan."], (20000, 23799)),
            4: ("Belo Horizonte", "MG", ["Belo Horizonte", "BELO HORIZONTE", "BH", "B. Horizonte"], (30000, 31999)),
            5: ("Curitiba", "PR", ["Curitiba", "CURITIBA", "Ctba"], (80000, 82999))}
_PREF = {"Supermercado": ["Supermerc.", "Superm."], "Distribuidora": ["Dist.", "Distrib."],
         "Farmácia": ["Farm.", "Farmacia"], "Atacado": ["Atac."], "Comercial": ["Com."], "Mercado": ["Merc."],
         "Drogaria": ["Drog."], "Armazém": ["Armazem", "Armz."], "Empório": ["Emporio"], "Casa": ["Cs."]}
_NOMES = ["Alfa", "Bom Preço", "Central", "Paulista", "Horizonte", "Boa Vista", "São Jorge", "Vitória",
          "Nova Era", "Primavera", "Estrela", "Real", "Santa Clara", "Progresso", "União", "Litoral",
          "Serra Azul", "Ipê", "Aurora", "Vale Verde"]
_TYPO = {"Supermercado": "Supermecado", "Distribuidora": "Distribuidra", "Drogaria": "Drogaira",
         "Farmácia": "Farmáca", "Atacado": "Atacdo", "Comercial": "Comerical"}
_INICIAIS = {"São": "S.", "Santa": "Sta.", "Nova": "N.", "Boa": "B.", "Vale": "V.", "Serra": "Sa."}


def _dv(nums, pesos):
    r = sum(n * p for n, p in zip(nums, pesos)) % 11
    return 0 if r < 2 else 11 - r


def _gera_cnpj():
    base = [_cad.randint(0, 9) for _ in range(8)] + [0, 0, 0, 1]
    d1 = _dv(base, [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    d2 = _dv(base + [d1], [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2])
    s = "".join(map(str, base + [d1, d2]))
    return s, f"{s[:2]}.{s[2:5]}.{s[5:8]}/{s[8:12]}-{s[12:]}"


def _cep_fmt(cep):
    return cep if _cad.random() < 0.5 else f"{cep[:5]}-{cep[5:]}"


_combos = [(p, n) for p in _PREF for n in _NOMES]
_cad.shuffle(_combos)
MESTRE = {}                                        # a "verdade" que nenhum sistema guarda inteira
for i in range(1, 201):
    pref, nome = _combos[i - 1]
    cd_cli = _cad.randint(1, 5)
    cnpj, cnpj_fmt = _gera_cnpj()
    lo, hi = _CIDADES[cd_cli][3]
    MESTRE[i] = {"pref": pref, "nome": nome, "razao": f"{pref} {nome} {_cad.choice(['Ltda', 'S.A.', 'ME', 'Eireli'])}",
                 "cnpj": cnpj, "cnpj_fmt": cnpj_fmt, "cd": cd_cli, "cidade": _CIDADES[cd_cli][0], "uf": _CIDADES[cd_cli][1],
                 "tipo": _cad.choice(list(_TIPOS)), "rua": _cad.choice(_RUAS), "numero": _cad.randint(10, 2999),
                 "bairro": _cad.choice(_BAIRROS), "cep": f"{_cad.randint(lo, hi):05d}{_cad.randint(0, 999):03d}"}
CLIENTES_ENDERECO_RUIM = set(_cad.sample(range(1, 201), 25))

# ERP — cadastro do faturamento (campos separados); 12 empresas cadastradas duas vezes com código novo
cli_erp_raw = []
for i, c in MESTRE.items():
    cli_erp_raw.append((str(i), c["razao"], c["cnpj_fmt"] if _cad.random() < 0.6 else c["cnpj"],
                        f'{c["tipo"]} {c["rua"]}', str(c["numero"]), c["bairro"], c["cidade"], c["uf"],
                        "" if _cad.random() < 0.05 else _cep_fmt(c["cep"])))
for novo_id, i in enumerate(sorted(_cad.sample(range(1, 201), 12)), start=201):
    c = MESTRE[i]
    cli_erp_raw.append((str(novo_id), c["razao"].upper(), c["cnpj"], f'{_cad.choice(_TIPOS[c["tipo"]][1:])} {c["rua"]}',
                        str(c["numero"]), c["bairro"], c["cidade"].upper(), c["uf"], c["cep"]))

# TMS — endereço de entrega digitado pelo operador do CD, em texto livre (1 a 3 versões por cliente)
cli_tms_raw = []
did = 0
for i, c in MESTRE.items():
    ruim = i in CLIENTES_ENDERECO_RUIM
    for _ in range(_cad.choice([1, 1, 2, 2, 3])):
        did += 1
        tipo = _cad.choice(_TIPOS[c["tipo"]])
        rua = c["rua"] if _cad.random() < 0.8 else c["rua"].upper()
        cidade = _cad.choice(_CIDADES[c["cd"]][2])
        num, cep = str(c["numero"]), c["cep"]
        if ruim:                                   # endereço que leva o motorista ao lugar errado
            if _cad.random() < 0.5:
                num = _cad.choice(["S/N", ""])
            else:
                lo, hi = _CIDADES[_cad.choice([k for k in _CIDADES if k != c["cd"]])][3]
                cep = f"{_cad.randint(lo, hi):05d}{_cad.randint(0, 999):03d}"
        bairro = "" if _cad.random() < 0.05 else c["bairro"]
        uf, formato = c["uf"], _cad.randint(1, 3)
        if formato == 1:
            txt = f"{tipo} {rua}, {num} - {bairro} - {cidade}/{uf}" if num else f"{tipo} {rua} - {bairro} - {cidade}/{uf}"
        elif formato == 2:
            txt = f"{tipo} {rua} nº {num}, {bairro}, {cidade} {uf}" if num else f"{tipo} {rua}, {bairro}, {cidade} {uf}"
        else:
            txt = f"{tipo} {rua}, {num}, {cidade}-{uf}" if num else f"{tipo} {rua}, {cidade}-{uf}"
        txt = txt.replace(" -  - ", " - ").replace(", , ", ", ")
        cli_tms_raw.append((str(did), str(i), txt, "" if _cad.random() < 0.03 else _cep_fmt(cep)))

# CRM — planilha do time comercial: nome fantasia escrito de vários jeitos, CNPJ às vezes ausente
crm_raw = []
for n, i in enumerate(sorted(_cad.sample(range(1, 201), 180)), start=1):
    c = MESTRE[i]
    pref, nome = c["pref"], c["nome"]
    r = _cad.random()
    if r < 0.25:
        pref = _cad.choice(_PREF[c["pref"]])                   # abreviação
    elif r < 0.40:
        pref = _TYPO.get(c["pref"], pref)                      # erro de digitação
    if _cad.random() < 0.3:
        nome = " ".join(_INICIAIS.get(w, w) for w in nome.split())
    fantasia = f"{nome} {pref}" if _cad.random() < 0.3 else f"{pref} {nome}"
    if _cad.random() < 0.3:
        fantasia = fantasia.upper()
    q = _cad.random()
    cnpj = c["cnpj_fmt"] if q < 0.5 else (c["cnpj"] if q < 0.75 else "")
    crm_raw.append((f"CRM-{n:04d}", fantasia, cnpj, _cad.choice(_CIDADES[c["cd"]][2]), c["uf"]))
for k, nome in enumerate(["Ômega", "Delta", "Pioneiro", "Cristal", "Sol Nascente", "Jequitibá", "Atlântico", "Guarani"]):
    cd_p = _cad.randint(1, 5)                      # prospects: contas comerciais que ainda não são clientes
    crm_raw.append((f"CRM-{181 + k:04d}", f"{_cad.choice(list(_PREF))} {nome}", _gera_cnpj()[1],
                    _cad.choice(_CIDADES[cd_p][2]), _CIDADES[cd_p][1]))

# Entregas para clientes com endereço ruim no TMS atrasam mais: o motorista procura o lugar certo
_novo = {}
for l in tms_raw:
    if l[0] in _novo or l[8] != "Entregue" or l[7] != l[6] or int(l[2]) not in CLIENTES_ENDERECO_RUIM:
        continue
    _novo[l[0]] = (date.fromisoformat(l[6]) + timedelta(days=_cad.randint(1, 2))).isoformat() if _cad.random() < 0.35 else None
tms_raw = [l[:7] + (_novo[l[0]],) + l[8:] if _novo.get(l[0]) else l for l in tms_raw]

# ── Fonte 3 · ERP faturas (estruturado) ──
erp_raw = []
fid = 0
for l in {l[0]: l for l in tms_raw}.values():      # 1 fatura por entrega entregue
    if l[8] != "Entregue":
        continue
    fid += 1
    valor = abs(float(l[9]))
    p_div = 0.45 if int(l[2]) in CLIENTES_ATENCAO else 0.015
    faturado = round(valor * random.uniform(1.08, 1.45), 2) if random.random() < p_div else valor
    erp_raw.append((str(fid), l[0], l[2], f"{faturado:.2f}", l[7]))
for _ in range(30):                                # faturas órfãs (entrega inexistente)
    fid += 1
    erp_raw.append((str(fid), str(random.randint(90_000, 99_999)), str(random.randint(1, 200)),
                    f"{random.uniform(200, 3000):.2f}", (BASE + timedelta(days=random.randint(0, DIAS - 1))).isoformat()))

# ── Fonte 4 · WMS estoque (estruturado, foto diária por CD × SKU) ──
wms_raw = []
for cd in CDS:
    for sku in range(1, 21):
        for d in range(DIAS):
            demanda = random.randint(5, 40)
            p_rupt = 0.04 + (0.25 if chuva[(cd, d)] > 30 else 0) + (0.10 if cd == 3 and sku <= 4 else 0)
            saldo = 0 if random.random() < p_rupt else random.randint(demanda, demanda * 6)
            if random.random() < 0.005:
                saldo = -random.randint(1, 50)   # saldo negativo (erro de inventário)
            wms_raw.append((str(cd), f"SKU-{sku:03d}", (BASE + timedelta(days=d)).isoformat(),
                            str(saldo), str(demanda), str(demanda * 2)))

# ── Fonte 5 · API de clima (JSON externo) ──
clima_raw = []
for (cd, d), mm in chuva.items():
    reg = {"estacao": f"INMET-A7{cd:02d}", "cd_id": cd, "data": (BASE + timedelta(days=d)).isoformat(),
           "medicoes": {"chuva_mm": mm, "temp_max_c": round(random.uniform(17, 34), 1)},
           "alerta": "laranja" if mm > 45 else ("amarelo" if mm > 25 else None)}
    r = random.random()
    if r < 0.03:
        reg["medicoes"].pop("chuva_mm")          # medição ausente
    elif r < 0.05:
        reg["medicoes"]["chuva_mm"] = 9999.0     # código de erro do sensor
    elif r < 0.08:
        clima_raw.append(json.dumps(reg))        # resposta duplicada da API
    clima_raw.append(json.dumps(reg))

# ── Fonte 6 · Ocorrências (texto livre) ──
TEXTOS = {
    "mecanica": ["Motor esquentando na subida, parei pra esfriar", "luz do painel acesa e barulho no motor",
                 "freio fazendo barulho estranho", "superaquecimento de novo, temperatura no talo",
                 "pneu furado na BR-116, troquei no acostamento"],
    "clima_transito": ["chuva forte, via alagada, esperei baixar", "transito parado na marginal por acidente",
                       "temporal na serra, reduzi a velocidade", "engarrafamento na entrada do CD"],
    "cobranca": ["cliente reclamou do valor cobrado na nota", "cliente diz que a cobrança veio em duplicidade",
                 "nota fiscal com valor diferente do combinado", "cliente recusou assinar por divergência de valor"],
    "avaria": ["caixa amassada na descarga", "produto molhado, embalagem rasgada", "volume avariado no transporte"],
}
entregas_ok = [l for l in {l[0]: l for l in tms_raw}.values() if l[8] == "Entregue"]
ocorr_raw = []
for oid in range(1, 1_201):
    l = random.choice(entregas_ok)
    v, cli, d = int(l[4]), int(l[2]), (date.fromisoformat(l[6]) - BASE).days
    pesos = {"mecanica": 3 if v in VEICULOS_ATENCAO else 1, "clima_transito": 3 if chuva[(int(l[3]), d)] > 30 else 1,
             "cobranca": 8 if cli in CLIENTES_ATENCAO else 1, "avaria": 1}
    cat = random.choices(list(pesos), list(pesos.values()))[0]
    texto = random.choice(TEXTOS[cat])
    texto = random.choice([texto, texto.upper(), texto.capitalize(), "  " + texto + "  "])
    if random.random() < 0.04:
        texto = random.choice(["", "   ", "ok", "-"])   # registros vazios/inúteis
    ocorr_raw.append((str(oid), l[0], l[4], f"{l[7]}T{random.randint(7, 19):02d}:{random.randint(0, 59):02d}:00", texto))

print(f"IoT: {len(iot_raw):,} · TMS: {len(tms_raw):,} · ERP: {len(erp_raw):,} · WMS: {len(wms_raw):,} · "
      f"Clima: {len(clima_raw):,} · Ocorrências: {len(ocorr_raw):,}")
print(f"Cadastro de clientes — ERP: {len(cli_erp_raw):,} · TMS: {len(cli_tms_raw):,} · CRM: {len(crm_raw):,}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 2 — Camada BRONZE: o recibo da ingestão (pronto)
# MAGIC
# MAGIC Tudo entra **como chegou**, mais dois metadados: *quando* chegou (`_ingestao_ts`) e *de onde*
# MAGIC veio (`_fonte`). JSON e texto entram como texto puro; os extratos estruturados entram com todas
# MAGIC as colunas como texto. Nada é validado aqui — se a Silver errar, reprocessamos a partir da Bronze.

# COMMAND ----------

from pyspark.sql import functions as F


def para_bronze(linhas, colunas, tabela, fonte):
    df = (spark.createDataFrame(linhas, colunas)
          .withColumn("_ingestao_ts", F.current_timestamp())
          .withColumn("_fonte", F.lit(fonte)))
    df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(f"lodlog_bronze.{tabela}")
    print(f"Bronze {tabela:22s} {spark.table(f'lodlog_bronze.{tabela}').count():>7,} linhas  ← {fonte}")


para_bronze([(e,) for e in iot_raw], ["payload_json"], "iot_telemetria_raw", "iot-frota (streaming)")
para_bronze(tms_raw, ["entrega_id", "numero_pedido", "cliente_id", "cd_id", "veiculo_id", "motorista_id",
                      "data_prevista", "data_entrega", "status", "valor_frete", "distancia_km"],
            "tms_entregas_raw", "tms (batch/CDC)")
para_bronze(erp_raw, ["fatura_id", "entrega_id", "cliente_id", "valor_faturado", "data_emissao"],
            "erp_faturas_raw", "erp (batch diário)")
para_bronze(wms_raw, ["cd_id", "sku", "data", "saldo", "demanda_dia", "ponto_reposicao"],
            "wms_estoque_raw", "wms (batch diário)")
para_bronze([(e,) for e in clima_raw], ["payload_json"], "clima_api_raw", "api-inmet (externa)")
para_bronze(ocorr_raw, ["ocorrencia_id", "entrega_id", "veiculo_id", "registrado_em", "texto"],
            "ocorrencias_raw", "app-motorista (texto livre)")
para_bronze(cli_erp_raw, ["cliente_id", "razao_social", "cnpj", "logradouro", "numero", "bairro", "cidade", "uf", "cep"],
            "erp_clientes_raw", "erp (cadastro de clientes)")
para_bronze(cli_tms_raw, ["destinatario_id", "cliente_id", "endereco_entrega", "cep_informado"],
            "tms_destinatarios_raw", "tms (endereço digitado no CD)")
para_bronze(crm_raw, ["conta_id", "nome_fantasia", "cnpj", "cidade", "uf"],
            "crm_contas_raw", "planilha comercial (CRM)")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 3 — Camada SILVER das fontes prontas (pronto)
# MAGIC
# MAGIC Na Silver o dado ganha **tipo, regra e dono**: aplicamos o schema, removemos duplicatas e barramos o
# MAGIC que viola regra de negócio. Cada `WHERE` abaixo é uma **regra de qualidade explícita e auditável** —
# MAGIC é isso que separa um data lake de um pântano de dados.
# MAGIC
# MAGIC **3.1 · IoT (semiestruturado):** o JSON vira colunas; leituras sem veículo ou com velocidade absurda saem.

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS lodlog_silver.iot_telemetria;
# MAGIC CREATE TABLE lodlog_silver.iot_telemetria USING DELTA AS
# MAGIC WITH parseado AS (
# MAGIC   SELECT from_json(payload_json,
# MAGIC     'veiculo_id INT, ts TIMESTAMP, gps STRUCT<lat: DOUBLE, lon: DOUBLE>,
# MAGIC      velocidade_kmh DOUBLE, temperatura_motor_c DOUBLE, nivel_combustivel_pct DOUBLE') AS e
# MAGIC   FROM lodlog_bronze.iot_telemetria_raw
# MAGIC )
# MAGIC SELECT DISTINCT                                   -- remove eventos duplicados
# MAGIC   e.veiculo_id, e.ts AS timestamp_evento, DATE(e.ts) AS data_evento,
# MAGIC   e.gps.lat AS latitude, e.gps.lon AS longitude,
# MAGIC   e.velocidade_kmh, e.temperatura_motor_c, e.nivel_combustivel_pct
# MAGIC FROM parseado
# MAGIC WHERE e.veiculo_id IS NOT NULL
# MAGIC   AND e.velocidade_kmh BETWEEN 0 AND 160;         -- regra: leitura fisicamente plausível

# COMMAND ----------

# MAGIC %md
# MAGIC **3.2 · TMS entregas:** tipos corretos, uma linha por entrega (o extrato reenviado gera duplicata),
# MAGIC frete negativo barrado e duas colunas derivadas que o negócio entende: `atraso_dias` e `no_prazo`.

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS lodlog_silver.tms_entregas;
# MAGIC CREATE TABLE lodlog_silver.tms_entregas USING DELTA AS
# MAGIC SELECT DISTINCT
# MAGIC   CAST(entrega_id AS BIGINT)            AS entrega_id,
# MAGIC   numero_pedido,
# MAGIC   CAST(cliente_id AS INT)               AS cliente_id,
# MAGIC   CAST(cd_id AS INT)                    AS cd_id,
# MAGIC   CAST(veiculo_id AS INT)               AS veiculo_id,
# MAGIC   CAST(motorista_id AS INT)             AS motorista_id,
# MAGIC   CAST(data_prevista AS DATE)           AS data_prevista,
# MAGIC   CAST(NULLIF(data_entrega, '') AS DATE) AS data_entrega,
# MAGIC   status,
# MAGIC   CAST(valor_frete AS DECIMAL(12,2))    AS valor_frete,
# MAGIC   CAST(distancia_km AS DOUBLE)          AS distancia_km,
# MAGIC   DATEDIFF(CAST(NULLIF(data_entrega, '') AS DATE), CAST(data_prevista AS DATE)) AS atraso_dias,
# MAGIC   DATEDIFF(CAST(NULLIF(data_entrega, '') AS DATE), CAST(data_prevista AS DATE)) <= 0 AS no_prazo
# MAGIC FROM lodlog_bronze.tms_entregas_raw
# MAGIC WHERE CAST(valor_frete AS DECIMAL(12,2)) > 0;      -- regra: frete precisa ser positivo

# COMMAND ----------

# MAGIC %md
# MAGIC **3.3 · ERP faturas:** tipos corretos e uma marca de **integridade referencial** — a fatura aponta
# MAGIC para uma entrega que existe? (No Unity Catalog, chave estrangeira é só informativa: quem garante é
# MAGIC a regra da Silver.) Não apagamos a órfã: marcamos, porque ela é evidência para auditoria.

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS lodlog_silver.erp_faturas;
# MAGIC CREATE TABLE lodlog_silver.erp_faturas USING DELTA AS
# MAGIC SELECT
# MAGIC   CAST(f.fatura_id AS BIGINT)            AS fatura_id,
# MAGIC   CAST(f.entrega_id AS BIGINT)           AS entrega_id,
# MAGIC   CAST(f.cliente_id AS INT)              AS cliente_id,
# MAGIC   CAST(f.valor_faturado AS DECIMAL(12,2)) AS valor_faturado,
# MAGIC   CAST(f.data_emissao AS DATE)           AS data_emissao,
# MAGIC   e.entrega_id IS NOT NULL               AS tem_entrega   -- FALSE = fatura órfã
# MAGIC FROM lodlog_bronze.erp_faturas_raw f
# MAGIC LEFT JOIN (SELECT DISTINCT CAST(entrega_id AS BIGINT) AS entrega_id
# MAGIC            FROM lodlog_bronze.tms_entregas_raw) e
# MAGIC   ON CAST(f.entrega_id AS BIGINT) = e.entrega_id;

# COMMAND ----------

# MAGIC %md
# MAGIC **3.4 · WMS estoque:** saldo negativo é erro de inventário e sai; `ruptura` vira uma coluna explícita.

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS lodlog_silver.wms_estoque;
# MAGIC CREATE TABLE lodlog_silver.wms_estoque USING DELTA AS
# MAGIC SELECT
# MAGIC   CAST(cd_id AS INT)            AS cd_id,
# MAGIC   sku,
# MAGIC   CAST(data AS DATE)            AS data,
# MAGIC   CAST(saldo AS INT)            AS saldo,
# MAGIC   CAST(demanda_dia AS INT)      AS demanda_dia,
# MAGIC   CAST(ponto_reposicao AS INT)  AS ponto_reposicao,
# MAGIC   CAST(saldo AS INT) = 0        AS ruptura
# MAGIC FROM lodlog_bronze.wms_estoque_raw
# MAGIC WHERE CAST(saldo AS INT) >= 0;          -- regra: saldo negativo é erro de inventário

# COMMAND ----------

for t in ["iot_telemetria", "tms_entregas", "erp_faturas", "wms_estoque"]:
    nb = spark.table(f"lodlog_bronze.{t}_raw").count()
    ns = spark.table(f"lodlog_silver.{t}").count()
    print(f"{t:16s} Bronze → Silver: {nb:>7,} → {ns:>7,}  ({nb - ns:,} barradas pela qualidade)")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 4 — 🟨 TODO 1 · Levar uma fonte semi/não estruturada até a Silver
# MAGIC
# MAGIC Duas fontes ficaram só na Bronze. O grupo leva **uma delas** (a recomendada para o seu cenário)
# MAGIC até a Silver. O código está pronto; **as regras são decisão de vocês**:
# MAGIC
# MAGIC - **`clima`** (JSON da API do INMET) — que valor de chuva diária é plausível? A API às vezes
# MAGIC   devolve `9999` como código de erro. Acima de qual limite vocês descartam a leitura?
# MAGIC - **`ocorrencias`** (texto livre) — o motorista escreve como quer. Para virar dado analisável,
# MAGIC   cada texto recebe uma **categoria** pelas palavras-chave que vocês definem. Olhem a amostra
# MAGIC   abaixo e completem as listas. Quanto menos texto cair em `outros`, melhor a regra.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Amostra para inspirar as regras (pronto)
# MAGIC SELECT texto, COUNT(*) AS vezes FROM lodlog_bronze.ocorrencias_raw GROUP BY texto ORDER BY vezes DESC LIMIT 25;

# COMMAND ----------

# 🟨 TODO 1a — qual fonte o grupo leva para a Silver? "clima" ou "ocorrencias"
FONTE_EXTRA = None

# 🟨 TODO 1b (se escolheram "clima") — maior chuva diária plausível, em mm.
#    Dica: o recorde brasileiro em 24h fica na casa dos 300 mm.
CHUVA_MAX_MM = None

# 🟨 TODO 1b (se escolheram "ocorrencias") — completem as palavras-chave de cada categoria.
#    Use pedaços de palavra em minúsculas e sem acento quando possível ("cobr" pega cobrança e cobrado).
CATEGORIAS = {
    "mecanica":       ["motor", "freio"],    # completem: o que mais indica problema mecânico?
    "clima_transito": [],                    # completem
    "cobranca":       [],                    # completem
    "avaria":         ["amassad"],           # completem
}

# COMMAND ----------

# Construção da Silver da fonte extra (pronto — usa as decisões acima)
FONTES_EXTRAS = [FONTE_EXTRA] if isinstance(FONTE_EXTRA, str) else list(FONTE_EXTRA or [])

if not FONTES_EXTRAS:
    print("⏸  TODO 1 pendente: defina FONTE_EXTRA na célula acima.")

if "clima" in FONTES_EXTRAS:
    if CHUVA_MAX_MM is None:
        print("⏸  TODO 1b pendente: defina CHUVA_MAX_MM.")
    else:
        spark.sql("DROP TABLE IF EXISTS lodlog_silver.clima_diario")
        spark.sql(f"""
            CREATE TABLE lodlog_silver.clima_diario USING DELTA AS
            WITH p AS (
              SELECT from_json(payload_json,
                'estacao STRING, cd_id INT, data DATE,
                 medicoes STRUCT<chuva_mm: DOUBLE, temp_max_c: DOUBLE>, alerta STRING') AS c
              FROM lodlog_bronze.clima_api_raw)
            SELECT DISTINCT c.cd_id, c.data, c.estacao,
                   c.medicoes.chuva_mm AS chuva_mm, c.medicoes.temp_max_c AS temp_max_c,
                   COALESCE(c.alerta, 'sem alerta') AS alerta
            FROM p
            WHERE c.medicoes.chuva_mm IS NOT NULL
              AND c.medicoes.chuva_mm BETWEEN 0 AND {float(CHUVA_MAX_MM)}""")
        nb = spark.table("lodlog_bronze.clima_api_raw").count()
        ns = spark.table("lodlog_silver.clima_diario").count()
        print(f"clima Bronze → Silver: {nb:,} → {ns:,}  ({nb - ns:,} barradas: duplicatas, ausentes e códigos de erro)")

if "ocorrencias" in FONTES_EXTRAS:
    def _regra(cat, palavras):
        cond = " OR ".join(f"t LIKE '%{p.lower().replace(chr(39), '')}%'" for p in palavras if p.strip())
        return f"WHEN {cond} THEN '{cat}'" if cond else ""
    casos = "\n".join(_regra(c, ps) for c, ps in CATEGORIAS.items())
    spark.sql("DROP TABLE IF EXISTS lodlog_silver.ocorrencias")
    spark.sql(f"""
        CREATE TABLE lodlog_silver.ocorrencias USING DELTA AS
        WITH limpo AS (
          SELECT CAST(ocorrencia_id AS BIGINT) AS ocorrencia_id,
                 CAST(entrega_id AS BIGINT)    AS entrega_id,
                 CAST(veiculo_id AS INT)       AS veiculo_id,
                 CAST(registrado_em AS TIMESTAMP) AS registrado_em,
                 TRIM(texto) AS texto,
                 translate(lower(TRIM(texto)), 'áàâãéêíóôõúç', 'aaaaeeiooouc') AS t
          FROM lodlog_bronze.ocorrencias_raw)
        SELECT ocorrencia_id, entrega_id, veiculo_id, registrado_em, texto,
               CASE {casos} ELSE 'outros' END AS categoria
        FROM limpo
        WHERE LENGTH(t) >= 5                -- regra: descarta registros vazios ou inúteis
        """)
    dist = spark.sql("SELECT categoria, COUNT(*) n FROM lodlog_silver.ocorrencias GROUP BY categoria ORDER BY n DESC")
    display(dist)
    total = spark.table("lodlog_silver.ocorrencias").count()
    outros = spark.sql("SELECT COUNT(*) FROM lodlog_silver.ocorrencias WHERE categoria = 'outros'").first()[0]
    print(f"ocorrências classificadas: {total:,} · em 'outros': {outros:,} ({100 * outros / total:.0f}%)"
          + ("  ← acima de 10%: revisem as palavras-chave" if outros / total > 0.10 else "  ✅"))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 5 — Camada GOLD
# MAGIC
# MAGIC ### 5.1 · Gold de referência (pronto)
# MAGIC Um exemplo completo: resumo diário da frota, a partir da telemetria. Notem o padrão que a Gold
# MAGIC do grupo vai seguir — **chaves de negócio + contagens + uma métrica que alguém usa para decidir.**

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS lodlog_gold.resumo_diario_frota;
# MAGIC CREATE TABLE lodlog_gold.resumo_diario_frota USING DELTA AS
# MAGIC SELECT data_evento, veiculo_id,
# MAGIC        COUNT(*)                               AS leituras,
# MAGIC        ROUND(AVG(velocidade_kmh), 1)          AS velocidade_media,
# MAGIC        ROUND(MAX(temperatura_motor_c), 1)     AS temperatura_max_motor,
# MAGIC        ROUND(MIN(nivel_combustivel_pct), 1)   AS menor_nivel_combustivel
# MAGIC FROM lodlog_silver.iot_telemetria
# MAGIC GROUP BY data_evento, veiculo_id;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 5.2 · 🟨 TODO 2 · A Gold do cenário do grupo
# MAGIC
# MAGIC Cada cenário tem um **modelo de Gold quase pronto**: junta uma fonte estruturada com a fonte extra
# MAGIC do TODO 1 e já calcula as contagens. Falta **uma linha — a métrica-chave**, o número que vai
# MAGIC para o pitch. Encontrem o seu cenário abaixo e troquem `CAST(NULL AS DOUBLE)` pela fórmula
# MAGIC (a dica está no comentário). Mexam nos outros cenários só se quiserem.

# COMMAND ----------

GOLD = {
    "A": ("lodlog_gold.cenario_a_pontualidade", """
        SELECT e.cd_id, e.data_prevista AS data,
               COUNT(*)                                          AS entregas,
               SUM(CASE WHEN e.no_prazo THEN 1 ELSE 0 END)       AS entregas_no_prazo,
               ROUND(AVG(e.atraso_dias), 2)                      AS atraso_medio_dias,
               MAX(c.chuva_mm)                                   AS chuva_mm,
               CAST(NULL AS DOUBLE) AS metrica_chave   -- 🟨 TODO 2: % de entregas no prazo.
                                                       --    Dica: ROUND(100.0 * <no prazo> / <entregas>, 1)
        FROM lodlog_silver.tms_entregas e
        LEFT JOIN lodlog_silver.clima_diario c ON c.cd_id = e.cd_id AND c.data = e.data_prevista
        WHERE e.status = 'Entregue'
        GROUP BY e.cd_id, e.data_prevista"""),
    "B": ("lodlog_gold.cenario_b_saude_frota", """
        WITH iot AS (
          SELECT veiculo_id,
                 COUNT(*)                                                    AS leituras,
                 ROUND(AVG(temperatura_motor_c), 1)                          AS temp_media_motor,
                 SUM(CASE WHEN temperatura_motor_c > 105 THEN 1 ELSE 0 END)  AS leituras_superaquecimento
          FROM lodlog_silver.iot_telemetria GROUP BY veiculo_id),
        oc AS (
          SELECT veiculo_id, COUNT(*) AS ocorrencias_mecanicas
          FROM lodlog_silver.ocorrencias WHERE categoria = 'mecanica' GROUP BY veiculo_id)
        SELECT i.veiculo_id, i.leituras, i.temp_media_motor, i.leituras_superaquecimento,
               COALESCE(o.ocorrencias_mecanicas, 0) AS ocorrencias_mecanicas,
               CAST(NULL AS DOUBLE) AS metrica_chave   -- 🟨 TODO 2: % das leituras em superaquecimento.
                                                       --    Dica: ROUND(100.0 * <superaquecimento> / <leituras>, 1)
        FROM iot i LEFT JOIN oc o ON o.veiculo_id = i.veiculo_id"""),
    "C": ("lodlog_gold.cenario_c_ruptura", """
        SELECT w.cd_id, w.sku,
               COUNT(*)                                                         AS dias_observados,
               SUM(CASE WHEN w.ruptura THEN 1 ELSE 0 END)                       AS dias_em_ruptura,
               SUM(CASE WHEN w.ruptura AND c.chuva_mm > 30 THEN 1 ELSE 0 END)   AS rupturas_com_chuva_forte,
               CAST(NULL AS DOUBLE) AS metrica_chave   -- 🟨 TODO 2: taxa de ruptura (%).
                                                       --    Dica: ROUND(100.0 * <dias em ruptura> / <dias observados>, 1)
        FROM lodlog_silver.wms_estoque w
        LEFT JOIN lodlog_silver.clima_diario c ON c.cd_id = w.cd_id AND c.data = w.data
        GROUP BY w.cd_id, w.sku"""),
    "D": ("lodlog_gold.cenario_d_divergencia", """
        WITH fat AS (
          SELECT e.cliente_id, e.entrega_id, e.valor_frete, f.valor_faturado
          FROM lodlog_silver.tms_entregas e
          JOIN lodlog_silver.erp_faturas f ON f.entrega_id = e.entrega_id),
        oc AS (
          SELECT e.cliente_id, COUNT(*) AS reclamacoes_cobranca
          FROM lodlog_silver.ocorrencias o
          JOIN lodlog_silver.tms_entregas e ON e.entrega_id = o.entrega_id
          WHERE o.categoria = 'cobranca' GROUP BY e.cliente_id)
        SELECT fat.cliente_id,
               COUNT(*)                                                                      AS faturas,
               SUM(CASE WHEN ABS(fat.valor_faturado - fat.valor_frete) > 0.01 THEN 1 ELSE 0 END) AS faturas_divergentes,
               ROUND(SUM(fat.valor_faturado - fat.valor_frete), 2)                           AS diferenca_total_rs,
               COALESCE(MAX(oc.reclamacoes_cobranca), 0)                                     AS reclamacoes_cobranca,
               CAST(NULL AS DOUBLE) AS metrica_chave   -- 🟨 TODO 2: % de faturas divergentes.
                                                       --    Dica: ROUND(100.0 * <divergentes> / <faturas>, 1)
        FROM fat LEFT JOIN oc ON oc.cliente_id = fat.cliente_id
        GROUP BY fat.cliente_id"""),
}
FONTE_DO_CENARIO = {"A": "clima", "B": "ocorrencias", "C": "clima", "D": "ocorrencias"}

# COMMAND ----------

# Construção da Gold do grupo (pronto)
CENARIOS = [CENARIO] if isinstance(CENARIO, str) else list(CENARIO or [])
if not CENARIOS:
    print("⏸  Escolha o CENARIO no início do notebook.")
for cen in CENARIOS:
    tabela, sql = GOLD[cen]
    precisa = FONTE_DO_CENARIO[cen]
    if precisa not in FONTES_EXTRAS:
        print(f"⏸  Cenário {cen} usa a Silver de '{precisa}': conclua o TODO 1 com essa fonte.")
        continue
    spark.sql(f"DROP TABLE IF EXISTS {tabela}")
    spark.sql(f"CREATE TABLE {tabela} USING DELTA AS {sql}")
    preenchida = spark.sql(f"SELECT COUNT(metrica_chave) FROM {tabela}").first()[0]
    print(f"Gold {tabela}: {spark.table(tabela).count():,} linhas · métrica-chave "
          + ("✅ preenchida" if preenchida else "⏸  ainda NULL — falta o TODO 2"))
    display(spark.table(tabela).limit(10))

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 6 — Análise sobre a Gold
# MAGIC
# MAGIC ### 6.1 · Exemplo pronto
# MAGIC *Pergunta: quantos veículos por dia chegam à reserva de combustível (abaixo de 10%) — risco de
# MAGIC parada em rota?* Repare no formato: **pergunta → consulta → frase para a diretoria.**

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT data_evento,
# MAGIC        COUNT(*)                                                   AS veiculos_ativos,
# MAGIC        SUM(CASE WHEN menor_nivel_combustivel < 10 THEN 1 ELSE 0 END) AS veiculos_na_reserva
# MAGIC FROM lodlog_gold.resumo_diario_frota
# MAGIC GROUP BY data_evento
# MAGIC ORDER BY veiculos_na_reserva DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %md
# MAGIC > **Frase para a diretoria (exemplo):** *"Nos piores dias, um em cada quatro veículos ativos chega
# MAGIC > à reserva; uma regra de abastecimento antes da saída custa menos que um caminhão parado em rota."*
# MAGIC
# MAGIC ### 6.2 · 🟨 TODO 3 · A análise do grupo
# MAGIC A consulta do seu cenário **já vem pronta** e roda sozinha. O trabalho do grupo é de líder de dados:
# MAGIC 1. Escrever a **pergunta de negócio** que a Gold responde.
# MAGIC 2. Escrever a **interpretação**: o que vocês diriam ao diretor com esse número? Que decisão ela apoia?

# COMMAND ----------

# 🟨 TODO 3a — a pergunta de negócio do grupo (uma frase)
PERGUNTA_NEGOCIO = ""

ANALISE = {
    "A": """SELECT cd_id, SUM(entregas) AS entregas,
                   ROUND(AVG(CASE WHEN chuva_mm > 30 THEN metrica_chave END), 1) AS pct_no_prazo_dia_chuvoso,
                   ROUND(AVG(CASE WHEN chuva_mm <= 30 THEN metrica_chave END), 1) AS pct_no_prazo_dia_seco
            FROM lodlog_gold.cenario_a_pontualidade GROUP BY cd_id ORDER BY cd_id""",
    "B": """SELECT veiculo_id, metrica_chave AS pct_leituras_superaquecimento, ocorrencias_mecanicas, temp_media_motor
            FROM lodlog_gold.cenario_b_saude_frota ORDER BY metrica_chave DESC LIMIT 10""",
    "C": """SELECT cd_id, ROUND(AVG(metrica_chave), 1) AS taxa_ruptura_pct,
                   SUM(dias_em_ruptura) AS dias_em_ruptura, SUM(rupturas_com_chuva_forte) AS com_chuva_forte
            FROM lodlog_gold.cenario_c_ruptura GROUP BY cd_id ORDER BY taxa_ruptura_pct DESC""",
    "D": """SELECT cliente_id, faturas, metrica_chave AS pct_divergentes, diferenca_total_rs, reclamacoes_cobranca
            FROM lodlog_gold.cenario_d_divergencia ORDER BY metrica_chave DESC LIMIT 10""",
}
for cen in CENARIOS:
    try:
        display(spark.sql(ANALISE[cen]))
    except Exception as e:
        print(f"⏸  Cenário {cen}: a Gold ainda não existe ({str(e).splitlines()[0][:80]})")

# COMMAND ----------

# 🟨 TODO 3b — depois de ver o resultado: o que vocês diriam à diretoria? Que decisão isso apoia?
INTERPRETACAO = ""

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 7 — Governança, glossário e catálogo
# MAGIC
# MAGIC ### 7.1 · Exemplo pronto na Gold de referência
# MAGIC Os 4 pilares da Aula 4 viram **metadados na própria tabela**: quem é o dono, o que ela contém,
# MAGIC se tem dado pessoal (LGPD) e por quanto tempo guardar. Qualquer pessoa que achar a tabela no
# MAGIC catálogo encontra essas respostas — é o antídoto contra o "de onde veio esse número?".

# COMMAND ----------

def aplicar_governanca(tabela, g):
    descricao = g["descricao"].replace("'", "")
    spark.sql(f"COMMENT ON TABLE {tabela} IS '{descricao}'")
    spark.sql(f"""ALTER TABLE {tabela} SET TBLPROPERTIES (
        'lodlog.dono' = '{g["dono"]}',
        'lodlog.contem_dados_pessoais' = '{str(g["contem_dados_pessoais"]).lower()}',
        'lodlog.retencao_dias' = '{g["retencao_dias"]}',
        'lodlog.regra_qualidade' = '{g["regra_qualidade"]}')""")
    props = {r["key"]: r["value"] for r in spark.sql(f"SHOW TBLPROPERTIES {tabela}").collect()
             if r["key"].startswith("lodlog.")}
    print(f"Governança aplicada em {tabela}: {props}")


aplicar_governanca("lodlog_gold.resumo_diario_frota", {
    "dono": "Gerência de Manutenção de Frota",
    "descricao": "Resumo diário por veículo a partir da telemetria IoT (Silver iot_telemetria).",
    "contem_dados_pessoais": False,
    "retencao_dias": 730,
    "regra_qualidade": "leituras_positivas",
})

# COMMAND ----------

# MAGIC %md
# MAGIC **Glossário de negócio e catálogo (pronto).** Metadado técnico diz *onde* está o dado; o **glossário** diz
# MAGIC *o que ele significa* e *quem responde por ele* (DMBOK caps. 3 e 12). Cada termo tem definição, regra,
# MAGIC **dono** (a área que decide) e **steward** (quem cuida do dia a dia), e a definição vai para o comentário
# MAGIC da coluna no catálogo — quem achar a coluna no Catalog Explorer lê o significado ali. As **tags** permitem
# MAGIC buscar, por exemplo, todo dado crítico da empresa.

# COMMAND ----------

spark.sql("""CREATE TABLE IF NOT EXISTS lodlog_gold.glossario_negocio (
    termo STRING, definicao STRING, dono STRING, steward STRING,
    regra_ou_calculo STRING, tabela STRING, coluna STRING, origem STRING) USING DELTA""")


def registrar_termos(termos, origem):
    """Grava os termos no glossário (substitui os da mesma origem) e leva a definição para o catálogo."""
    spark.sql(f"DELETE FROM lodlog_gold.glossario_negocio WHERE origem = '{origem}'")
    linhas = [(t["termo"], t["definicao"], t["dono"], t["steward"], t["regra"], t.get("tabela", ""),
               t.get("coluna", ""), origem) for t in termos]
    (spark.createDataFrame(linhas, "termo STRING, definicao STRING, dono STRING, steward STRING, "
                                   "regra_ou_calculo STRING, tabela STRING, coluna STRING, origem STRING")
     .write.format("delta").mode("append").saveAsTable("lodlog_gold.glossario_negocio"))
    for t in termos:
        if t.get("tabela") and t.get("coluna") and spark.catalog.tableExists(t["tabela"]):
            texto = f'{t["termo"]}: {t["definicao"]} Dono: {t["dono"]}.'.replace("'", "")
            spark.sql(f"ALTER TABLE {t['tabela']} ALTER COLUMN {t['coluna']} COMMENT '{texto}'")
    print(f"Glossário: {len(termos)} termo(s) de origem '{origem}' registrado(s).")


def marcar_no_catalogo(tabela, tags):
    """Tags do Unity Catalog (busca por domínio, criticidade, camada...)."""
    pares = ", ".join(f"'{k}' = '{v}'" for k, v in tags.items())
    try:
        spark.sql(f"ALTER TABLE {tabela} SET TAGS ({pares})")
        print(f"Tags em {tabela}: {tags}")
    except Exception as e:
        print(f"(tags indisponíveis fora do Unity Catalog: {str(e).splitlines()[0][:60]})")


registrar_termos([
    {"termo": "Leitura de telemetria válida", "dono": "Gerência de Manutenção de Frota",
     "steward": "Analista de dados da frota",
     "definicao": "Evento IoT com veículo identificado e velocidade entre 0 e 160 km/h.",
     "regra": "veiculo_id IS NOT NULL AND velocidade_kmh BETWEEN 0 AND 160",
     "tabela": "lodlog_silver.iot_telemetria", "coluna": "velocidade_kmh"},
    {"termo": "Temperatura máxima do motor no dia", "dono": "Gerência de Manutenção de Frota",
     "steward": "Analista de dados da frota",
     "definicao": "Maior temperatura do motor registrada pelo veículo no dia, em graus Celsius.",
     "regra": "MAX(temperatura_motor_c) por veículo e dia",
     "tabela": "lodlog_gold.resumo_diario_frota", "coluna": "temperatura_max_motor"},
], origem="exemplo")
marcar_no_catalogo("lodlog_gold.resumo_diario_frota", {"dominio": "frota", "dado_critico": "nao", "camada": "gold"})
display(spark.table("lodlog_gold.glossario_negocio"))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 7.2 · 🟨 TODO 4 · Governança e glossário da Gold do grupo
# MAGIC **4a.** Preencham o dicionário de governança. **4b.** Definam os **dois termos de negócio** mais importantes
# MAGIC da Gold — o primeiro é a métrica-chave (por exemplo, "Entrega no prazo": o que conta, o que não conta, quem
# MAGIC decide). Na Aula 4 vimos que a mesma palavra dá números diferentes em cada área: o glossário é onde a
# MAGIC LODLog decide **um** significado oficial. Para a regra de qualidade, escolham uma das regras prontas:
# MAGIC
# MAGIC | Regra | O que verifica |
# MAGIC |---|---|
# MAGIC | `metrica_entre_0_e_100` | A métrica-chave é um percentual válido |
# MAGIC | `metrica_sem_nulos` | Nenhuma linha da Gold ficou sem métrica |
# MAGIC | `chave_unica` | Não há linha duplicada para a mesma chave de negócio |

# COMMAND ----------

# 🟨 TODO 4 — governança da Gold do grupo
GOVERNANCA_GRUPO = {
    "dono": "",                       # área de negócio responsável (não uma pessoa)
    "descricao": "",                  # uma frase: o que a tabela contém e de quais Silvers vem
    "contem_dados_pessoais": None,    # True / False — pensem em cliente_id e motorista_id
    "retencao_dias": None,            # por quanto tempo guardar? (número de dias)
    "regra_qualidade": "",            # uma das três regras da tabela acima
}

# 🟨 TODO 4b — glossário: os dois termos de negócio mais importantes da Gold do grupo.
#    dono = área que decide sobre o termo · steward = quem cuida do dado no dia a dia · regra = como se calcula
GLOSSARIO_GRUPO = [
    {"termo": "", "definicao": "", "dono": "", "steward": "", "regra": "", "coluna": "metrica_chave"},
    {"termo": "", "definicao": "", "dono": "", "steward": "", "regra": "", "coluna": ""},
]

# COMMAND ----------

# Aplicação e checagem da governança (pronto)
CHAVES = {"A": "cd_id, data", "B": "veiculo_id", "C": "cd_id, sku", "D": "cliente_id"}
REGRAS = {
    "metrica_entre_0_e_100": "SELECT COUNT(*) FROM {t} WHERE metrica_chave < 0 OR metrica_chave > 100",
    "metrica_sem_nulos":     "SELECT COUNT(*) FROM {t} WHERE metrica_chave IS NULL",
    "chave_unica":           "SELECT COUNT(*) FROM (SELECT {k} FROM {t} GROUP BY {k} HAVING COUNT(*) > 1)",
}
g = GOVERNANCA_GRUPO
governanca_ok = bool(g["dono"] and g["descricao"] and g["contem_dados_pessoais"] is not None
                     and g["retencao_dias"] and g["regra_qualidade"] in REGRAS)
for cen in CENARIOS:
    tabela = GOLD[cen][0]
    if not spark.catalog.tableExists(tabela):
        print(f"⏸  {tabela} ainda não existe.")
    elif not governanca_ok:
        print("⏸  TODO 4 pendente: preencham todos os campos de GOVERNANCA_GRUPO.")
    else:
        aplicar_governanca(tabela, g)
        violacoes = spark.sql(REGRAS[g["regra_qualidade"]].format(t=tabela, k=CHAVES[cen])).first()[0]
        print(f"Regra '{g['regra_qualidade']}': {violacoes} violação(ões) " + ("✅" if violacoes == 0 else "⚠️ investiguem"))
        marcar_no_catalogo(tabela, {"cenario": cen, "camada": "gold"})
    glossario_ok = all(all(str(t.get(k, "")).strip() for k in ("termo", "definicao", "dono", "steward", "regra"))
                       for t in GLOSSARIO_GRUPO)
    if spark.catalog.tableExists(tabela) and glossario_ok:
        registrar_termos([dict(t, tabela=tabela if t.get("coluna") else "") for t in GLOSSARIO_GRUPO], origem="grupo")
    elif spark.catalog.tableExists(tabela):
        print("⏸  TODO 4b pendente: preencham termo, definição, dono, steward e regra dos dois termos do glossário.")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 7B — O dado mais crítico da LODLog: cliente e endereço (MDM)
# MAGIC
# MAGIC **Por que este dado.** Todo cenário passa pelo cliente: é para ele que a entrega vai (A) e é ele que
# MAGIC recebe a fatura (D). E o **endereço de entrega** decide se o motorista acerta na primeira tentativa.
# MAGIC Na LODLog, o mesmo cliente está cadastrado em **três sistemas**, cada um do seu jeito:
# MAGIC
# MAGIC | Sistema | Quem cadastra | Como o cliente aparece | Problema típico |
# MAGIC |---|---|---|---|
# MAGIC | **ERP** (faturamento) | Comercial | razão social, CNPJ e endereço em campos separados | a mesma empresa cadastrada duas vezes, com códigos diferentes |
# MAGIC | **TMS** (entregas) | Operador do CD | endereço de entrega em **texto livre** | abreviações, cidade escrita de vários jeitos, sem número, CEP de outra cidade |
# MAGIC | **CRM** (planilha comercial) | Vendedor | nome fantasia, às vezes sem CNPJ | nome abreviado, palavras trocadas de lugar, erro de digitação |
# MAGIC
# MAGIC Gerenciar esse **dado mestre** (MDM, DMBOK cap. 10) tem quatro passos, e esta etapa percorre os quatro:
# MAGIC 1. **Padronizar** (7B.1 e 7B.2) — regras SQL onde a regra resolve e **IA** (`ai_query` com o modelo
# MAGIC    `system.ai.llama-4-maverick`) onde o texto é livre demais para regra.
# MAGIC 2. **Casar** (7B.3) — descobrir quais registros dos três sistemas são a mesma empresa (a tabela de-para).
# MAGIC 3. **Medir** (7B.4) — o scorecard de qualidade do dado crítico, com as dimensões do DMBOK.
# MAGIC 4. **Decidir o registro de ouro** (7B.5 · 🟨 **TODO 5**) — de onde vem o endereço oficial e o que é um
# MAGIC    "endereço válido para entrega". **Essa decisão é de negócio, não de TI** — por isso é do grupo.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Antes de tudo, olhem o problema: a mesma empresa (cliente 197) nos três sistemas (pronto)
# MAGIC WITH alvo AS (SELECT regexp_replace(cnpj, '[^0-9]', '') AS cnpj FROM lodlog_bronze.erp_clientes_raw WHERE cliente_id = '197')
# MAGIC SELECT 'ERP' AS sistema, CONCAT('código ', cliente_id) AS codigo, razao_social AS nome, cnpj,
# MAGIC        CONCAT_WS(', ', logradouro, numero, bairro, cidade) AS endereco, cep
# MAGIC FROM lodlog_bronze.erp_clientes_raw WHERE regexp_replace(cnpj, '[^0-9]', '') IN (SELECT cnpj FROM alvo)
# MAGIC UNION ALL
# MAGIC SELECT 'TMS', CONCAT('código ', cliente_id), NULL, NULL, endereco_entrega, cep_informado
# MAGIC FROM lodlog_bronze.tms_destinatarios_raw WHERE cliente_id = '197'
# MAGIC UNION ALL
# MAGIC SELECT 'CRM', conta_id, nome_fantasia, cnpj, cidade, NULL
# MAGIC FROM lodlog_bronze.crm_contas_raw WHERE regexp_replace(cnpj, '[^0-9]', '') IN (SELECT cnpj FROM alvo)
# MAGIC ORDER BY sistema;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 7B.1 · Padronização por regras (pronto)
# MAGIC Duas **tabelas de referência** (DMBOK cap. 10: dado que serve para classificar e checar outros dados) e
# MAGIC uma regra de nome. A chave de comparação do nome tira acento, pontuação e sufixo societário (Ltda, S.A., ME),
# MAGIC troca abreviações conhecidas pela palavra inteira e põe as palavras em ordem alfabética — assim
# MAGIC "Bom Preço Supermercado" e "Superm. Bom Preço Ltda" viram a mesma chave.

# COMMAND ----------

spark.sql("DROP TABLE IF EXISTS lodlog_silver.ref_faixa_cep")
spark.createDataFrame([                     # faixas simplificadas das cinco cidades atendidas
    ("SAO PAULO", "SP", "01000000", "05999999"), ("CAMPINAS", "SP", "13000000", "13139999"),
    ("RIO DE JANEIRO", "RJ", "20000000", "23799999"), ("BELO HORIZONTE", "MG", "30000000", "31999999"),
    ("CURITIBA", "PR", "80000000", "82999999")], "cidade STRING, uf STRING, cep_inicio STRING, cep_fim STRING") \
    .write.format("delta").saveAsTable("lodlog_silver.ref_faixa_cep")

ABREVIACOES = {"SUPERM": "SUPERMERCADO", "SUPERMERC": "SUPERMERCADO", "DIST": "DISTRIBUIDORA",
               "DISTRIB": "DISTRIBUIDORA", "FARM": "FARMACIA", "ATAC": "ATACADO", "COM": "COMERCIAL",
               "MERC": "MERCADO", "DROG": "DROGARIA", "ARMZ": "ARMAZEM", "CS": "CASA"}
SEM_ACENTO = "translate(upper(trim({c})), 'ÁÀÂÃÉÊÍÓÔÕÚÇ', 'AAAAEEIOOOUC')"


def chave_nome(col):
    """Nome → chave de comparação (só regra, sem IA)."""
    e = f"regexp_replace({SEM_ACENTO.format(c=col)}, '[^A-Z0-9 ]', ' ')"
    e = f"regexp_replace({e}, '\\\\b(LTDA|S A|SA|ME|EIRELI)\\\\b', ' ')"
    for abrev, palavra in ABREVIACOES.items():
        e = f"regexp_replace({e}, '\\\\b{abrev}\\\\b', '{palavra}')"
    return f"array_join(array_sort(filter(split(trim({e}), ' +'), w -> w <> '')), ' ')"


def cidade_padrao(col):
    """Variações de escrita da cidade → nome oficial, sem acento."""
    u = SEM_ACENTO.format(c=col)
    return f"""CASE WHEN {u} RLIKE 'PAULO|SAMPA' THEN 'SAO PAULO'
                    WHEN {u} RLIKE 'CAMPINAS|^CPS$' THEN 'CAMPINAS'
                    WHEN {u} RLIKE '^RIO' THEN 'RIO DE JANEIRO'
                    WHEN {u} RLIKE 'HORIZONTE|^BH$' THEN 'BELO HORIZONTE'
                    WHEN {u} RLIKE 'CURITIBA|^CTBA$' THEN 'CURITIBA' END"""


spark.sql("DROP TABLE IF EXISTS lodlog_silver.cliente_candidatos")
spark.sql(f"""
CREATE TABLE lodlog_silver.cliente_candidatos USING DELTA AS
WITH origem AS (
  SELECT 'ERP' AS sistema, cliente_id AS chave_origem, CAST(cliente_id AS INT) AS cliente_id,
         razao_social AS nome, cnpj, logradouro, numero, bairro, cidade, cep
  FROM lodlog_bronze.erp_clientes_raw
  UNION ALL
  SELECT 'CRM', conta_id, NULL, nome_fantasia, cnpj, NULL, NULL, NULL, cidade, NULL
  FROM lodlog_bronze.crm_contas_raw)
SELECT sistema, chave_origem, cliente_id, nome,
       {chave_nome('nome')}                          AS chave_nome,
       NULLIF(regexp_replace(cnpj, '[^0-9]', ''), '') AS cnpj,
       logradouro, numero, bairro,
       {cidade_padrao('cidade')}                     AS cidade,
       NULLIF(regexp_replace(cep, '[^0-9]', ''), '') AS cep
FROM origem""")
display(spark.sql("""SELECT sistema, nome, chave_nome, cnpj, cidade FROM lodlog_silver.cliente_candidatos
                     WHERE chave_nome LIKE '%BOM PRECO%' OR chave_nome LIKE '%SAO JORGE%' ORDER BY chave_nome, sistema"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 7B.2 · Padronização com IA (pronto) — só onde a regra não dá conta
# MAGIC Duas situações em que regra não basta:
# MAGIC - o **endereço do TMS** é texto livre ("R. das Flores nº 123, Centro, BH MG");
# MAGIC - o **nome do CRM sem CNPJ** pode ter erro de digitação ou iniciais ("Supermecado S. Jorge") — sem CNPJ,
# MAGIC   o nome é a única pista para achar o cliente.
# MAGIC
# MAGIC Para esses casos chamamos um modelo de linguagem **direto do SQL**, com `ai_query`, pedindo a resposta num
# MAGIC **formato JSON fixo** (`responseFormat`) — assim a saída da IA vira colunas, não texto solto. Três cuidados de
# MAGIC arquitetura que valem para qualquer uso de IA em dados:
# MAGIC 1. **Custo:** a IA só recebe o que a regra não resolve (endereços distintos e nomes sem CNPJ), não as 6 mil entregas.
# MAGIC 2. **Cache:** o resultado fica numa tabela; um novo Run All **não paga de novo**.
# MAGIC 3. **Rastreabilidade e plano B:** cada linha registra se veio da `ia` ou da `regra`. Se a IA falhar
# MAGIC    (cota do Free Edition, por exemplo), a linha cai na regra e o pipeline segue.

# COMMAND ----------

MODELO_IA = "system.ai.llama-4-maverick"
USAR_IA = True          # False = só regras (por exemplo, se a cota do Free Edition acabar)

PROMPT_ENDERECO = ("Voce padroniza enderecos brasileiros de entrega. Separe o endereco em partes e padronize: "
                   "tipo de logradouro por extenso (R. = Rua, Av. = Avenida, Tv. = Travessa, Al. = Alameda), "
                   "nomes com iniciais maiusculas e a cidade pelo nome oficial (BH = Belo Horizonte, Ctba = Curitiba, "
                   "Sampa ou S. Paulo = Sao Paulo, Cps = Campinas). Numero so com digitos; se nao houver numero ou se "
                   "for S/N, devolva vazio. Se nao houver bairro, devolva vazio. Nao invente nada que nao esteja no texto. "
                   "Endereco: ")
PROMPT_NOME = ("Voce padroniza nomes de empresas brasileiras para um cadastro. Devolva o nome no formato TIPO DE NEGOCIO + "
               "NOME, em maiusculas, sem acentos, sem sufixo societario (LTDA, S.A., ME, EIRELI), com abreviacoes e "
               "iniciais por extenso (Superm. = SUPERMERCADO, Drog. = DROGARIA, S. = SAO, Sta. = SANTA, N. = NOVA, "
               "B. = BOA, V. = VALE) e erros de digitacao corrigidos. Exemplos: Bom Preco Supermercado = "
               "SUPERMERCADO BOM PRECO; Drogaira Sta. Clara ME = DROGARIA SANTA CLARA. Nome: ")


def _formato(nome, campos):
    return json.dumps({"type": "json_schema", "json_schema": {"name": nome, "strict": True, "schema": {
        "type": "object", "additionalProperties": False, "required": campos,
        "properties": {c: {"type": "string"} for c in campos}}}})


def _ai(prompt, coluna, formato):
    return (f"ai_query('{MODELO_IA}', CONCAT('{prompt}', {coluna}), "
            f"responseFormat => '{formato}', failOnError => false)")


SEM_RESPOSTA = "CAST(NULL AS STRUCT<result: STRING, errorMessage: STRING>)"

# Plano B por regra para o endereço em texto livre (pior que a IA, mas não para o pipeline)
_tipo = ("regexp_replace(regexp_replace(regexp_replace(regexp_replace({x}, "
         "'^(?i)(r\\\\.?|rua) ', 'Rua '), '^(?i)(av\\\\.?|avda\\\\.?|avenida) ', 'Avenida '), "
         "'^(?i)(tv\\\\.?|trav\\\\.?|travessa) ', 'Travessa '), '^(?i)(al\\\\.?|alameda) ', 'Alameda ')")
REGRA_END = {
    "logradouro": "initcap(" + _tipo.format(x="regexp_extract(endereco_entrega, '^(.+?)(,| n[º°] | - )', 1)") + ")",
    "numero": "NULLIF(regexp_extract(endereco_entrega, '(,|n[º°]) *([0-9]{1,5})\\\\b', 2), '')",
    "bairro": ("NULLIF(COALESCE(NULLIF(regexp_extract(endereco_entrega, ' - ([^-]+?) - ', 1), ''), "
               "NULLIF(regexp_extract(endereco_entrega, '^[^,]+(, *[0-9]+)?, ([^,0-9]+), [^,]+$', 2), '')), 'S/N')"),
    "cidade": cidade_padrao("regexp_extract(endereco_entrega, '(, | - )([^,-]*?)[ /-]([A-Z]{2}) *$', 2)"),
}


def sql_enderecos(com_ia):
    resp = _ai(PROMPT_ENDERECO, "endereco_entrega", _formato("endereco", ["logradouro", "numero", "bairro", "cidade"])) \
        if com_ia else SEM_RESPOSTA
    ok = "(e IS NOT NULL AND erro IS NULL)"
    return f"""
    WITH d AS (SELECT DISTINCT endereco_entrega FROM lodlog_bronze.tms_destinatarios_raw),
    r AS (SELECT endereco_entrega, {resp} AS resp FROM d),
    p AS (SELECT endereco_entrega, resp.errorMessage AS erro,
                 from_json(resp.result, 'logradouro STRING, numero STRING, bairro STRING, cidade STRING') AS e FROM r)
    SELECT endereco_entrega,
           CASE WHEN {ok} THEN 'ia' ELSE 'regra' END                                        AS metodo,
           CASE WHEN {ok} THEN initcap(e.logradouro) ELSE {REGRA_END['logradouro']} END     AS logradouro,
           CASE WHEN {ok} THEN NULLIF(regexp_replace(e.numero, '[^0-9]', ''), '') ELSE {REGRA_END['numero']} END AS numero,
           CASE WHEN {ok} THEN NULLIF(trim(e.bairro), '') ELSE {REGRA_END['bairro']} END    AS bairro,
           CASE WHEN {ok} THEN {cidade_padrao('e.cidade')} ELSE {REGRA_END['cidade']} END   AS cidade
    FROM p"""


def sql_nomes(com_ia):
    resp = _ai(PROMPT_NOME, "nome", _formato("nome", ["nome_padronizado"])) if com_ia else SEM_RESPOSTA
    return f"""
    WITH d AS (SELECT chave_origem, nome, chave_nome FROM lodlog_silver.cliente_candidatos
               WHERE sistema = 'CRM' AND cnpj IS NULL),
    r AS (SELECT *, {resp} AS resp FROM d),
    p AS (SELECT *, from_json(resp.result, 'nome_padronizado STRING').nome_padronizado AS n, resp.errorMessage AS erro FROM r)
    SELECT chave_origem, nome, n AS nome_padronizado_ia,
           CASE WHEN n IS NOT NULL AND erro IS NULL THEN {chave_nome('n')} ELSE chave_nome END AS chave_nome_padronizada,
           CASE WHEN n IS NOT NULL AND erro IS NULL THEN 'ia' ELSE 'regra' END AS metodo
    FROM p"""


def padronizar(tabela, gerar_sql):
    """Cria a tabela com IA (ou reaproveita a que já existe); se a IA falhar, usa só a regra."""
    if spark.catalog.tableExists(tabela) and spark.sql(f"SELECT COUNT(*) FROM {tabela} WHERE metodo = 'ia'").first()[0] > 0:
        print(f"{tabela}: reaproveitando o resultado da IA já gravado (sem custo novo).")
        return
    spark.sql(f"DROP TABLE IF EXISTS {tabela}")
    try:
        if not USAR_IA:
            raise RuntimeError("USAR_IA = False")
        spark.sql(f"CREATE TABLE {tabela} USING DELTA AS {gerar_sql(True)}")
    except Exception as e:
        print(f"{tabela}: IA indisponível ({str(e).splitlines()[0][:90]}) → seguindo só com regras.")
        spark.sql(f"CREATE TABLE {tabela} USING DELTA AS {gerar_sql(False)}")
    for r in spark.sql(f"SELECT metodo, COUNT(*) AS n FROM {tabela} GROUP BY metodo").collect():
        print(f"{tabela}: {r['n']:,} linha(s) padronizada(s) por {r['metodo']}")


padronizar("lodlog_silver.endereco_tms_padronizado", sql_enderecos)
padronizar("lodlog_silver.nome_crm_padronizado", sql_nomes)
display(spark.sql("""SELECT endereco_entrega AS como_chegou, logradouro, numero, bairro, cidade, metodo
                     FROM lodlog_silver.endereco_tms_padronizado ORDER BY endereco_entrega LIMIT 15"""))
display(spark.table("lodlog_silver.nome_crm_padronizado").limit(15))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 7B.3 · Casamento: quem é quem nos três sistemas (pronto)
# MAGIC A tabela **de-para** (*cross-reference*, DMBOK cap. 10) liga cada registro de origem a um **id mestre**.
# MAGIC Três regras, da mais forte para a mais fraca — e cada linha guarda qual regra a casou (rastreabilidade):
# MAGIC 1. **ERP:** mesmo CNPJ = mesma empresa. O menor código vira o id mestre; os outros são cadastro duplicado.
# MAGIC 2. **TMS:** o código do cliente no TMS é o mesmo do ERP (chave transacional).
# MAGIC 3. **CRM:** primeiro pelo CNPJ; sem CNPJ, pelo nome padronizado + cidade. O que não casar vai para a
# MAGIC    **fila do steward** — uma pessoa decide, não o algoritmo.

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS lodlog_silver.cliente_xref;
# MAGIC CREATE TABLE lodlog_silver.cliente_xref USING DELTA AS
# MAGIC WITH erp AS (
# MAGIC   SELECT chave_origem, cliente_id, cnpj, chave_nome, cidade,
# MAGIC          MIN(cliente_id) OVER (PARTITION BY COALESCE(cnpj, chave_origem)) AS id_mestre
# MAGIC   FROM lodlog_silver.cliente_candidatos WHERE sistema = 'ERP'),
# MAGIC mestre AS (SELECT id_mestre, cnpj, chave_nome, cidade FROM erp WHERE cliente_id = id_mestre),
# MAGIC crm AS (
# MAGIC   SELECT c.chave_origem, c.cnpj, c.cidade,
# MAGIC          COALESCE(n.chave_nome_padronizada, c.chave_nome) AS chave_nome, COALESCE(n.metodo, 'regra') AS metodo
# MAGIC   FROM lodlog_silver.cliente_candidatos c
# MAGIC   LEFT JOIN lodlog_silver.nome_crm_padronizado n ON n.chave_origem = c.chave_origem
# MAGIC   WHERE c.sistema = 'CRM')
# MAGIC SELECT 'ERP' AS sistema, chave_origem, id_mestre,
# MAGIC        CASE WHEN cliente_id = id_mestre THEN 'registro original' ELSE 'mesmo CNPJ (cadastro duplicado)' END AS regra_casamento
# MAGIC FROM erp
# MAGIC UNION ALL
# MAGIC SELECT 'TMS', t.destinatario_id, e.id_mestre, 'código do cliente no TMS'
# MAGIC FROM lodlog_bronze.tms_destinatarios_raw t
# MAGIC JOIN erp e ON e.cliente_id = CAST(t.cliente_id AS INT)
# MAGIC UNION ALL
# MAGIC SELECT 'CRM', crm.chave_origem, COALESCE(m1.id_mestre, m2.id_mestre),
# MAGIC        CASE WHEN m1.id_mestre IS NOT NULL THEN 'mesmo CNPJ'
# MAGIC             WHEN m2.id_mestre IS NOT NULL THEN CONCAT('mesmo nome e cidade (', crm.metodo, ')')
# MAGIC             ELSE 'sem casamento: fila do steward' END
# MAGIC FROM crm
# MAGIC LEFT JOIN mestre m1 ON m1.cnpj = crm.cnpj
# MAGIC LEFT JOIN mestre m2 ON crm.cnpj IS NULL AND m2.chave_nome = crm.chave_nome AND m2.cidade = crm.cidade;
# MAGIC
# MAGIC SELECT sistema, regra_casamento, COUNT(*) AS registros
# MAGIC FROM lodlog_silver.cliente_xref GROUP BY sistema, regra_casamento ORDER BY sistema, registros DESC;

# COMMAND ----------

# MAGIC %md
# MAGIC ### 7B.4 · O scorecard do dado crítico (pronto)
# MAGIC Primeiro, todos os endereços candidatos de cada cliente mestre (o do ERP e as versões do TMS), já com as
# MAGIC quatro regras de qualidade calculadas. Depois, o **scorecard** com as dimensões do DMBOK (Aula 4) — a
# MAGIC fotografia do problema **antes** de qualquer decisão.

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS lodlog_silver.cliente_enderecos;
# MAGIC CREATE TABLE lodlog_silver.cliente_enderecos USING DELTA AS
# MAGIC WITH e AS (
# MAGIC   SELECT x.id_mestre, 'ERP' AS sistema, c.chave_origem, initcap(c.logradouro) AS logradouro, c.numero, c.bairro,
# MAGIC          c.cidade, c.cep, 'cadastro' AS metodo
# MAGIC   FROM lodlog_silver.cliente_candidatos c
# MAGIC   JOIN lodlog_silver.cliente_xref x ON x.sistema = 'ERP' AND x.chave_origem = c.chave_origem
# MAGIC   WHERE c.sistema = 'ERP'
# MAGIC   UNION ALL
# MAGIC   SELECT x.id_mestre, 'TMS', t.destinatario_id, p.logradouro, p.numero, p.bairro, p.cidade,
# MAGIC          NULLIF(regexp_replace(t.cep_informado, '[^0-9]', ''), ''), p.metodo
# MAGIC   FROM lodlog_bronze.tms_destinatarios_raw t
# MAGIC   JOIN lodlog_silver.endereco_tms_padronizado p ON p.endereco_entrega = t.endereco_entrega
# MAGIC   JOIN lodlog_silver.cliente_xref x ON x.sistema = 'TMS' AND x.chave_origem = t.destinatario_id)
# MAGIC SELECT e.*, r.uf,
# MAGIC        COALESCE(e.cep RLIKE '^[0-9]{8}$', FALSE)                     AS cep_8_digitos,
# MAGIC        COALESCE(e.cep BETWEEN r.cep_inicio AND r.cep_fim, FALSE)      AS cep_coerente_com_cidade,
# MAGIC        COALESCE(e.numero RLIKE '^[0-9]+$', FALSE)                     AS tem_numero,
# MAGIC        COALESCE(LENGTH(TRIM(e.bairro)) > 0, FALSE)                    AS tem_bairro,
# MAGIC        COUNT(*) OVER (PARTITION BY e.id_mestre, e.sistema, lower(e.logradouro), e.numero) AS frequencia
# MAGIC FROM e LEFT JOIN lodlog_silver.ref_faixa_cep r ON r.cidade = e.cidade;
# MAGIC
# MAGIC DROP TABLE IF EXISTS lodlog_gold.scorecard_cliente;
# MAGIC CREATE TABLE lodlog_gold.scorecard_cliente USING DELTA AS
# MAGIC WITH s AS (
# MAGIC   SELECT 'Unicidade' AS dimensao, 'Um código de cliente por CNPJ' AS regra, 'ERP' AS sistema,
# MAGIC          COUNT(*) AS registros, SUM(CASE WHEN regra_casamento = 'registro original' THEN 0 ELSE 1 END) AS violacoes
# MAGIC   FROM lodlog_silver.cliente_xref WHERE sistema = 'ERP'
# MAGIC   UNION ALL
# MAGIC   SELECT 'Completude', 'CEP preenchido', sistema, COUNT(*), SUM(CASE WHEN cep IS NULL THEN 1 ELSE 0 END)
# MAGIC   FROM lodlog_silver.cliente_enderecos GROUP BY sistema
# MAGIC   UNION ALL
# MAGIC   SELECT 'Completude', 'Número do endereço preenchido', sistema, COUNT(*), SUM(CASE WHEN tem_numero THEN 0 ELSE 1 END)
# MAGIC   FROM lodlog_silver.cliente_enderecos GROUP BY sistema
# MAGIC   UNION ALL
# MAGIC   SELECT 'Validade', 'CEP com 8 dígitos', sistema, COUNT(*), SUM(CASE WHEN cep_8_digitos THEN 0 ELSE 1 END)
# MAGIC   FROM lodlog_silver.cliente_enderecos GROUP BY sistema
# MAGIC   UNION ALL
# MAGIC   SELECT 'Consistência', 'CEP dentro da faixa da cidade', sistema, COUNT(*),
# MAGIC          SUM(CASE WHEN cep_coerente_com_cidade THEN 0 ELSE 1 END)
# MAGIC   FROM lodlog_silver.cliente_enderecos GROUP BY sistema
# MAGIC   UNION ALL
# MAGIC   SELECT 'Completude', 'CNPJ preenchido', 'CRM', COUNT(*), SUM(CASE WHEN cnpj IS NULL THEN 1 ELSE 0 END)
# MAGIC   FROM lodlog_silver.cliente_candidatos WHERE sistema = 'CRM'
# MAGIC   UNION ALL
# MAGIC   SELECT 'Integridade', 'Conta do CRM ligada a um cliente', 'CRM', COUNT(*),
# MAGIC          SUM(CASE WHEN id_mestre IS NULL THEN 1 ELSE 0 END)
# MAGIC   FROM lodlog_silver.cliente_xref WHERE sistema = 'CRM')
# MAGIC SELECT *, ROUND(100.0 * (registros - violacoes) / registros, 1) AS pct_ok FROM s;
# MAGIC
# MAGIC SELECT * FROM lodlog_gold.scorecard_cliente ORDER BY pct_ok;

# COMMAND ----------

# MAGIC %md
# MAGIC > **Para discutir:** a "violação" de integridade do CRM é sempre erro? Nem toda conta da planilha comercial
# MAGIC > é cliente — algumas são *prospects*. A regra de qualidade precisa da **definição de negócio** para ser justa.
# MAGIC
# MAGIC ### 7B.5 · 🟨 TODO 5 · O registro de ouro do cliente
# MAGIC O DMBOK chama de **registro de ouro** (*golden record*) a melhor versão que a empresa tem de cada entidade —
# MAGIC e alerta: "ouro" não é "verdade única"; é uma escolha documentada. Duas escolhas são do grupo:
# MAGIC
# MAGIC **5a · De onde vem o endereço de entrega oficial?** (a razão social já vem do ERP, sistema de registro do cliente)
# MAGIC
# MAGIC | Opção | O que significa | A favor | Contra |
# MAGIC |---|---|---|---|
# MAGIC | `erp` | o cadastro do faturamento | tem dono formal (Comercial) e campos separados | o endereço de cobrança nem sempre é o de entrega |
# MAGIC | `tms_mais_frequente` | a versão que o operador mais usa | é onde o motorista de fato vai | herda os erros de digitação do CD |
# MAGIC | `mais_completo` | a versão, de qualquer sistema, que passa em mais regras | maximiza a qualidade | mistura origens: quem é o dono? |
# MAGIC
# MAGIC **5b · O que é um "endereço válido para entrega" na LODLog?** Marquem `True` nas regras que valem. Olhem o
# MAGIC scorecard acima: regra demais reprova cliente bom; regra de menos deixa passar o endereço que atrasa a entrega.

# COMMAND ----------

# 🟨 TODO 5a — de onde vem o endereço do registro de ouro? "erp", "tms_mais_frequente" ou "mais_completo"
FONTE_ENDERECO = None

# 🟨 TODO 5b — quais regras definem um endereço válido para entrega? True ou False em cada uma
REGRAS_ENDERECO = {
    "cep_8_digitos": None,             # o CEP tem 8 dígitos
    "cep_coerente_com_cidade": None,   # o CEP cai na faixa da cidade (tabela ref_faixa_cep)
    "tem_numero": None,                # o endereço tem número (não é S/N nem vazio)
    "tem_bairro": None,                # o endereço tem bairro
}

# COMMAND ----------

# Construção do registro de ouro (pronto — usa as decisões acima)
ORDEM_ENDERECO = {
    "erp": ("sistema = 'ERP'", "n_regras_ok DESC"),
    "tms_mais_frequente": ("sistema = 'TMS'", "frequencia DESC, n_regras_ok DESC"),
    "mais_completo": ("TRUE", "n_regras_ok DESC, CASE sistema WHEN 'ERP' THEN 0 ELSE 1 END"),
}
mdm_ok = FONTE_ENDERECO in ORDEM_ENDERECO and all(v is not None for v in REGRAS_ENDERECO.values())
if not mdm_ok:
    print("⏸  TODO 5 pendente: defina FONTE_ENDERECO e marque True/False em todas as REGRAS_ENDERECO.")
else:
    ativas = [r for r, v in REGRAS_ENDERECO.items() if v]
    valido = " AND ".join(ativas) if ativas else "TRUE"
    pontos = " + ".join(f"CAST({r} AS INT)" for r in ativas) if ativas else "0"
    filtro, ordem = ORDEM_ENDERECO[FONTE_ENDERECO]
    spark.sql("DROP TABLE IF EXISTS lodlog_gold.cliente_mestre")
    spark.sql(f"""
    CREATE TABLE lodlog_gold.cliente_mestre USING DELTA AS
    WITH e AS (SELECT *, {pontos} AS n_regras_ok, ({valido}) AS valido FROM lodlog_silver.cliente_enderecos),
    escolhido AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY id_mestre ORDER BY {ordem}) AS rn FROM e WHERE {filtro}),
    nome AS (SELECT x.id_mestre, c.nome AS razao_social, c.cnpj
             FROM lodlog_silver.cliente_candidatos c
             JOIN lodlog_silver.cliente_xref x ON x.sistema = 'ERP' AND x.chave_origem = c.chave_origem
             WHERE c.sistema = 'ERP' AND x.regra_casamento = 'registro original'),
    origem AS (SELECT id_mestre, COUNT(*) AS registros_de_origem,
                      concat_ws(' + ', array_sort(collect_set(sistema))) AS sistemas
               FROM lodlog_silver.cliente_xref WHERE id_mestre IS NOT NULL GROUP BY id_mestre),
    tms AS (SELECT id_mestre, ROUND(100.0 * AVG(CAST(valido AS INT)), 0) AS pct_enderecos_tms_validos
            FROM e WHERE sistema = 'TMS' GROUP BY id_mestre)
    SELECT n.id_mestre, n.razao_social, n.cnpj,
           s.logradouro, s.numero, s.bairro, s.cidade, s.uf, s.cep,
           s.sistema AS fonte_endereco, COALESCE(s.valido, FALSE) AS endereco_valido,
           o.registros_de_origem, o.sistemas, t.pct_enderecos_tms_validos
    FROM nome n
    LEFT JOIN escolhido s ON s.id_mestre = n.id_mestre AND s.rn = 1
    LEFT JOIN origem o ON o.id_mestre = n.id_mestre
    LEFT JOIN tms t ON t.id_mestre = n.id_mestre""")

    # O significado do dado crítico vai para o glossário e para o catálogo, com dono e steward
    registrar_termos([
        {"termo": "Cliente mestre", "dono": "Diretoria Comercial", "steward": "Analista de cadastro (Comercial)",
         "definicao": "Empresa atendida pela LODLog, identificada pelo CNPJ, com um único registro de ouro que liga "
                      "seus códigos no ERP, no TMS e no CRM.",
         "regra": "um id_mestre por CNPJ; de-para em lodlog_silver.cliente_xref",
         "tabela": "lodlog_gold.cliente_mestre", "coluna": "id_mestre"},
        {"termo": "Endereço válido para entrega", "dono": "Diretoria de Operações", "steward": "Coordenação de cadastro do CD",
         "definicao": "Endereço que atende às regras definidas pela LODLog: " + (", ".join(ativas) or "nenhuma regra"),
         "regra": valido, "tabela": "lodlog_gold.cliente_mestre", "coluna": "endereco_valido"},
    ], origem="mdm")
    aplicar_governanca("lodlog_gold.cliente_mestre", {
        "dono": "Diretoria Comercial",
        "descricao": f"Registro de ouro do cliente (endereço vindo de: {FONTE_ENDERECO}), a partir de ERP, TMS e CRM.",
        "contem_dados_pessoais": False,          # CNPJ é dado de empresa (atenção a MEs: o CNPJ pode identificar uma pessoa)
        "retencao_dias": 3650,
        "regra_qualidade": "chave_unica",
    })
    marcar_no_catalogo("lodlog_gold.cliente_mestre", {"dominio": "cliente", "dado_critico": "sim", "camada": "gold"})

    r = spark.sql("""SELECT COUNT(*) AS mestres, SUM(registros_de_origem) AS origem,
                            SUM(CASE WHEN endereco_valido THEN 1 ELSE 0 END) AS validos
                     FROM lodlog_gold.cliente_mestre""").first()
    print(f"{r['origem']:,} registros de origem (ERP + TMS + CRM) → {r['mestres']:,} clientes mestres · "
          f"{r['validos']:,} com endereço válido para entrega ({100 * r['validos'] / r['mestres']:.0f}%)")
    display(spark.sql("SELECT * FROM lodlog_gold.cliente_mestre ORDER BY registros_de_origem DESC LIMIT 10"))

# COMMAND ----------

# MAGIC %md
# MAGIC ### 7B.6 · O que o dado crítico custa para o negócio (pronto)
# MAGIC A pergunta que justifica o MDM para a diretoria: **endereço ruim no TMS atrasa a entrega?** A consulta
# MAGIC separa os clientes pela parte das suas versões de endereço no TMS que passam na definição do TODO 5.

# COMMAND ----------

if spark.catalog.tableExists("lodlog_gold.cliente_mestre"):
    display(spark.sql("""
        SELECT CASE WHEN m.pct_enderecos_tms_validos = 100 THEN '1. todas as versões do TMS válidas'
                    WHEN m.pct_enderecos_tms_validos > 0  THEN '2. parte das versões inválida'
                    ELSE '3. nenhuma versão válida no TMS' END                    AS endereco_no_tms,
               COUNT(DISTINCT m.id_mestre)                                       AS clientes,
               COUNT(*)                                                          AS entregas,
               ROUND(100.0 * AVG(CASE WHEN e.no_prazo THEN 1 ELSE 0 END), 1)     AS pct_no_prazo
        FROM lodlog_silver.tms_entregas e
        JOIN lodlog_silver.cliente_xref x ON x.sistema = 'ERP' AND x.chave_origem = CAST(e.cliente_id AS STRING)
        JOIN lodlog_gold.cliente_mestre m ON m.id_mestre = x.id_mestre
        WHERE e.status = 'Entregue'
        GROUP BY 1 ORDER BY 1"""))
else:
    print("⏸  O impacto aparece depois do TODO 5 (registro de ouro).")

# COMMAND ----------

# MAGIC %md
# MAGIC > **Frase para a diretoria (formato):** *"X% dos clientes têm endereço inválido no TMS e recebem no prazo
# MAGIC > Y pontos a menos; corrigir o cadastro na origem, com dono e regra definidos, é mais barato que a multa."*
# MAGIC > Ajustem X e Y com o resultado de vocês — e notem como a resposta muda conforme as regras do TODO 5b.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Etapa 8 — Conferência final e números para o pitch (pronto)
# MAGIC Rodem esta célula ao fim de cada sessão. Tudo ✅ = notebook pronto para a apresentação da Aula 5.

# COMMAND ----------

def _existe(t):
    return spark.catalog.tableExists(t)


print("═" * 72)
print(f"Cenário: {CENARIO or '— não definido —'}")
cen = CENARIOS[0] if CENARIOS else None
gold = GOLD[cen][0] if cen else None
checks = [
    ("Cenário escolhido", bool(cen)),
    ("TODO 1 · fonte extra na Silver",
     bool(cen) and _existe({"clima": "lodlog_silver.clima_diario", "ocorrencias": "lodlog_silver.ocorrencias"}[FONTE_DO_CENARIO[cen]])),
    ("TODO 2 · Gold do cenário com métrica-chave",
     bool(gold) and _existe(gold) and spark.sql(f"SELECT COUNT(metrica_chave) FROM {gold}").first()[0] > 0),
    ("TODO 3 · pergunta de negócio", len(PERGUNTA_NEGOCIO.strip()) > 10),
    ("TODO 3 · interpretação", len(INTERPRETACAO.strip()) > 20),
    ("TODO 4 · governança aplicada",
     bool(gold) and _existe(gold) and any(r["key"] == "lodlog.dono" for r in spark.sql(f"SHOW TBLPROPERTIES {gold}").collect())),
    ("TODO 4 · dois termos no glossário",
     _existe("lodlog_gold.glossario_negocio")
     and spark.sql("SELECT COUNT(*) FROM lodlog_gold.glossario_negocio WHERE origem = 'grupo'").first()[0] >= 2),
    ("TODO 5 · registro de ouro do cliente", _existe("lodlog_gold.cliente_mestre")),
]
for nome, ok in checks:
    print(f"  {'✅' if ok else '⬜'} {nome}")

print("\nNúmeros do pipeline (para o slide de execução):")
for camada in ["lodlog_bronze", "lodlog_silver", "lodlog_gold"]:
    for r in spark.sql(f"SHOW TABLES IN {camada}").collect():
        t = f"{camada}.{r['tableName']}"
        print(f"  {t:45s} {spark.table(t).count():>8,} linhas")
if _existe("lodlog_gold.cliente_mestre"):
    m = spark.sql("""SELECT COUNT(*) AS mestres, SUM(registros_de_origem) AS origem,
                             SUM(CASE WHEN endereco_valido THEN 1 ELSE 0 END) AS validos FROM lodlog_gold.cliente_mestre""").first()
    fila = spark.sql("SELECT COUNT(*) FROM lodlog_silver.cliente_xref WHERE id_mestre IS NULL").first()[0]
    print(f"\nDado crítico (MDM): {m['origem']:,} registros de origem → {m['mestres']:,} clientes mestres · "
          f"{m['validos']:,} com endereço válido · {fila} conta(s) do CRM na fila do steward")
    print(f"  Endereço oficial vem de: {FONTE_ENDERECO} · regras: {[r for r, v in REGRAS_ENDERECO.items() if v]}")
if PERGUNTA_NEGOCIO.strip():
    print(f"\nPergunta: {PERGUNTA_NEGOCIO}\nInterpretação: {INTERPRETACAO or '—'}")
print("═" * 72)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Para levar para a apresentação (Aula 5)
# MAGIC
# MAGIC - **Arquitetura:** as seis fontes → Bronze → Silver → Gold, destacando **o que veio pronto e o que o grupo construiu**.
# MAGIC - **Integração:** a Gold de vocês junta uma fonte estruturada (TMS, WMS ou ERP) com uma semi/não estruturada (clima ou ocorrências).
# MAGIC - **Execução:** os números da Etapa 8 — quantas linhas a qualidade barrou em cada camada e por quê.
# MAGIC - **Análise:** a pergunta, a consulta e a frase para a diretoria (TODO 3).
# MAGIC - **Dado crítico:** quantos registros viraram quantos clientes mestres, de onde vem o endereço oficial,
# MAGIC   a definição de "endereço válido" e o efeito na pontualidade (TODO 5, Etapa 7B). Quem é o dono e o steward?
# MAGIC - **Avaliação pós-projeto (preliminar):** 2 vantagens, 2 limitações e 1 lição. A versão completa é a entrega individual.
# MAGIC
# MAGIC > 🧹 *Para recomeçar do zero:* `DROP SCHEMA lodlog_gold CASCADE` (idem silver e bronze) e Run All.
