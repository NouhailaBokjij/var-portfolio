import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from var_models import get_returns, historical_var, parametric_var, monte_carlo_var, backtest

st.set_page_config(page_title="VaR Portfolio", page_icon="📉", layout="wide")
st.title("📉 Value at Risk — Portfolio Risk Analyzer")
st.caption("Projet personnel — MS Finance & Gestion des Risques | ENSAE Paris")

# --- Sidebar ---
st.sidebar.header("Portfolio Settings")

tickers_input = st.sidebar.text_input(
    "Tickers (séparés par des virgules)",
    value="AAPL, MSFT, BNP.PA"
)
tickers = [t.strip() for t in tickers_input.split(",")]

period = st.sidebar.selectbox("Période historique", ["1y", "2y", "5y"], index=1)
confidence = st.sidebar.slider("Niveau de confiance", 0.90, 0.99, 0.99, step=0.01)
investment = st.sidebar.number_input("Montant investi (€)", value=100000, step=10000)

st.sidebar.subheader("Poids du portefeuille")
n = len(tickers)
weights = []
for t in tickers:
    w = st.sidebar.slider(f"Poids {t}", 0.0, 1.0, round(1/n, 2))
    weights.append(w)
weights = np.array(weights)
weights = weights / weights.sum()

# --- Chargement des données ---
st.subheader("📊 Données du portefeuille")
with st.spinner("Téléchargement des données..."):
    try:
        returns = get_returns(tickers, period)
        st.success(f"✅ {len(returns)} jours de données chargés pour {', '.join(tickers)}")
    except Exception as e:
        st.error(f"Erreur : {e}")
        st.stop()

# --- Calcul des VaR ---
h_var = historical_var(returns, weights, confidence)
p_var = parametric_var(returns, weights, confidence)
m_var = monte_carlo_var(returns, weights, confidence)

h_var_eur = h_var * investment
p_var_eur = p_var * investment
m_var_eur = m_var * investment

# --- Affichage des VaR ---
st.subheader(f"📐 Value at Risk (confiance {int(confidence*100)}%)")
col1, col2, col3 = st.columns(3)
col1.metric("VaR Historique",    f"{h_var_eur:,.0f} €", f"{h_var*100:.2f}%")
col2.metric("VaR Paramétrique",  f"{p_var_eur:,.0f} €", f"{p_var*100:.2f}%")
col3.metric("VaR Monte Carlo",   f"{m_var_eur:,.0f} €", f"{m_var*100:.2f}%")

st.caption(f"Sur un portefeuille de {investment:,} €, la perte maximale journalière est estimée à ces montants avec {int(confidence*100)}% de confiance.")

# --- Backtesting ---
st.subheader("🔍 Backtesting Basel")
bt = backtest(returns, weights, h_var, confidence)
col1, col2, col3 = st.columns(3)
col1.metric("Violations", bt["n_violations"])
col2.metric("Taux de violation", f"{bt['violation_rate']}%")
col3.markdown(f"**Statut Basel** : {bt['zone']}")

# --- Graphique rendements + violations ---
st.subheader("📈 Rendements du portefeuille et violations de la VaR")
portfolio_returns = returns.dot(weights)

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(portfolio_returns.index, portfolio_returns * 100,
        color="#2196F3", linewidth=0.8, label="Rendement journalier")
ax.axhline(-h_var * 100, color="red", linestyle="--", linewidth=1.5,
           label=f"VaR Historique ({int(confidence*100)}%)")
violations_idx = portfolio_returns[bt["violations"]].index
ax.scatter(violations_idx, portfolio_returns[bt["violations"]] * 100,
           color="red", s=20, zorder=5, label=f"Violations ({bt['n_violations']})")
ax.set_xlabel("Date")
ax.set_ylabel("Rendement (%)")
ax.legend(fontsize=9)
ax.set_title("Rendements journaliers et violations de la VaR")
st.pyplot(fig)

# --- Distribution des rendements ---
st.subheader("📊 Distribution des rendements")
fig2, ax2 = plt.subplots(figsize=(10, 4))
ax2.hist(portfolio_returns * 100, bins=60, color="#2196F3",
         alpha=0.7, edgecolor="white", label="Rendements")
ax2.axvline(-h_var * 100, color="red",    linestyle="--", label=f"VaR Historique")
ax2.axvline(-p_var * 100, color="orange", linestyle="--", label=f"VaR Paramétrique")
ax2.axvline(-m_var * 100, color="green",  linestyle="--", label=f"VaR Monte Carlo")
ax2.set_xlabel("Rendement journalier (%)")
ax2.set_ylabel("Fréquence")
ax2.legend(fontsize=9)
ax2.set_title("Distribution des rendements et comparaison des VaR")
st.pyplot(fig2)

st.caption("Données : Yahoo Finance | Modèles : Historique, Paramétrique, Monte Carlo | Réglementation : Bâle III")