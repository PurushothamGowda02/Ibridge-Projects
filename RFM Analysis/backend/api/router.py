"""
REST API router for the RFM Analysis backend.

Defines all /api/* endpoints using a FastAPI APIRouter.
The pre-computed RFM DataFrame is read from request.app.state.rfm_df,
which is populated once at application startup in main.py.

Endpoints
---------
GET /api/health            → {"status": "ok"}
GET /api/rfm               → full RFM records array
GET /api/segments/summary  → segment distribution with percentages
GET /api/rfm/top?n=10      → top-n customers by RFM_Score (descending)
"""

import logging
from typing import Any
import io

from fastapi import APIRouter, HTTPException, Query, Request, UploadFile, File
import pandas as pd

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/api/health", summary="Health check")
def health() -> dict[str, str]:
    """
    Health check endpoint.

    Returns
    -------
    dict
        ``{"status": "ok"}``
    """
    return {"status": "ok"}


@router.get("/api/rfm", summary="Full RFM records")
def get_rfm(request: Request) -> list[dict[str, Any]]:
    """
    Return the full RFM dataset as a JSON array.

    Each record contains: CustomerID, Recency, Frequency, Monetary,
    R_Score, F_Score, M_Score, RFM_Score, Customer_Segment.

    Returns
    -------
    list[dict]
        Array of RFM records; one element per customer.
    """
    rfm_df = request.app.state.rfm_df
    columns = [
        "CustomerID", "Recency", "Frequency", "Monetary",
        "R_Score", "F_Score", "M_Score", "RFM_Score", "Customer_Segment",
    ]
    records = rfm_df[columns].to_dict(orient="records")
    logger.info("GET /api/rfm — returning %d records.", len(records))
    return records


@router.get("/api/segments/summary", summary="Segment distribution summary")
def get_segments_summary(request: Request) -> list[dict[str, Any]]:
    """
    Return the segment distribution as a JSON array.

    Each element: segment (str), count (int), percentage (float).
    Percentages sum to 100 within floating-point tolerance.

    Returns
    -------
    list[dict]
        Array of segment summary records.
    """
    rfm_df = request.app.state.rfm_df
    total = len(rfm_df)
    counts = rfm_df["Customer_Segment"].value_counts()

    summary = []
    for segment, count in counts.items():
        summary.append({
            "segment": segment,
            "count": int(count),
            "percentage": round(count / total * 100, 2),
        })

    logger.info("GET /api/segments/summary — %d segments.", len(summary))
    return summary


@router.get("/api/rfm/top", summary="Top-N customers by RFM score")
def get_rfm_top(
    request: Request,
    n: Any = Query(default=10, description="Number of top customers to return"),
) -> list[dict[str, Any]]:
    """
    Return the top-n customers ranked by RFM_Score descending.

    Parameters
    ----------
    n : int
        Must be a positive integer. Defaults to 10.

    Returns
    -------
    list[dict]
        Array of up to n RFM records sorted by RFM_Score descending.

    Raises
    ------
    HTTPException (400)
        If n is not a positive integer.
    """
    try:
        if isinstance(n, str) and "." in n:
            raise ValueError("float string")
        n_int = int(n)
        if n_int <= 0:
            raise ValueError("non-positive")
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=400,
            detail="Invalid value for parameter 'n': must be a positive integer.",
        )

    rfm_df = request.app.state.rfm_df
    sorted_df = rfm_df.sort_values("RFM_Score", ascending=False)
    top_df = sorted_df.head(n_int)

    columns = [
        "CustomerID", "Recency", "Frequency", "Monetary",
        "R_Score", "F_Score", "M_Score", "RFM_Score", "Customer_Segment",
    ]
    records = top_df[columns].to_dict(orient="records")
    logger.info("GET /api/rfm/top?n=%d — returning %d records.", n_int, len(records))
    return records


