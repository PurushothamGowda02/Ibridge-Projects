from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
import yfinance as yf

from .backtest import backtest_strategies
from .data_loader import daily_returns, download_adjusted_close
from .optimizer import equal_weights, max_sharpe_weights, min_variance_weights, portfolio_summary
from .visualization import plot_cumulative_returns, plot_weights


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def ensure_report_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def main(config_path: str) -> None:
    config = load_config(config_path)
    cache_dir = Path("data/raw/yf_cache")
    cache_dir.mkdir(parents=True, exist_ok=True)
    yf.set_tz_cache_location(str(cache_dir.resolve()))

    tickers = config["tickers"]
    start_date = config["start_date"]
    end_date = config["end_date"]
    risk_free_rate = float(config.get("risk_free_rate", 0.05))
    allow_short_selling = bool(config.get("allow_short_selling", False))

    prices = download_adjusted_close(tickers, start_date, end_date)
    if prices.shape[1] < 2:
        raise ValueError(
            f"Need at least 2 valid tickers for portfolio optimization, got {prices.shape[1]}: {list(prices.columns)}"
        )
    returns = daily_returns(prices)

    w_min_var = min_variance_weights(returns, allow_short_selling=allow_short_selling)
    w_max_sharpe = max_sharpe_weights(returns, risk_free_rate=risk_free_rate, allow_short_selling=allow_short_selling)
    w_equal = equal_weights(len(tickers))

    strategies = {
        "Equal Weight": w_equal,
        "Min Variance": w_min_var,
        "Max Sharpe": w_max_sharpe,
    }

    metrics = {
        name: portfolio_summary(weights, returns, risk_free_rate)
        for name, weights in strategies.items()
    }

    weights_df = pd.DataFrame(strategies, index=tickers)
    cumulative_df = backtest_strategies(returns, strategies)

    reports_dir = Path("reports")
    ensure_report_dir(reports_dir)

    metrics_path = reports_dir / "metrics.json"
    cumulative_plot_path = reports_dir / "cumulative_returns.png"
    weights_plot_path = reports_dir / "weights_comparison.png"

    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    plot_cumulative_returns(cumulative_df, cumulative_plot_path)
    plot_weights(weights_df, weights_plot_path)

    print("Optimization complete.")
    print(f"Saved metrics: {metrics_path}")
    print(f"Saved chart: {cumulative_plot_path}")
    print(f"Saved chart: {weights_plot_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Stock portfolio optimization runner")
    parser.add_argument("--config", default="config.json", help="Path to config JSON")
    args = parser.parse_args()
    main(args.config)
