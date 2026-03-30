import numpy as np
import pandas as pd
import yfinance as yf
from scipy.stats import norm

def get_returns(tickers, period="2y"):
    """
    Télécharge les prix historiques et calcule les rendements journaliers.
    tickers : liste de symboles boursiers ex: ["AAPL", "BNP.PA", "TTE.PA"]
    period  : période historique ("1y", "2y", "5y")
    """
    data = yf.download(tickers, period=period, auto_adjust=True, progress=False)["Close"]
    returns = data.pct_change().dropna()
    return returns

def historical_var(returns, weights, confidence=0.99):
    """
    VaR Historique — pas d'hypothèse sur la distribution.
    On trie les pertes passées et on prend le quantile.
    """
    portfolio_returns = returns.dot(weights)
    var = -np.percentile(portfolio_returns, (1 - confidence) * 100)
    return var

def parametric_var(returns, weights, confidence=0.99):
    """
    VaR Paramétrique — suppose que les rendements suivent une loi normale.
    VaR = mu - z * sigma
    """
    portfolio_returns = returns.dot(weights)
    mu    = portfolio_returns.mean()
    sigma = portfolio_returns.std()
    z     = norm.ppf(confidence)
    var   = -(mu - z * sigma)
    return var

def monte_carlo_var(returns, weights, confidence=0.99, n_simulations=10000):
    """
    VaR Monte Carlo — simule 10 000 scénarios futurs.
    Basé sur la matrice de covariance historique (corrélations réelles).
    """
    portfolio_returns = returns.dot(weights)
    mu    = portfolio_returns.mean()
    sigma = portfolio_returns.std()
    simulated = np.random.normal(mu, sigma, n_simulations)
    var = -np.percentile(simulated, (1 - confidence) * 100)
    return var

def backtest(returns, weights, var, confidence=0.99):
    """
    Backtesting Basel — compte les violations de la VaR.
    Une violation = perte réelle > VaR estimée.
    Règle Basel : max 4 violations sur 250 jours (zone verte).
    """
    portfolio_returns = returns.dot(weights)
    violations = portfolio_returns < -var
    n_violations = violations.sum()
    violation_rate = violations.mean()

    if n_violations <= 4:
        zone = "🟢 Green zone (Basel compliant)"
    elif n_violations <= 9:
        zone = "🟡 Yellow zone (Basel warning)"
    else:
        zone = "🔴 Red zone (Basel non-compliant)"

    return {
        "n_violations": int(n_violations),
        "violation_rate": round(float(violation_rate) * 100, 2),
        "zone": zone,
        "violations": violations
    }