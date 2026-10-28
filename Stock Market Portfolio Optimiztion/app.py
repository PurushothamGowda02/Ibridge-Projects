from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st
import yfinance as yf

from src.portfolio_opt.backtest import backtest_strategies
from src.portfolio_opt.data_loader import daily_returns, download_adjusted_close
from src.portfolio_opt.optimizer import equal_weights, max_sharpe_weights, min_variance_weights, portfolio_summary


st.set_page_config(page_title="Portfolio Optimizer", page_icon="📈", layout="wide")


def _format_pct(value: float) -> str:
    return f"{value * 100:.2f}%"


def _prepare_cache() -> None:
    cache_dir = Path("data/raw/yf_cache")
    cache_dir.mkdir(parents=True, exist_ok=True)
    yf.set_tz_cache_location(str(cache_dir.resolve()))


def _validate_tickers(raw_tickers: str) -> list[str]:
    tickers = [t.strip().upper() for t in raw_tickers.split(",") if t.strip()]
    unique_tickers = list(dict.fromkeys(tickers))
    if len(unique_tickers) < 2:
        raise ValueError("Enter at least 2 tickers, separated by commas.")
    return unique_tickers


def run_optimization(
    tickers: list[str],
    start_date: str,
    end_date: str,
    risk_free_rate: float,
    allow_short_selling: bool,
) -> tuple[pd.DataFrame, pd.DataFrame, dict, pd.DataFrame, pd.DataFrame]:
    _prepare_cache()

    prices = download_adjusted_close(tickers, start_date, end_date)
    if prices.shape[1] < 2:
        raise ValueError(
            f"Need at least 2 valid tickers for optimization, got {prices.shape[1]}: {list(prices.columns)}"
        )

    returns = daily_returns(prices)

    active_tickers = list(prices.columns)
    w_equal = equal_weights(len(active_tickers))
    w_min_var = min_variance_weights(returns, allow_short_selling=allow_short_selling)
    w_max_sharpe = max_sharpe_weights(
        returns,
        risk_free_rate=risk_free_rate,
        allow_short_selling=allow_short_selling,
    )

    strategies = {
        "Equal Weight": w_equal,
        "Min Variance": w_min_var,
        "Max Sharpe": w_max_sharpe,
    }

    metrics = {
        name: portfolio_summary(weights, returns, risk_free_rate)
        for name, weights in strategies.items()
    }
    weights_df = pd.DataFrame(strategies, index=active_tickers)
    cumulative_df = backtest_strategies(returns, strategies)
    return prices, returns, metrics, weights_df, cumulative_df


def main() -> None:
    st.title("Stock Market Portfolio Optimization")
    st.caption("BCA Final Year Project | Markowitz Optimization + Backtesting")

    with st.sidebar:
        st.header("Inputs")
        raw_tickers = st.text_area(
            "Tickers (comma-separated)",
            value="RELIANCE.NS, TCS.NS, INFY.NS, HDFCBANK.NS, ITC.NS",
            height=100,
        )
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start date", value=pd.Timestamp("2020-01-01").date())
        with col2:
            end_date = st.date_input("End date", value=pd.Timestamp("2025-12-31").date())

        risk_free_rate = st.number_input("Risk-free rate (annual)", min_value=0.0, max_value=1.0, value=0.06, step=0.01)
        allow_short_selling = st.checkbox("Allow short selling", value=False)
        run = st.button("Run Optimization", type="primary", use_container_width=True)

    if not run:
        st.info("Set your inputs in the sidebar and click Run Optimization.")
        return

    try:
        tickers = _validate_tickers(raw_tickers)
        if start_date >= end_date:
            raise ValueError("Start date must be before end date.")

        prices, returns, metrics, weights_df, cumulative_df = run_optimization(
            tickers=tickers,
            start_date=str(start_date),
            end_date=str(end_date),
            risk_free_rate=float(risk_free_rate),
            allow_short_selling=allow_short_selling,
        )
    except Exception as exc:
        st.error(str(exc))
        return

    st.success(f"Downloaded data for {prices.shape[1]} tickers and {prices.shape[0]} trading days.")

    metric_cols = st.columns(3)
    labels = ["Equal Weight", "Min Variance", "Max Sharpe"]
    for idx, label in enumerate(labels):
        metric_cols[idx].metric(f"{label} Return", _format_pct(metrics[label]["annual_return"]))
        metric_cols[idx].metric(f"{label} Volatility", _format_pct(metrics[label]["annual_volatility"]))
        metric_cols[idx].metric(f"{label} Sharpe", f"{metrics[label]['sharpe_ratio']:.3f}")

    st.subheader("Portfolio Weights")
    st.dataframe(weights_df.style.format("{:.4f}"), use_container_width=True)
    st.bar_chart(weights_df)

    st.subheader("Backtest: Cumulative Growth")
    st.line_chart(cumulative_df)

    st.subheader("Raw Price Data (tail)")
    st.dataframe(prices.tail(10), use_container_width=True)

    metrics_json = json.dumps(metrics, indent=2)
    st.download_button(
        label="Download Metrics JSON",
        data=metrics_json,
        file_name="metrics.json",
        mime="application/json",
    )


if __name__ == "__main__":
    main()
