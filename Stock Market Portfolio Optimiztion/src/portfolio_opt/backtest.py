from __future__ import annotations

import pandas as pd
import numpy as np


def portfolio_daily_returns(asset_returns: pd.DataFrame, weights: np.ndarray) -> pd.Series:
    return asset_returns @ weights


def cumulative_growth(daily_returns: pd.Series) -> pd.Series:
    return (1 + daily_returns).cumprod()


def backtest_strategies(asset_returns: pd.DataFrame, strategy_weights: dict[str, np.ndarray]) -> pd.DataFrame:
    series = {}
    for name, weights in strategy_weights.items():
        sret = portfolio_daily_returns(asset_returns, weights)
        series[name] = cumulative_growth(sret)
    return pd.DataFrame(series)
