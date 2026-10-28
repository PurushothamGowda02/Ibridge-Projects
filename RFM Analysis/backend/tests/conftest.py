"""
Shared pytest fixtures for the RFM Analysis test suite.
"""

import pandas as pd
import pytest

from data.ingestion import clean_dataset
from rfm.computation import assign_scores, assign_segments, compute_rfm


@pytest.fixture
def sample_raw_df() -> pd.DataFrame:
    """
    Small in-memory DataFrame matching the raw CSV schema.

    Includes:
    - Some rows with null CustomerID (should be dropped by clean_dataset)
    - Some rows with negative Quantity (will produce Amount <= 0, dropped)
    - Multiple invoices per customer for realistic RFM variation
    """
    data = {
        "InvoiceNo": [
            "536365", "536365", "536366", "536367", "536368",
            "536369", "536370", "536371", "536372", "536373",
            "536374", "536375",
        ],
        "StockCode": [
            "85123A", "71053", "84406B", "84029G", "84029E",
            "22752", "21730", "22633", "22632", "84879",
            "47566", "20719",
        ],
        "Description": [
            "WHITE HANGING HEART T-LIGHT HOLDER", "WHITE METAL LANTERN",
            "CREAM CUPID HEARTS COAT HANGER", "KNITTED UNION FLAG HOT WATER BOTTLE",
            "RED WOOLLY HOTTIE WHITE HEART.", "SET 7 BABUSHKA NESTING BOXES",
            "GLASS STAR FROSTED T-LIGHT HOLDER", "HAND WARMER UNION JACK",
            "HAND WARMER RED POLKA DOT", "ASSORTED COLOUR BIRD ORNAMENT",
            "PARTY BUNTING", "EDWARDIAN PARASOL BLACK",
        ],
        "Quantity": [
            6, 6, 8, 6, 6,
            2, 6, 6, 6, 32,
            -3, 4,  # negative Quantity → Amount <= 0 → should be dropped
        ],
        "InvoiceDate": pd.to_datetime([
            "2010-12-01 08:26", "2010-12-01 08:26", "2010-12-01 08:28",
            "2010-12-01 08:34", "2010-12-01 08:34",
            "2010-12-01 09:00", "2010-12-01 09:10", "2010-12-01 09:20",
            "2010-12-01 09:20", "2010-12-01 09:30",
            "2010-12-01 09:40", "2010-12-01 09:50",
        ]),
        "UnitPrice": [
            2.55, 3.39, 2.75, 3.39, 3.39,
            7.65, 4.25, 1.85, 1.85, 1.69,
            4.95, 5.00,
        ],
        "CustomerID": [
            "17850", "17850", "17850", "13047", "13047",
            None,    # null CustomerID → should be dropped
            "12583", "12583", "12583", "15100",
            "15100", "17850",
        ],
        "Country": [
            "United Kingdom", "United Kingdom", "United Kingdom",
            "United Kingdom", "United Kingdom",
            "United Kingdom",
            "France", "France", "France", "United Kingdom",
            "United Kingdom", "United Kingdom",
        ],
    }
    return pd.DataFrame(data)


@pytest.fixture
def sample_clean_df(sample_raw_df: pd.DataFrame) -> pd.DataFrame:
    """Cleaned version of sample_raw_df (null and negative rows removed, Amount derived)."""
    return clean_dataset(sample_raw_df)


@pytest.fixture
def sample_rfm_df(sample_clean_df: pd.DataFrame) -> pd.DataFrame:
    """
    Pre-computed RFM DataFrame with R_Score, F_Score, M_Score, RFM_Score,
    and Customer_Segment columns, produced by running the full pipeline on
    sample_clean_df.
    """
    reference_date = sample_clean_df["InvoiceDate"].max() + pd.Timedelta(days=1)
    rfm = compute_rfm(sample_clean_df, reference_date)
    rfm = assign_scores(rfm)
    rfm = assign_segments(rfm)
    return rfm


@pytest.fixture
def test_app(sample_rfm_df: pd.DataFrame):
    """
    FastAPI TestClient wrapping the app with sample_rfm_df injected into
    app.state.rfm_df.

    If create_app is not yet implemented in backend/main.py, this fixture
    is skipped gracefully.
    """
    try:
        from main import create_app  # noqa: PLC0415
    except (ImportError, AttributeError):
        pytest.skip("create_app not yet implemented in backend/main.py")

    try:
        from httpx import ASGITransport, AsyncClient  # noqa: F401
        from starlette.testclient import TestClient
    except ImportError:
        pytest.skip("httpx / starlette TestClient not installed")

    app = create_app()
    app.state.rfm_df = sample_rfm_df

    return TestClient(app)