@router.post("/api/rfm/analyze-unseen", summary="Analyze unseen dataset")
async def analyze_unseen_dataset(file: UploadFile = File(...)) -> dict[str, Any]:
    """
    Upload and analyze an unseen CSV dataset.

    Accepts a CSV file with columns: InvoiceNo, StockCode, Description,
    Quantity, InvoiceDate, UnitPrice, CustomerID, Country.

    Returns RFM analysis results for the uploaded dataset.

    Parameters
    ----------
    file : UploadFile
        CSV file to analyze.

    Returns
    -------
    dict
        Contains:
        - rfm_data: Array of RFM records
        - segments_summary: Segment distribution
        - stats: Summary statistics
        - message: Success message

    Raises
    ------
    HTTPException (400)
        If file format is invalid or required columns are missing.
    HTTPException (500)
        If processing fails.
    """
    try:
        # Read uploaded CSV
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        logger.info(f"Uploaded CSV has {len(df)} rows and columns: {df.columns.tolist()}")
        
        # Validate required columns
        required_cols = ['InvoiceNo', 'StockCode', 'Description', 'Quantity',
                        'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {', '.join(missing_cols)}. Found columns: {', '.join(df.columns.tolist())}"
            )
        
        # Import here to avoid circular imports
        from data.ingestion import clean_dataset
        from rfm.computation import compute_rfm, assign_scores, assign_segments
        
        # Parse InvoiceDate with multiple format support
        try:
            df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], infer_datetime_format=True)
        except Exception as date_error:
            logger.error(f"Date parsing error: {date_error}")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid date format in InvoiceDate column. Please use format like 'MM/DD/YYYY HH:MM' or 'YYYY-MM-DD HH:MM:SS'. Error: {str(date_error)}"
            )
        
        # Clean dataset
        original_count = len(df)
        df_clean = clean_dataset(df)
        cleaned_count = len(df_clean)
        
        logger.info(f"Cleaned dataset: {original_count} rows -> {cleaned_count} rows (removed {original_count - cleaned_count})")
        
        if len(df_clean) == 0:
            raise HTTPException(
                status_code=400,
                detail=f"No valid records after cleaning. Original rows: {original_count}. All rows were removed due to: null values in required columns (CustomerID, InvoiceDate, Quantity, UnitPrice) or non-positive amounts (Quantity × UnitPrice ≤ 0)."
            )
        
        # Compute RFM
        reference_date = df_clean['InvoiceDate'].max() + pd.Timedelta(days=1)
        rfm = compute_rfm(df_clean, reference_date)
        rfm = assign_scores(rfm)
        rfm = assign_segments(rfm)
        
        # Prepare response
        columns = [
            "CustomerID", "Recency", "Frequency", "Monetary",
            "R_Score", "F_Score", "M_Score", "RFM_Score", "Customer_Segment",
        ]
        rfm_records = rfm[columns].to_dict(orient="records")
        
        # Segment summary
        total = len(rfm)
        counts = rfm["Customer_Segment"].value_counts()
        segments_summary = [
            {
                "segment": segment,
                "count": int(count),
                "percentage": round(count / total * 100, 2),
            }
            for segment, count in counts.items()
        ]
        
        # Statistics
        stats = {
            "total_customers": len(rfm),
            "total_transactions": len(df_clean),
            "avg_recency": round(rfm['Recency'].mean(), 2),
            "avg_frequency": round(rfm['Frequency'].mean(), 2),
            "avg_monetary": round(rfm['Monetary'].mean(), 2),
            "rows_cleaned": len(df) - len(df_clean),
        }
        
        logger.info(
            "POST /api/rfm/analyze-unseen — analyzed %d customers from uploaded file.",
            len(rfm)
        )
        
        return {
            "rfm_data": rfm_records,
            "segments_summary": segments_summary,
            "stats": stats,
            "message": f"Successfully analyzed {len(rfm)} customers from uploaded dataset"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error analyzing unseen dataset: %s", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )
