# Bengaluru Real Estate Price Prediction

A full-stack machine learning application for predicting real estate prices in Bengaluru, India. The system features a trained Random Forest model, FastAPI backend, and an interactive Streamlit dashboard with market analytics.

## Features

- **Price Prediction**: Predict property prices based on location, area, BHK, bathrooms, and year
- **Market Analytics**: View trends, distributions, and insights from historical data
- **Interactive Dashboard**: User-friendly Streamlit interface with real-time predictions
- **REST API**: FastAPI backend for programmatic access
- **Year-Aware Predictions**: Adjust predictions based on historical price trends
- **Data Visualization**: Charts showing price distributions, BHK averages, and 10-year trends

## Tech Stack

- **Machine Learning**: scikit-learn (Random Forest Regressor)
- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit
- **Database**: SQLite
- **Data Processing**: Pandas, NumPy

## Project Structure

```
.
├── api/                    # FastAPI backend
│   └── main.py            # API endpoints and logic
├── database/              # Database and data loading
│   ├── houses.db          # SQLite database (Bengaluru data)
│   ├── load_to_db.py      # Script to load data into database
│   └── fetch_from_db.py   # Fetch data for ML training
├── ml_model/              # Machine learning pipeline
│   ├── train_model.py     # Model training script
│   └── artifacts/         # Trained models and configs
│       ├── real_estate_model.pkl
│       └── columns.json
├── scripts/               # Utility scripts
├── streamlit_app.py       # Streamlit dashboard
└── requirements.txt       # Python dependencies
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd real-estate-price-prediction
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database** (if not already present)
   ```bash
   python database/load_to_db.py
   ```

4. **Train the model** (if artifacts are missing)
   ```bash
   python ml_model/train_model.py
   ```

## Usage

### Option 1: Streamlit Dashboard (Recommended)

Run the all-in-one Streamlit application:

```bash
streamlit run streamlit_app.py
```

Then open your browser to `http://localhost:8501`

### Option 2: FastAPI Backend

Run the REST API server:

```bash
python api/main.py
```

The API will be available at `http://127.0.0.1:8000`

**API Endpoints:**

- `GET /` - Health check
- `GET /locations` - Get list of available locations
- `GET /analytics` - Get market analytics data
- `POST /predict` - Predict property price

**Example prediction request:**

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "location": "whitefield",
    "total_sqft": 1200,
    "bath": 2,
    "bhk": 2,
    "year": 2024
  }'
```

**API Documentation:**

Visit `http://127.0.0.1:8000/docs` for interactive Swagger documentation.

## Model Details

- **Algorithm**: Random Forest Regressor
- **Features**: Location (one-hot encoded), Total Square Feet, Bathrooms, BHK
- **Data Processing**:
  - Outlier removal based on price per sqft
  - Location dimensionality reduction (grouping rare locations)
  - Square footage range handling (e.g., "1200-1500" → average)
- **Performance**: R² score typically > 0.80

## Data

The project uses Bengaluru house price data with the following attributes:

- Location
- Size (BHK)
- Total Square Feet
- Number of Bathrooms
- Price (in Lakhs)
- Availability Year

## Features in Detail

### Streamlit Dashboard

- **Price Prediction Form**: Input property details and get instant predictions
- **Market Snapshot**: Key metrics (dataset size, average/median prices)
- **Price Distribution**: Visualize price ranges across the market
- **BHK Analysis**: Average prices by bedroom count
- **Top Locations**: Most listed areas in the dataset
- **10-Year Trend**: Historical price changes over time

### FastAPI Backend

- CORS-enabled for frontend integration
- Year-aware predictions with historical indexing
- Comprehensive analytics endpoint
- Automatic artifact loading on startup
- Error handling and validation

## Development

### Running Both Services

To run the complete stack:

**Terminal 1 - API:**
```bash
python api/main.py
```

**Terminal 2 - Streamlit:**
```bash
streamlit run streamlit_app.py
```

### Retraining the Model

If you have new data or want to retrain:

1. Update the database with new data
2. Run the training script:
   ```bash
   python ml_model/train_model.py
   ```
3. Restart the API/Streamlit app to load new artifacts

## Requirements

- Python 3.8+
- See `requirements.txt` for package dependencies

## License

This project is open source and available for educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Dataset: Bengaluru House Price Data
- Built with FastAPI, Streamlit, and scikit-learn
