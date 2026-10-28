import json
import os
import pickle
import sqlite3
from datetime import datetime

import numpy as np
import pandas as pd
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Bengaluru Real Estate Predictor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None
config = None
analytics = None

MODEL_PATH = "ml_model/artifacts/real_estate_model.pkl"
CONFIG_PATH = "ml_model/artifacts/columns.json"
DB_PATH = "database/houses.db"


def preprocess_sqft(value):
    tokens = str(value).split("-")
    if len(tokens) == 2:
        try:
            return (float(tokens[0]) + float(tokens[1])) / 2
        except ValueError:
            return None
    try:
        return float(value)
    except ValueError:
        return None


def extract_availability_year(value):
    text = str(value).strip()
    if "-" not in text:
        return None
    parts = text.split("-")
    if len(parts) != 2:
        return None
    yy = parts[0]
    if not yy.isdigit() or len(yy) != 2:
        return None
    year = 2000 + int(yy)
    current_year = datetime.now().year
    if year < 2000 or year > current_year + 1:
        return None
    return year


def build_analytics():
    if not os.path.exists(DB_PATH):
        return None

    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM houses", conn)
    conn.close()

    if df.empty:
        return None

    df = df.dropna(subset=["location", "size", "total_sqft", "price"]).copy()
    df["location"] = df["location"].astype(str).str.strip()
    df["bhk"] = df["size"].astype(str).str.extract(r"(\d+)").astype(float)
    df["total_sqft"] = df["total_sqft"].apply(preprocess_sqft)
    df = df.dropna(subset=["bhk", "total_sqft"])

    if df.empty:
        return None

    top_locations = (
        df["location"]
        .value_counts()
        .head(10)
        .rename_axis("location")
        .reset_index(name="count")
    )
    bhk_distribution = (
        df.groupby(df["bhk"].astype(int))["price"]
        .mean()
        .round(2)
        .rename_axis("bhk")
        .reset_index(name="avg_price")
    )
    price_distribution = (
        pd.cut(
            df["price"],
            bins=[0, 50, 100, 150, 200, 300, float("inf")],
            labels=["0-50", "50-100", "100-150", "150-200", "200-300", "300+"],
            include_lowest=True,
        )
        .value_counts()
        .sort_index()
        .rename_axis("bucket")
        .reset_index(name="count")
    )

    trend_df = df.dropna(subset=["availability"]).copy()
    trend_df["year"] = trend_df["availability"].apply(extract_availability_year)
    trend_df = trend_df.dropna(subset=["year"])
    trend_df["year"] = trend_df["year"].astype(int)
    yearly_prices = (
        trend_df.groupby("year")["price"]
        .mean()
        .round(2)
        .sort_index()
    )
    ten_year_trend = []
    ten_year_change = None
    yearly_index = []
    if not yearly_prices.empty:
        latest_year = int(yearly_prices.index.max())
        latest_avg = float(yearly_prices.loc[latest_year])
        if latest_avg:
            yearly_index = [
                {
                    "year": int(year),
                    "index_vs_latest": round(float(price) / latest_avg, 6),
                }
                for year, price in yearly_prices.items()
            ]

        window = yearly_prices.tail(10)
        ten_year_trend = [
            {"year": int(year), "avg_price_lakhs": float(price)}
            for year, price in window.items()
        ]
        start_year = int(window.index[0])
        end_year = int(window.index[-1])
        start_price = float(window.iloc[0])
        end_price = float(window.iloc[-1])
        pct_change = ((end_price - start_price) / start_price * 100.0) if start_price else 0.0
        ten_year_change = {
            "from_year": start_year,
            "to_year": end_year,
            "from_price_lakhs": round(start_price, 2),
            "to_price_lakhs": round(end_price, 2),
            "absolute_change_lakhs": round(end_price - start_price, 2),
            "percent_change": round(pct_change, 2),
            "note": "Computed from records with month-year availability values.",
        }

    return {
        "dataset_size": int(len(df)),
        "avg_price_lakhs": round(float(df["price"].mean()), 2),
        "median_price_lakhs": round(float(df["price"].median()), 2),
        "bhk_distribution": bhk_distribution.to_dict(orient="records"),
        "top_locations": top_locations.to_dict(orient="records"),
        "price_distribution": price_distribution.to_dict(orient="records"),
        "ten_year_trend": ten_year_trend,
        "ten_year_change": ten_year_change,
        "available_years": [int(y["year"]) for y in yearly_index],
        "yearly_index": yearly_index,
    }


