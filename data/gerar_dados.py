"""
Gerador de dados históricos simulados — Ações B3 (2024)
Simula preços diários baseados em volatilidades e retornos reais do mercado brasileiro.
"""
import pandas as pd
import numpy as np

np.random.seed(42)

# Parâmetros baseados em comportamento real dos ativos em 2024
ATIVOS = {
    # ticker: (preco_inicial, retorno_anual, volatilidade_diaria, setor)
    "PETR4": (36.50, 0.08,  0.022, "Energia"),
    "VALE3": (70.20, -0.12, 0.025, "Mineração"),
    "ITUB4": (28.30, 0.22,  0.016, "Bancário"),
    "BBDC4": (14.80, 0.15,  0.018, "Bancário"),
    "BBAS3": (55.10, 0.28,  0.017, "Bancário"),
    "ABEV3": (12.40, -0.05, 0.014, "Consumo"),
    "MGLU3": ( 6.20, -0.30, 0.045, "Varejo"),
    "RENT3": (64.80, 0.10,  0.019, "Varejo"),
    "WEGE3": (38.50, 0.18,  0.016, "Indústria"),
    "SUZB3": (56.20, 0.25,  0.021, "Papel/Celulose"),
}

# Ibovespa
IBOV_RETORNO = 0.087
IBOV_VOL     = 0.012
IBOV_INICIO  = 131_000

datas = pd.bdate_range("2024-01-02", "2024-12-31")  # Dias úteis

registros = []

# Gera série do Ibovespa
ibov_ret = np.random.normal(IBOV_RETORNO / 252, IBOV_VOL, len(datas))
ibov_precos = [IBOV_INICIO]
for r in ibov_ret[1:]:
    ibov_precos.append(ibov_precos[-1] * (1 + r))

# Gera séries dos ativos com correlação parcial com Ibovespa
for ticker, (preco0, ret_anual, vol_dia, setor) in ATIVOS.items():
    correlacao = np.random.uniform(0.45, 0.75)  # Correlação com Ibovespa
    idio_vol   = vol_dia * np.sqrt(1 - correlacao**2)
    mkt_beta   = correlacao * vol_dia / IBOV_VOL

    ibov_diario = np.diff(np.log(ibov_precos), prepend=np.log(ibov_precos[0]))
    ret_diario  = (ret_anual / 252
                   + mkt_beta * ibov_diario
                   + np.random.normal(0, idio_vol, len(datas)))

    precos = [preco0]
    for r in ret_diario[1:]:
        precos.append(precos[-1] * np.exp(r))

    for i, (data, preco) in enumerate(zip(datas, precos)):
        variacao = (preco / preco0 - 1) * 100
        volume   = int(np.random.lognormal(15, 0.5))
        registros.append({
            "data": data.date(),
            "ticker": ticker,
            "setor": setor,
            "preco_fechamento": round(preco, 2),
            "volume": volume,
            "retorno_acumulado": round(variacao, 2),
        })

df = pd.DataFrame(registros)
df.to_csv("/home/claude/acoes-b3-dashboard/data/acoes_b3_2024.csv", index=False)

# Salva Ibovespa separado
df_ibov = pd.DataFrame({
    "data": [d.date() for d in datas],
    "ticker": "IBOV",
    "preco_fechamento": [round(p, 0) for p in ibov_precos],
    "retorno_acumulado": [round((p / IBOV_INICIO - 1) * 100, 2) for p in ibov_precos],
})
df_ibov.to_csv("/home/claude/acoes-b3-dashboard/data/ibovespa_2024.csv", index=False)

print(f"Gerados {len(df)} registros para {len(ATIVOS)} ativos")
print(f"Gerados {len(df_ibov)} registros do Ibovespa")
