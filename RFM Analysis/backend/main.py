"""
FastAPI application entry point for the RFM Analysis backend.

Usage
-----
Start the development server from the backend/ directory::

    python -m uvicorn main:app --reload

Or run this file directly::

    python main.py
"""

import logging
from contextlib import asynccontextmanager

import pandas as pd
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.router import router
from config import CORS_ORIGINS, DATASET_PATH
from data.ingestion import clean_dataset, load_dataset
from rfm.computation import assign_scores, assign_segments, compute_rfm

# Configure root logger so startup messages are visible in the console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.

    On startup:
    1. Load the raw CSV dataset from DATASET_PATH.
    2. Clean the dataset (drop nulls, derive Amount, drop Amount <= 0).
    3. Compute per-customer RFM metrics (Recency, Frequency, Monetary).
    4. Assign quantile-based R/F/M scores and composite RFM_Score.
    5. Assign customer segment labels.
    6. Store the resulting DataFrame on app.state.rfm_df.
    """
    logger.info("Starting up — loading dataset from '%s'.", DATASET_PATH)

    df = load_dataset(DATASET_PATH)
    df = clean_dataset(df)

    reference_date: pd.Timestamp = df["InvoiceDate"].max() + pd.Timedelta(days=1)
    rfm = compute_rfm(df, reference_date)
    rfm = assign_scores(rfm)
    rfm = assign_segments(rfm)

    app.state.rfm_df = rfm
    logger.info("Startup complete — %d customers loaded and segmented.", len(rfm))

    yield

    logger.info("Shutting down RFM Analysis API.")


def create_app() -> FastAPI:
    """
    Application factory.

    Creates and configures the FastAPI application:
    - Registers the API router (all /api/* endpoints).
    - Adds CORSMiddleware using CORS_ORIGINS from config.py.
    - Attaches the lifespan handler for startup data loading.

    Returns
    -------
    FastAPI
        Fully configured application instance.
    """
    app = FastAPI(
        title="RFM Analysis API",
        description="REST API for RFM customer segmentation analysis.",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Mount router; endpoints already include /api prefix
    app.include_router(router, prefix="")

    # CORS — allow the plain HTML/JS frontend to call the API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


# Module-level app instance used by uvicorn and the test suite
app = create_app()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
