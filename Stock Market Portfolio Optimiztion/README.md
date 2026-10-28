# Stock Market Portfolio Optimization (BCA Final Year Project)

A practical project to optimize stock portfolios using Modern Portfolio Theory (Markowitz), evaluate risk-return trade-offs, and compare results with equal-weight investing.

## Features
- Historical stock price download using `yfinance`
- Daily returns and annualized risk/return calculations
- Portfolio optimization with minimum variance and maximum Sharpe ratio
- Backtesting against equal-weight benchmark
- CLI workflow and interactive Streamlit dashboard
- Automatic chart and metrics export

## Tech Stack
- Python 3.10+
- pandas, numpy, scipy
- yfinance
- matplotlib
- streamlit

## Project Structure
- `src/portfolio_opt/data_loader.py`: download and clean adjusted close prices
- `src/portfolio_opt/optimizer.py`: optimization models
- `src/portfolio_opt/backtest.py`: strategy comparison
- `src/portfolio_opt/visualization.py`: result plots
- `src/portfolio_opt/main.py`: CLI runner
- `app.py`: Streamlit web app
- `config.json`: user inputs (tickers, period, risk-free rate)

## Setup
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

## Run CLI
```bash
python -m src.portfolio_opt.main --config config.json
```

## Run Streamlit App
```bash
streamlit run app.py
```

## Output
Generated in `reports/` by CLI:
- `metrics.json`
- `cumulative_returns.png`
- `weights_comparison.png`

## Suggested Final-Year Enhancements
- Add CAPM expected returns module
- Add Black-Litterman model
- Add sector constraints and transaction cost modeling
- Add portfolio rebalancing frequency controls