def load_artifacts():
    global model, config, analytics
    if os.path.exists(MODEL_PATH) and os.path.exists(CONFIG_PATH):
        with open(MODEL_PATH, "rb") as file:
            model = pickle.load(file)
        with open(CONFIG_PATH, "r") as file:
            config = json.load(file)
        analytics = build_analytics()
        print("Artifacts loaded successfully.")
    else:
        print("Warning: Artifacts not found. Please run ml_model/train_model.py first.")


@app.on_event("startup")
async def startup_event():
    load_artifacts()


class PredictionInput(BaseModel):
    location: str
    total_sqft: float
    bath: float
    bhk: int
    year: int | None = None


@app.get("/")
def read_root():
    return {"message": "Bengaluru Real Estate API is running"}


@app.get("/locations")
def get_locations():
    if config is None:
        load_artifacts()
    if config:
        return {"locations": sorted(config["data_columns"][3:])}
    raise HTTPException(status_code=503, detail="Model artifacts not yet available")


@app.get("/analytics")
def get_analytics():
    global analytics
    if analytics is None:
        load_artifacts()
    if analytics:
        return analytics
    raise HTTPException(status_code=503, detail="Analytics data not yet available")


@app.post("/predict")
def predict_price(data: PredictionInput):
    global model, config, analytics
    if model is None or config is None:
        load_artifacts()
        if model is None:
            raise HTTPException(status_code=503, detail="Model is not loaded")

    data_columns = config["data_columns"]
    location = data.location.strip().lower()
    if location not in data_columns:
        raise HTTPException(status_code=400, detail="Invalid location selected")

    input_vector = np.zeros(len(data_columns))
    input_vector[0] = data.total_sqft
    input_vector[1] = data.bath
    input_vector[2] = data.bhk
    input_vector[data_columns.index(location)] = 1

    base_prediction = float(model.predict([input_vector])[0])

    # Year-aware adjustment based on Bengaluru historical availability-year averages.
    yearly_index = analytics.get("yearly_index", []) if analytics else []
    if not yearly_index:
        prediction = base_prediction
        return {
            "prediction_lakhs": round(prediction, 2),
            "prediction_crores": round(prediction / 100.0, 2),
        }

    index_by_year = {int(item["year"]): float(item["index_vs_latest"]) for item in yearly_index}
    latest_year = max(index_by_year.keys())
    requested_year = data.year if data.year is not None else latest_year
    if requested_year not in index_by_year:
        raise HTTPException(
            status_code=400,
            detail=f"Year {requested_year} is not available. Choose from {sorted(index_by_year.keys())}.",
        )

    current_prediction = base_prediction
    selected_prediction = base_prediction * index_by_year[requested_year]
    change = current_prediction - selected_prediction
    change_pct = (change / selected_prediction * 100.0) if selected_prediction else 0.0

    return {
        "year": int(requested_year),
        "latest_year_reference": int(latest_year),
        "prediction_lakhs": round(selected_prediction, 2),
        "prediction_crores": round(selected_prediction / 100.0, 2),
        "current_prediction_lakhs": round(current_prediction, 2),
        "current_prediction_crores": round(current_prediction / 100.0, 2),
        "difference_from_current_lakhs": round(change, 2),
        "difference_from_current_percent": round(change_pct, 2),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
