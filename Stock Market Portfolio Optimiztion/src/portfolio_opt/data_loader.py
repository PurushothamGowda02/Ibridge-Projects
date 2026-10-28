from __future__ import annotations

import pandas as pd
import yfinance as yf


def download_adjusted_close(tickers: list[str], start_date: str, end_date: str) -> pd.DataFrame:
    """Download adjusted close prices and return a clean DataFrame."""
    # Use per-symbol history fetch for better reliability than bulk download.
    frames: list[pd.Series] = []
    failed: list[str] = []

    for ticker in tickers:
        series = None
        last_error = None
        for _ in range(3):
            try:
                data = yf.Ticker(ticker).history(
                    start=start_date,
                    end=end_date,
                    auto_adjust=True,
                )
                if data.empty:
                    continue
                if "Close" not in data.columns:
                    continue
                series = data["Close"].copy().rename(ticker)
                break
            except Exception as exc:
                last_error = exc
                continue

        if series is None:
            failed.append(ticker)
            if last_error is not None:
                print(f"Failed {ticker}: {last_error}")
        else:
            frames.append(series)

    if not frames:
        raise ValueError(
            "No valid price data downloaded. Check internet/date range, or rerun if Yahoo cache was locked."
        )

    prices = pd.concat(frames, axis=1).sort_index()
    prices = prices.dropna(how="all").ffill().dropna(how="any")

    if prices.empty:
        raise ValueError("Price data became empty after cleaning.")

    if failed:
        print(f"Skipped tickers due to download errors: {failed}")

    return prices


def daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """Calculate daily percentage returns."""
    returns = prices.pct_change().dropna(how="any")
    if returns.empty:
        raise ValueError("Returns are empty. Not enough valid price history.")
    return returns
