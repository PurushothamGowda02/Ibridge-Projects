# Multivariate Weather Forecasting App

A full-stack weather forecasting application that uses Vector Autoregression (VAR) models to predict weather patterns based on historical data from Open-Meteo API.

## Project Structure

- **backend**: FastAPI service that fetches Open-Meteo weather data and runs the VAR forecast model
- **frontend**: React + Vite dashboard that displays historical and forecast weather series with interactive charts

## Prerequisites

- Python 3.13+ (or Python 3.10+)
- Node.js 16+ and npm
- Internet connection (for fetching weather data)

## Setup & Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. (Optional) Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install npm dependencies:
```bash
npm install
```

## Running the Application

### Start the Backend

From the `backend` directory:

```bash
python main.py
```

The backend will start at: **http://localhost:8000**

API endpoints:
- `GET /api/weather/historical?days=14` - Historical weather data
- `GET /api/weather/forecast?steps=12` - VAR model forecast
- `GET /api/weather/full?days=14&forecast_days=7` - Combined historical, current, and provider forecast

### Start the Frontend

From the `frontend` directory (in a separate terminal):

```bash
npm run dev
```

The frontend will start at: **http://localhost:5173**

## Usage

1. Start the backend server first
2. Start the frontend development server
3. Open http://localhost:5173 in your browser
4. The dashboard will display:
   - Historical weather data (temperature, humidity, pressure, wind speed)
   - VAR model forecasts
   - Interactive charts powered by Recharts

## Build for Production

### Frontend Build

```bash
cd frontend
npm run build
```

The production build will be created in the `frontend/dist` directory.

## Technologies Used

### Backend
- FastAPI - Modern Python web framework
- Uvicorn - ASGI server
- Pandas - Data manipulation
- NumPy - Numerical computing
- Statsmodels - VAR time series forecasting
- Requests - HTTP client for Open-Meteo API

### Frontend
- React 19 - UI library
- Vite - Build tool and dev server
- Recharts - Charting library
- Lucide React - Icon library
- date-fns - Date utilities

## API Configuration

The backend is configured to fetch weather data for Mumbai, India by default:
- Latitude: 19.0760
- Longitude: 72.8777

To change the location, edit the `LATITUDE` and `LONGITUDE` constants in `backend/main.py`.

## Notes

- The backend must be running before opening the frontend
- The frontend expects the API at `http://localhost:8000/api`
- Weather data is fetched from the free Open-Meteo API
- The VAR model is trained on 60 days of historical data by default
