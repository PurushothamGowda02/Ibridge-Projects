from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import pandas as pd
import numpy as np
from statsmodels.tsa.api import VAR

app = FastAPI(title="Multivariate Weather Forecasting API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration for Open-Meteo
LATITUDE = 19.0760  # Default: Mumbai
LONGITUDE = 72.8777
VARIABLES = ["temperature_2m", "relative_humidity_2m", "surface_pressure", "wind_speed_10m"]

def _format_weather_records(df, record_type=None):
    result = []
    for index, row in df.iterrows():
        record = {"time": index.strftime("%Y-%m-%d %H:%M")}
        if record_type:
            record["type"] = record_type(index)
        record.update(row.to_dict())
        result.append(record)
    return result

def _weather_frame_from_payload(data):
    hourly = data.get("hourly", {})
    if not hourly:
        raise Exception("No hourly data returned from Open-Meteo")

    df = pd.DataFrame(hourly)
    df["time"] = pd.to_datetime(df["time"])
    df.set_index("time", inplace=True)
    df.dropna(inplace=True)
    return df

def _append_current_observation(df, data):
    current = data.get("current")
    if not current:
        return df

    current_time = current.get("time")
    if not current_time:
        return df

    current_values = {
        variable: current.get(variable)
        for variable in VARIABLES
        if current.get(variable) is not None
    }
    if len(current_values) != len(VARIABLES):
        return df

    current_row = pd.DataFrame(
        [current_values],
        index=[pd.to_datetime(current_time)]
    )
    return pd.concat([df, current_row]).sort_index().loc[lambda frame: ~frame.index.duplicated(keep="last")]

def fetch_open_meteo_data(past_days=90, forecast_days=0, include_current=False):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "hourly": ",".join(VARIABLES),
        "past_days": past_days,
        "forecast_days": forecast_days,
        "timezone": "auto"
    }
    if include_current:
        params["current"] = ",".join(VARIABLES)
    
    response = requests.get(url, params=params, timeout=15)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data from Open-Meteo: {response.text}")

    data = response.json()
    df = _weather_frame_from_payload(data)
    if include_current:
        df = _append_current_observation(df, data)
    return data, df

def fetch_weather_data(past_days=90):
    _, df = fetch_open_meteo_data(past_days=past_days)
    return df

@app.get("/api/weather/historical")
def get_historical_data(days: int = 30):
    """Returns historical weather data for visualization."""
    try:
        df = fetch_weather_data(past_days=days)
        # Resample to daily average to reduce data points for UI if needed, 
        # but let's keep hourly or resample to 6-hourly to keep things clean.
        df_resampled = df.resample("6h").mean().dropna()
        
        return {"data": _format_weather_records(df_resampled)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/weather/full")
def get_full_weather_data(days: int = 30, forecast_days: int = 7):
    """
    Returns the full Open-Meteo series: recent past hours, latest current
    observation, and provider forecast hours. This is separate from the VAR
    endpoint so provider forecast values are not used as model training data.
    """
    try:
        payload, df = fetch_open_meteo_data(
            past_days=days,
            forecast_days=forecast_days,
            include_current=True
        )
        current_time = pd.to_datetime(payload.get("current", {}).get("time"))

        def classify_record(index):
            if pd.isna(current_time):
                return "weather"
            if index < current_time:
                return "historical"
            if index == current_time:
                return "current"
            return "provider_forecast"

        df_resampled = df.resample("6h").mean().dropna()
        return {
            "data": _format_weather_records(df_resampled, classify_record),
            "current": payload.get("current"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/weather/forecast")
def get_weather_forecast(steps: int = 12):
    """
    Trains a VAR model on the recent historical data and predicts the next 'steps'.
    If we resample to 6H, 12 steps = 3 days ahead forecast.
    """
    try:
        # Fetch longer history for training
        df = fetch_weather_data(past_days=60)
        df_resampled = df.resample("6h").mean().dropna()
        
        if df_resampled.empty:
            raise Exception("Processed dataframe is empty.")
            
        # Ensure stationarity by differencing (simplified approach for VAR)
        # In a robust production app, we'd check for stationarity and determine optimal lag
        df_diff = df_resampled.diff().dropna()
        
        # Fit VAR model
        model = VAR(df_diff)
        # Using selected lag order (e.g., 4 = 1 day of 6h intervals)
        results = model.fit(4) 
        
        # Forecast
        lag_order = results.k_ar
        forecast_input = df_diff.values[-lag_order:]
        forecast_diff = results.forecast(y=forecast_input, steps=steps)
        
        # Reconstruct forecast (reverse differencing)
        forecast_values = []
        last_val = df_resampled.iloc[-1].values
        
        for i in range(steps):
            next_val = last_val + forecast_diff[i]
            forecast_values.append(next_val)
            last_val = next_val
            
        # Create forecast DataFrame
        last_time = df_resampled.index[-1]
        forecast_times = pd.date_range(start=last_time, periods=steps+1, freq="6h")[1:]
        
        df_forecast = pd.DataFrame(forecast_values, index=forecast_times, columns=df_resampled.columns)
        
        return {"forecast": _format_weather_records(df_forecast)}
        
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
