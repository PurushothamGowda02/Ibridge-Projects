"""
RFM computation module for the RFM Analysis backend.

Provides three public functions that form the core analytical pipeline:
- compute_rfm:     Aggregate line-item data into per-customer RFM metrics.
- assign_scores:   Assign quantile-based scores (1–5) for R, F, and M.
- assign_segments: Map score combinations to human-readable segment labels.
"""

import logging

import pandas as pd

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Segment rules: evaluated in priority order; first match wins.
# Each rule is a tuple of (label, condition_callable).
# The callable receives the rfm DataFrame and returns a boolean Series.
# ---------------------------------------------------------------------------
_SEGMENT_RULES = [
    ("Champions",           lambda df: (df["R_Score"] >= 4) & (df["F_Score"] >= 4)),
    ("Loyal Customers",     lambda df: (df["F_Score"] >= 4) & (df["R_Score"] >= 2)),
    ("Potential Loyalists", lambda df: (df["R_Score"] >= 3) & (df["F_Score"] >= 2)),
    ("New Customers",       lambda df: (df["R_Score"] >= 4) & (df["F_Score"] == 1)),
    ("At Risk",             lambda df: (df["R_Score"] <= 2) & (df["F_Score"] >= 3)),
    ("Lost",                lambda df: (df["R_Score"] <= 2) & (df["F_Score"] <= 2)),
    ("Others",              lambda df: pd.Series(True, index=df.index)),  # catch-all
]

_VALID_SEGMENTS = frozenset(label for label, _ in _SEGMENT_RULES)


def compute_rfm(df: pd.DataFrame, reference_date: pd.Timestamp) -> pd.DataFrame:
    """
    Aggregate cleaned line-item data into per-customer RFM metrics.

    For each unique ``CustomerID`` the function computes:

    * **Recency** – number of days between the customer's most recent
      ``InvoiceDate`` and *reference_date*.  Lower values indicate more
      recent activity.
    * **Frequency** – count of distinct ``InvoiceNo`` values, representing
      the number of separate purchase transactions.
    * **Monetary** – total spend, calculated as the sum of the ``Amount``
      column across all line items for that customer.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataframe produced by :func:`data.ingestion.clean_dataset`.
        Must contain columns: ``CustomerID``, ``InvoiceDate``, ``InvoiceNo``,
        ``Amount``.
    reference_date : pd.Timestamp
        The date used as "today" for Recency calculation.  Typically set to
        one day after the latest ``InvoiceDate`` in the dataset so that the
        most recent customer has Recency = 1 rather than 0.

    Returns
    -------
    pd.DataFrame
        One row per ``CustomerID`` with columns:
        ``CustomerID``, ``Recency`` (int), ``Frequency`` (int),
        ``Monetary`` (float).  Index is reset to a default RangeIndex.

    Notes
    -----
    ``CustomerID`` is cast to ``str`` before grouping so that numeric IDs
    read from CSV (e.g. ``12345.0``) are normalised to plain strings.
    """
    df = df.copy()
    df["CustomerID"] = df["CustomerID"].astype(str)

    rfm = (
        df.groupby("CustomerID")
        .agg(
            Recency=("InvoiceDate", lambda x: (reference_date - x.max()).days),
            Frequency=("InvoiceNo", "nunique"),
            Monetary=("Amount", "sum"),
        )
        .reset_index()
    )

    # Ensure integer types for Recency and Frequency
    rfm["Recency"] = rfm["Recency"].astype(int)
    rfm["Frequency"] = rfm["Frequency"].astype(int)

    logger.info(
        "compute_rfm: aggregated %d customers from %d line items (reference_date=%s).",
        len(rfm),
        len(df),
        reference_date.date(),
    )
    return rfm


