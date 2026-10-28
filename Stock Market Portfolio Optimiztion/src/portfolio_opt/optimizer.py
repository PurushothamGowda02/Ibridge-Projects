from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import minimize


TRADING_DAYS = 252


def annualized_portfolio_return(weights: np.ndarray, mean_daily_returns: np.ndarray) -> float:
    return float(np.dot(weights, mean_daily_returns) * TRADING_DAYS)


def annualized_portfolio_volatility(weights: np.ndarray, cov_daily: np.ndarray) -> float:
    return float(np.sqrt(weights.T @ (cov_daily * TRADING_DAYS) @ weights))


def sharpe_ratio(weights: np.ndarray, mean_daily_returns: np.ndarray, cov_daily: np.ndarray, risk_free_rate: float) -> float:
    port_ret = annualized_portfolio_return(weights, mean_daily_returns)
    port_vol = annualized_portfolio_volatility(weights, cov_daily)
    if port_vol == 0:
        return -np.inf
    return (port_ret - risk_free_rate) / port_vol


def _weight_constraints(n_assets: int) -> tuple:
    return ({"type": "eq", "fun": lambda w: np.sum(w) - 1.0},)


def _weight_bounds(n_assets: int, allow_short_selling: bool) -> tuple:
    if allow_short_selling:
        return tuple((-1.0, 1.0) for _ in range(n_assets))
    return tuple((0.0, 1.0) for _ in range(n_assets))


def min_variance_weights(returns: pd.DataFrame, allow_short_selling: bool = False) -> np.ndarray:
    n_assets = returns.shape[1]
    cov_daily = returns.cov().values
    x0 = np.full(n_assets, 1.0 / n_assets)

    result = minimize(
        fun=lambda w: annualized_portfolio_volatility(w, cov_daily),
        x0=x0,
        method="SLSQP",
        bounds=_weight_bounds(n_assets, allow_short_selling),
        constraints=_weight_constraints(n_assets),
    )

    if not result.success:
        raise RuntimeError(f"Min variance optimization failed: {result.message}")

    return result.x


def max_sharpe_weights(returns: pd.DataFrame, risk_free_rate: float, allow_short_selling: bool = False) -> np.ndarray:
    n_assets = returns.shape[1]
    mean_daily = returns.mean().values
    cov_daily = returns.cov().values
    x0 = np.full(n_assets, 1.0 / n_assets)

    result = minimize(
        fun=lambda w: -sharpe_ratio(w, mean_daily, cov_daily, risk_free_rate),
        x0=x0,
        method="SLSQP",
        bounds=_weight_bounds(n_assets, allow_short_selling),
        constraints=_weight_constraints(n_assets),
    )

    if not result.success:
        raise RuntimeError(f"Max Sharpe optimization failed: {result.message}")

    return result.x


def equal_weights(n_assets: int) -> np.ndarray:
    return np.full(n_assets, 1.0 / n_assets)


def portfolio_summary(weights: np.ndarray, returns: pd.DataFrame, risk_free_rate: float) -> dict:
    mean_daily = returns.mean().values
    cov_daily = returns.cov().values
    port_ret = annualized_portfolio_return(weights, mean_daily)
    port_vol = annualized_portfolio_volatility(weights, cov_daily)
    sr = sharpe_ratio(weights, mean_daily, cov_daily, risk_free_rate)
    return {
        "annual_return": float(port_ret),
        "annual_volatility": float(port_vol),
        "sharpe_ratio": float(sr),
    }
