"""
Dashboard de Análise de Ações Brasileiras — B3 (2024)
======================================================
Análises:
  1. Retorno acumulado dos ativos vs Ibovespa
  2. Volatilidade anualizada por ativo
  3. Matriz de correlação entre ativos
  4. Comparativo de desempenho por setor vs Ibovespa
  5. Análise de risco x retorno (scatter)
  6. Sazonalidade — retorno médio mensal por setor
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

# ── Configuração visual ──────────────────────────────────────────────────────
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.3,
    "grid.linestyle": "--",
    "figure.dpi": 130,
})

CORES_SETOR = {
    "Bancário":      "#1A5276",
    "Energia":       "#D4AC0D",
    "Mineração":     "#7B241C",
    "Varejo":        "#1E8449",
    "Consumo":       "#6C3483",
    "Indústria":     "#1A535C",
    "Papel/Celulose":"#935116",
}
COR_IBOV = "#E74C3C"

# ── Carrega dados ────────────────────────────────────────────────────────────
df = pd.read_csv("data/acoes_b3_2024.csv", parse_dates=["data"])
ibov = pd.read_csv("data/ibovespa_2024.csv", parse_dates=["data"])

# Retorno diário por ativo
df_pivot = df.pivot(index="data", columns="ticker", values="preco_fechamento")
ret_diario = df_pivot.pct_change().dropna()

# Mapeia setor por ticker
setor_map = df.drop_duplicates("ticker").set_index("ticker")["setor"].to_dict()

# ════════════════════════════════════════════════════════════════════════════
# ANÁLISE 1 — Retorno acumulado vs Ibovespa
# ════════════════════════════════════════════════════════════════════════════
ret_acum = ((1 + ret_diario).cumprod() - 1) * 100

fig, ax = plt.subplots(figsize=(13, 6))
for ticker in ret_acum.columns:
    setor = setor_map.get(ticker, "Outros")
    cor = CORES_SETOR.get(setor, "#888888")
    ax.plot(ret_acum.index, ret_acum[ticker], color=cor, lw=1.3, alpha=0.75, label=f"{ticker} ({setor})")
    ax.text(ret_acum.index[-1] + pd.Timedelta(days=2),
            ret_acum[ticker].iloc[-1],
            ticker, fontsize=8, color=cor, va="center")

# Ibovespa como benchmark
ibov_ret = ibov.set_index("data")["preco_fechamento"].pct_change().dropna()
ibov_acum = ((1 + ibov_ret).cumprod() - 1) * 100
ax.plot(ibov_acum.index, ibov_acum, color=COR_IBOV, lw=2.2, ls="--", label="Ibovespa", zorder=5)
ax.text(ibov_acum.index[-1] + pd.Timedelta(days=2), ibov_acum.iloc[-1],
        "IBOV", fontsize=9, color=COR_IBOV, fontweight="bold", va="center")

ax.axhline(0, color="#AAAAAA", lw=1)
ax.set_title("Retorno Acumulado — Ativos B3 vs Ibovespa (2024)", fontsize=13, fontweight="bold", pad=14)
ax.set_ylabel("Retorno acumulado (%)")
ax.set_xlabel("")
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
ax.set_xlim(ret_acum.index[0], ret_acum.index[-1] + pd.Timedelta(days=25))
plt.tight_layout()
plt.savefig("outputs/01_retorno_acumulado.png", bbox_inches="tight")
plt.close()
print("✓ Análise 1 — Retorno acumulado salva")

# ════════════════════════════════════════════════════════════════════════════
# ANÁLISE 2 — Volatilidade anualizada por ativo
# ════════════════════════════════════════════════════════════════════════════
vol_anual = (ret_diario.std() * np.sqrt(252) * 100).sort_values(ascending=True)
retorno_total = ret_acum.iloc[-1].reindex(vol_anual.index)
cores_bar = [CORES_SETOR.get(setor_map.get(t, ""), "#888888") for t in vol_anual.index]

fig, ax = plt.subplots(figsize=(9, 5.5))
bars = ax.barh(vol_anual.index, vol_anual.values, color=cores_bar, alpha=0.88, edgecolor="none")
for bar, ret in zip(bars, retorno_total.reindex(vol_anual.index)):
    sinal = "+" if ret >= 0 else ""
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            f"{sinal}{ret:.1f}%", va="center", fontsize=9,
            color="#1E8449" if ret >= 0 else "#922B21")

# Linha do Ibovespa
vol_ibov = ibov_ret.std() * np.sqrt(252) * 100
ax.axvline(vol_ibov, color=COR_IBOV, lw=1.5, ls="--")
ax.text(vol_ibov + 0.2, -0.6, f"IBOV\n{vol_ibov:.1f}%", fontsize=8.5, color=COR_IBOV)

ax.set_xlabel("Volatilidade Anualizada (%)")
ax.set_title("Volatilidade Anualizada por Ativo\n(retorno acumulado no ano em destaque)", fontsize=12, fontweight="bold", pad=12)
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
plt.tight_layout()
plt.savefig("outputs/02_volatilidade.png", bbox_inches="tight")
plt.close()
print("✓ Análise 2 — Volatilidade salva")

# ════════════════════════════════════════════════════════════════════════════
# ANÁLISE 3 — Matriz de correlação
# ════════════════════════════════════════════════════════════════════════════
corr = ret_diario.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))

fig, ax = plt.subplots(figsize=(9, 7.5))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="RdYlGn",
            vmin=-0.2, vmax=1, linewidths=0.5, linecolor="#dddddd",
            ax=ax, annot_kws={"size": 9},
            cbar_kws={"label": "Coeficiente de Correlação"})
ax.set_title("Matriz de Correlação — Retornos Diários (2024)", fontsize=12, fontweight="bold", pad=12)
ax.tick_params(axis="x", rotation=45)
ax.tick_params(axis="y", rotation=0)
plt.tight_layout()
plt.savefig("outputs/03_correlacao.png", bbox_inches="tight")
plt.close()
print("✓ Análise 3 — Matriz de correlação salva")

# ════════════════════════════════════════════════════════════════════════════
# ANÁLISE 4 — Desempenho por setor vs Ibovespa
# ════════════════════════════════════════════════════════════════════════════
df["mes"] = df["data"].dt.to_period("M")
ibov["mes"] = ibov["data"].dt.to_period("M")

# Retorno mensal por ativo
df_ret_mes = (df.groupby(["ticker", "mes"])["preco_fechamento"]
               .apply(lambda x: (x.iloc[-1] / x.iloc[0] - 1) * 100)
               .reset_index(name="retorno_mensal"))
df_ret_mes["setor"] = df_ret_mes["ticker"].map(setor_map)
ret_setor_mes = df_ret_mes.groupby(["setor", "mes"])["retorno_mensal"].mean().reset_index()

ibov_ret_mes = (ibov.groupby("mes")["preco_fechamento"]
                    .apply(lambda x: (x.iloc[-1] / x.iloc[0] - 1) * 100)
                    .reset_index(name="retorno_mensal"))

fig, ax = plt.subplots(figsize=(13, 5.5))
for setor, cor in CORES_SETOR.items():
    sub = ret_setor_mes[ret_setor_mes["setor"] == setor]
    if sub.empty:
        continue
    meses = [str(m) for m in sub["mes"]]
    ax.plot(meses, sub["retorno_mensal"], color=cor, lw=2, marker="o", ms=5, label=setor, alpha=0.9)

ibov_x = [str(m) for m in ibov_ret_mes["mes"]]
ax.plot(ibov_x, ibov_ret_mes["retorno_mensal"], color=COR_IBOV, lw=2.2, ls="--",
        marker="D", ms=5, label="Ibovespa", zorder=5)
ax.axhline(0, color="#AAAAAA", lw=1)
ax.set_title("Retorno Mensal por Setor vs Ibovespa (2024)", fontsize=12, fontweight="bold", pad=12)
ax.set_ylabel("Retorno mensal (%)")
ax.set_xlabel("")
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f%%"))
ax.legend(fontsize=9, loc="upper right", ncol=2)
plt.xticks(rotation=45, fontsize=9)
plt.tight_layout()
plt.savefig("outputs/04_desempenho_setorial.png", bbox_inches="tight")
plt.close()
print("✓ Análise 4 — Desempenho setorial salva")

# ════════════════════════════════════════════════════════════════════════════
# ANÁLISE 5 — Risco x Retorno
# ════════════════════════════════════════════════════════════════════════════
ret_final = ret_acum.iloc[-1]
vol_df = ret_diario.std() * np.sqrt(252) * 100

fig, ax = plt.subplots(figsize=(9, 6.5))
for ticker in ret_final.index:
    setor = setor_map.get(ticker, "Outros")
    cor = CORES_SETOR.get(setor, "#888888")
    ax.scatter(vol_df[ticker], ret_final[ticker], color=cor, s=110, zorder=5, edgecolors="white", lw=0.8)
    ax.annotate(ticker, (vol_df[ticker], ret_final[ticker]),
                textcoords="offset points", xytext=(6, 4), fontsize=9, color=cor)

# Ibovespa como referência
ax.scatter(vol_ibov, ibov_acum.iloc[-1], color=COR_IBOV, s=130, marker="D",
           zorder=6, edgecolors="white", lw=1, label="Ibovespa")
ax.annotate("IBOV", (vol_ibov, ibov_acum.iloc[-1]),
            textcoords="offset points", xytext=(6, 4), fontsize=9, color=COR_IBOV, fontweight="bold")

ax.axhline(0, color="#AAAAAA", lw=1)
ax.axvline(vol_ibov, color=COR_IBOV, lw=1, ls="--", alpha=0.5)

# Quadrantes
xmid, ymid = vol_ibov, ibov_acum.iloc[-1]
ax.text(xmid - 5, max(ret_final) * 0.85, "Baixo risco\nAlto retorno", fontsize=8, color="#1E8449", ha="center", alpha=0.7)
ax.text(xmid + 5, max(ret_final) * 0.85, "Alto risco\nAlto retorno",  fontsize=8, color="#D4AC0D", ha="center", alpha=0.7)
ax.text(xmid - 5, min(ret_final) * 0.85, "Baixo risco\nBaixo retorno",fontsize=8, color="#888888", ha="center", alpha=0.7)
ax.text(xmid + 5, min(ret_final) * 0.85, "Alto risco\nBaixo retorno", fontsize=8, color="#922B21", ha="center", alpha=0.7)

ax.set_xlabel("Volatilidade Anualizada (%)")
ax.set_ylabel("Retorno Acumulado no Ano (%)")
ax.set_title("Matriz Risco x Retorno — Ativos B3 (2024)", fontsize=12, fontweight="bold", pad=12)
ax.xaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f%%"))
plt.tight_layout()
plt.savefig("outputs/05_risco_retorno.png", bbox_inches="tight")
plt.close()
print("✓ Análise 5 — Risco x retorno salva")

# ════════════════════════════════════════════════════════════════════════════
# ANÁLISE 6 — Sazonalidade: retorno médio mensal por setor (heatmap)
# ════════════════════════════════════════════════════════════════════════════
pivot_sazon = ret_setor_mes.pivot(index="setor", columns="mes", values="retorno_mensal")
pivot_sazon.columns = [str(c) for c in pivot_sazon.columns]
pivot_sazon.columns = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"][:len(pivot_sazon.columns)]

fig, ax = plt.subplots(figsize=(13, 4.5))
sns.heatmap(pivot_sazon, annot=True, fmt=".1f", cmap="RdYlGn", center=0,
            linewidths=0.5, linecolor="#dddddd", ax=ax, annot_kws={"size": 9},
            cbar_kws={"label": "Retorno médio mensal (%)"})
ax.set_title("Sazonalidade — Retorno Médio Mensal por Setor (2024)", fontsize=12, fontweight="bold", pad=12)
ax.set_xlabel("")
ax.set_ylabel("")
ax.tick_params(axis="y", rotation=0)
plt.tight_layout()
plt.savefig("outputs/06_sazonalidade_setorial.png", bbox_inches="tight")
plt.close()
print("✓ Análise 6 — Sazonalidade salva")

print("\n✅ Todas as análises concluídas! Imagens salvas em outputs/")