def assign_scores(rfm: pd.DataFrame) -> pd.DataFrame:
    """
    Assign R_Score, F_Score, and M_Score (each in range [1, 5]) using
    quantile binning, then derive a composite RFM_Score string.

    Scoring convention (5 = most favourable):

    * **R_Score** – *inverted*: a customer with lower Recency (purchased more
      recently) receives a higher score.  Achieved by negating Recency before
      binning.
    * **F_Score** – higher Frequency → higher score.
    * **M_Score** – higher Monetary → higher score.

    Quantile binning uses :func:`pandas.qcut` with ``q=5`` bins.  When
    duplicate bin edges arise (common with low-cardinality data), the
    ``duplicates="drop"`` option is used so that fewer than 5 bins may be
    produced.  Any ``NaN`` scores that result are filled with ``1`` (the
    lowest score), ensuring every customer receives a valid integer score.

    The composite ``RFM_Score`` is the string concatenation of the three
    integer scores, e.g. ``"455"``.

    Parameters
    ----------
    rfm : pd.DataFrame
        Dataframe with at minimum the columns ``Recency``, ``Frequency``,
        and ``Monetary``, as returned by :func:`compute_rfm`.

    Returns
    -------
    pd.DataFrame
        The input dataframe with four new columns appended:
        ``R_Score`` (int), ``F_Score`` (int), ``M_Score`` (int),
        ``RFM_Score`` (str).

    Notes
    -----
    When the dataset contains very few distinct values in a metric column,
    ``pd.qcut`` may produce fewer than 5 bins even with
    ``duplicates="drop"``.  The resulting labels are still integers in
    [1, 5] because NaN values are filled with 1 and the bin labels are
    mapped to the range [1, number_of_bins].
    """
    rfm = rfm.copy()

    def _qcut_score(series: pd.Series, invert: bool = False) -> pd.Series:
        """Return integer scores 1–5 via quantile binning."""
        values = -series if invert else series
        # pd.qcut returns category codes 0-based; add 1 to shift to [1, 5]
        cut = pd.qcut(values, q=5, labels=False, duplicates="drop")
        # cut is 0-indexed; shift to 1-indexed
        score = cut + 1
        # Fill NaN (from duplicate edges) with 1 (lowest score)
        score = score.fillna(1).astype(int)
        return score

    rfm["R_Score"] = _qcut_score(rfm["Recency"], invert=True)
    rfm["F_Score"] = _qcut_score(rfm["Frequency"])
    rfm["M_Score"] = _qcut_score(rfm["Monetary"])

    rfm["RFM_Score"] = (
        rfm["R_Score"].astype(str)
        + rfm["F_Score"].astype(str)
        + rfm["M_Score"].astype(str)
    )

    logger.info(
        "assign_scores: scored %d customers; score distribution — "
        "R: %s, F: %s, M: %s.",
        len(rfm),
        rfm["R_Score"].value_counts().to_dict(),
        rfm["F_Score"].value_counts().to_dict(),
        rfm["M_Score"].value_counts().to_dict(),
    )
    return rfm


def assign_segments(rfm: pd.DataFrame) -> pd.DataFrame:
    """
    Map each customer's R_Score and F_Score to a human-readable segment label.

    Segments are assigned using a priority-ordered rule list.  The first rule
    whose condition is satisfied by a customer's scores determines that
    customer's segment.  The final rule (``"Others"``) is a catch-all that
    matches every remaining customer, guaranteeing that no customer is left
    without a segment.

    Priority order and rules
    ------------------------
    1. **Champions**           – R_Score ≥ 4 AND F_Score ≥ 4
    2. **Loyal Customers**     – F_Score ≥ 4 AND R_Score ≥ 2
    3. **Potential Loyalists** – R_Score ≥ 3 AND F_Score ≥ 2
    4. **New Customers**       – R_Score ≥ 4 AND F_Score == 1
    5. **At Risk**             – R_Score ≤ 2 AND F_Score ≥ 3
    6. **Lost**                – R_Score ≤ 2 AND F_Score ≤ 2
    7. **Others**              – all remaining customers

    Parameters
    ----------
    rfm : pd.DataFrame
        Dataframe with at minimum the columns ``R_Score`` and ``F_Score``,
        as returned by :func:`assign_scores`.

    Returns
    -------
    pd.DataFrame
        The input dataframe with one new column appended:
        ``Customer_Segment`` (str).  Every value is a non-null member of
        ``{"Champions", "Loyal Customers", "Potential Loyalists",
        "New Customers", "At Risk", "Lost", "Others"}``.

    Notes
    -----
    The priority ordering matters: for example, a customer with R_Score=5
    and F_Score=5 satisfies both the "Champions" and "Loyal Customers" rules,
    but is assigned "Champions" because that rule is evaluated first.
    """
    rfm = rfm.copy()
    rfm["Customer_Segment"] = None

    unassigned = pd.Series(True, index=rfm.index)

    for label, condition in _SEGMENT_RULES:
        mask = unassigned & condition(rfm)
        rfm.loc[mask, "Customer_Segment"] = label
        unassigned = unassigned & ~mask

    # Sanity check: every customer must have a segment
    null_count = rfm["Customer_Segment"].isna().sum()
    if null_count > 0:  # pragma: no cover
        logger.error(
            "assign_segments: %d customer(s) were not assigned a segment. "
            "Defaulting to 'Others'.",
            null_count,
        )
        rfm["Customer_Segment"] = rfm["Customer_Segment"].fillna("Others")

    segment_counts = rfm["Customer_Segment"].value_counts().to_dict()
    logger.info("assign_segments: segment distribution — %s.", segment_counts)

    return rfm
