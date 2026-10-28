from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_cumulative_returns(cumulative_df: pd.DataFrame, save_path: Path) -> None:
    plt.figure(figsize=(10, 6))
    for col in cumulative_df.columns:
        plt.plot(cumulative_df.index, cumulative_df[col], label=col)
    plt.title("Cumulative Growth of 1 Unit")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()


def plot_weights(weights_df: pd.DataFrame, save_path: Path) -> None:
    ax = weights_df.plot(kind="bar", figsize=(10, 6))
    ax.set_title("Portfolio Weights by Strategy")
    ax.set_xlabel("Asset")
    ax.set_ylabel("Weight")
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
