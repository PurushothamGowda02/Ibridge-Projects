from fastapi import APIRouter, HTTPException, Query

from api.services.analytics_service import (
    predict_winner,
    prediction_inputs,
    season_wise,
    summary,
    top_performers,
    toss_impact,
    venue_stats,
)

router = APIRouter(tags=["analytics"])


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/summary")
def get_summary():
    try:
        return summary()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/season-wise")
def get_season_wise():
    try:
        return season_wise()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/venue-stats")
def get_venue_stats():
    try:
        return venue_stats()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/toss-impact")
def get_toss_impact():
    try:
        return toss_impact()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/top-performers")
def get_top_performers(limit: int = Query(default=10, ge=3, le=30)):
    try:
        return top_performers(limit=limit)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/prediction-inputs")
def get_prediction_inputs():
    try:
        return prediction_inputs()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/predict-winner")
def get_predict_winner(
    season: str = Query(...),
    venue: str = Query(...),
    toss_winner: str = Query(...),
):
    try:
        return predict_winner(season=season, venue=venue, toss_winner=toss_winner)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
