# Value at Risk — Portfolio Risk Analyzer

An interactive web application for measuring and comparing portfolio risk
using three classic VaR methodologies, built from scratch in Python with real market data.

## Overview

This project answers a fundamental question in risk management:
**what is the maximum loss a portfolio can suffer in one day?**

It downloads real stock market data, computes the VaR using three different
approaches, and backtests the model against Basel III regulatory requirements.

## Methods Implemented

### 1. Historical VaR
Uses past returns directly — no distributional assumption.
Sorts the historical losses and reads off the quantile.

### 2. Parametric VaR (Variance-Covariance)
Assumes returns follow a normal distribution:
- VaR = -(μ - z·σ)
- Where z is the confidence level quantile (e.g. z = 2.326 for 99%)

### 3. Monte Carlo VaR
Simulates 10,000 random future scenarios based on
the historical mean and volatility of the portfolio.

## Backtesting — Basel III

The model is validated using the Basel III backtesting framework:

| Violations (250 days) | Zone | Status |
|----------------------|------|--------|
| 0 – 4 | 🟢 Green | Basel compliant |
| 5 – 9 | 🟡 Yellow | Warning |
| 10+ | 🔴 Red | Non-compliant |

## Visualizations

- Daily portfolio returns with VaR threshold and violation markers
- Distribution of returns with all three VaR estimates overlaid
- Real-time recalculation when portfolio weights or confidence level change

## Getting Started
```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Tech Stack

| Tool | Usage |
|------|-------|
| Python 3.11 | Core language |
| yfinance | Real-time market data (Yahoo Finance) |
| NumPy / SciPy | Statistical computations |
| Pandas | Data manipulation |
| Matplotlib | Visualizations |
| Streamlit | Interactive web interface |

## References

- Basel Committee on Banking Supervision (1996). *Amendment to the Capital Accord to Incorporate Market Risks*
- J.P. Morgan (1996). *RiskMetrics Technical Document*
- Hull, J. (2018). *Options, Futures, and Other Derivatives*. Chapter on VaR.
