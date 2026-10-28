# Multivariate Weather Forecasting App

A full-stack weather forecasting application that uses Vector Autoregression (VAR) models to predict weather patterns based on historical data from Open-Meteo API.

## 🌟 Features

- **Real-time Weather Data**: Fetches current and historical weather data from Open-Meteo API
- **VAR Forecasting**: Uses Vector Autoregression models for multivariate time series forecasting
- **Interactive Dashboard**: Beautiful React-based UI with interactive charts
- **Multiple Variables**: Tracks temperature, humidity, pressure, and wind speed
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 📁 Project Structure

```
.
├── backend/              # FastAPI backend service
│   ├── main.py          # Main application file
│   └── requirements.txt # Python dependencies
├── frontend/            # React + Vite frontend
│   ├── src/            # Source files
│   ├── public/         # Static assets
│   └── package.json    # Node dependencies
└── README.md           # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Node.js 16 or higher
- npm or yarn

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd Multi-Variate-Time-Series
```

2. **Setup Backend**
```bash
cd backend
pip install -r requirements.txt
```

3. **Setup Frontend**
```bash
cd frontend
npm install
```

### Running the Application

1. **Start the Backend** (Terminal 1)
```bash
cd backend
python main.py
```
Backend will run at: http://localhost:8000

2. **Start the Frontend** (Terminal 2)
```bash
cd frontend
npm run dev
```
Frontend will run at: http://localhost:5173

3. **Open your browser** and navigate to http://localhost:5173

## 🛠️ Technologies

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Uvicorn** - Lightning-fast ASGI server
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Statsmodels** - Statistical modeling and VAR forecasting
- **Requests** - HTTP library for API calls

### Frontend
- **React 19** - UI library
- **Vite** - Next-generation frontend tooling
- **Recharts** - Composable charting library
- **Lucide React** - Beautiful icon set
- **date-fns** - Modern date utility library

## 📊 API Endpoints

- `GET /api/weather/historical?days=30` - Get historical weather data
- `GET /api/weather/forecast?steps=12` - Get VAR model forecast
- `GET /api/weather/full?days=30&forecast_days=7` - Get combined data with provider forecast

## ⚙️ Configuration

### Change Location

Edit `backend/main.py` to change the default location:

```python
LATITUDE = 19.0760   # Default: Mumbai
LONGITUDE = 72.8777
```

### Adjust Forecast Parameters

- **Training period**: Modify `past_days` parameter (default: 60 days)
- **Forecast horizon**: Modify `steps` parameter (default: 12 steps = 3 days)
- **Sampling frequency**: Data is resampled to 6-hour intervals

## 🏗️ Build for Production

### Frontend
```bash
cd frontend
npm run build
```

The production build will be in `frontend/dist/`

## 📝 Notes

- The backend must be running before starting the frontend
- Weather data is fetched from the free Open-Meteo API (no API key required)
- The VAR model is retrained on each forecast request with the latest data
- Data is resampled to 6-hour intervals for better model performance

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Weather data provided by [Open-Meteo](https://open-meteo.com/)
- Built with modern web technologies and best practices
