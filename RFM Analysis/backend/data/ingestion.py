"""
Data ingestion module for the RFM Analysis backend.

Provides two public functions:
- load_dataset: reads the raw CSV from disk into a pandas DataFrame.
- clean_dataset: removes invalid rows and derives the Amount column.
"""

import logging
import os

import pandas as pd

logger = logging.getLogger(__name__)


def load_dataset(filepath: str) -> pd.DataFrame:
    """
    Load the raw CSV dataset from the given filepath.

    Reads the file with ``pd.read_csv``, parsing the ``InvoiceDate`` column
    as a datetime.  Logs the filepath and the number of rows loaded at INFO
    level.

    Parameters
    ----------
    filepath : str
        Absolute or relative path to the CSV file.

    Returns
    -------
    pd.DataFrame
        Raw dataframe with all original columns.  ``InvoiceDate`` is parsed
        as ``datetime64``.

    Raises
    ------
    FileNotFoundError
        If no file exists at *filepath*.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"Dataset file not found: '{filepath}'. "
            "Please check the DATASET_PATH setting and ensure the CSV file is present."
        )

    df = pd.read_csv(filepath, parse_dates=["InvoiceDate"])
    logger.info("Loaded dataset from '%s' — %d rows.", filepath, len(df))
    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the raw dataset by removing invalid rows and deriving Amount.

    Rules applied in order:

    1. Drop rows where any of ``CustomerID``, ``InvoiceDate``, ``Quantity``,
       or ``UnitPrice`` is null.  The count of dropped rows is logged at
       WARNING level.
    2. Derive ``Amount = Quantity × UnitPrice`` and add it as a new column.
    3. Drop rows where ``Amount <= 0`` (returns, cancellations, free items).
       The count of dropped rows is logged at WARNING level.

    Parameters
    ----------
    df : pd.DataFrame
        Raw dataframe as returned by :func:`load_dataset`.

    Returns
    -------
    pd.DataFrame
        Cleaned dataframe with an additional ``Amount`` column.  The returned
        dataframe has a reset index.
    """
    required_cols = ["CustomerID", "InvoiceDate", "Quantity", "UnitPrice"]

    # Step 1: drop rows with nulls in required columns
    before_null_drop = len(df)
    df = df.dropna(subset=required_cols)
    null_dropped = before_null_drop - len(df)
    if null_dropped > 0:
        logger.warning(
            "Dropped %d row(s) with null values in required columns %s.",
            null_dropped,
            required_cols,
        )

    # Step 2: derive Amount
    df = df.copy()
    df["Amount"] = df["Quantity"] * df["UnitPrice"]

    # Step 3: drop rows where Amount <= 0
    before_amount_drop = len(df)
    df = df[df["Amount"] > 0]
    amount_dropped = before_amount_drop - len(df)
    if amount_dropped > 0:
        logger.warning(
            "Dropped %d row(s) where Amount <= 0 (returns / cancellations / free items).",
            amount_dropped,
        )

    return df.reset_index(drop=True)
