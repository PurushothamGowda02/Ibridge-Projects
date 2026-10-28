# Real Estate Price Prediction - Implementation Plan

This project aims to build a full end-to-end real estate price prediction system using a real-world dataset, a database for storage, a machine learning pipeline, a FastAPI backend, and a Streamlit frontend.

## User Review Required

> [!IMPORTANT]
> - I will use the **Bengaluru House Price Data** as the dataset.
> - I will use **SQLite** as the database for simplicity of setup unless you prefer a different database like PostgreSQL or MongoDB.
> - I will implement **Random Forest** for the first iteration as it's robust and easier to tune for this specific dataset size, though XGBoost can be swapped in easily.

## Proposed Changes

### 1. Project Organization
- `data/`: Raw and processed data storage.
- `database/`: SQLite database storage and scripts.
- `ml_model/`: Scripts for cleaning, feature engineering, and training.
- `api/`: FastAPI backend implementation.
- `streamlit_app.py`: Streamlit UI for prediction and analytics.

### 2. Database & Data Setup [NEW]
- **Script**: `load_to_db.py` - Fetches the dataset and saves it to an SQLite table `houses`.
- **Script**: `fetch_from_db.py` - Reads from the database to provide a dataframe for the ML pipeline.

### 3. Data Cleaning & Feature Engineering [NEW]
- `preprocessing.py`:
    - Drop unnecessary columns (`area_type`, `availability`, etc.).
    - Handle null values.
    - Standardize `size` (BHK).
    - Convert `total_sqft` (handle ranges like '2100 - 2850').
    - Simplify `location` (Dimensionality reduction: group rare locations as 'Other').

### 4. Model Training [NEW]
- `trainer.py`:
    - Train a Random Forest (or XGBoost) Regressor.
    - Evaluate using R² score and MAE.
    - Save the model as `real_estate_model.pkl` and metadata as `columns.json`.

### 5. Backend (FastAPI) [NEW]
- `main.py`:
    - Load the model and column mapping.
    - `/predict` endpoint: Accepts location, sqft, bath, BHK and returns price.
    - `/locations` endpoint: Returns a list of available locations for the dropdown.

### 6. Frontend (Streamlit) [NEW]
- `streamlit_app.py`:
    - Input form for property details.
    - Real-time prediction display.
    - Bengaluru market analytics summary and charts.

## Open Questions

- Do you have a preference between **Random Forest** and **XGBoost**? I will default to Random Forest for its reliability in this case.
- Are there any specific features of the dataset you want highlighted (e.g., area type)?

## Verification Plan

### Automated Tests
- Run `trainer.py` and check if R² score is > 0.8.
- Test FastAPI `/predict` endpoint with sample data using manual CURL or Swagger UI.

### Manual Verification
- Verify the Streamlit UI renders properly and communicates with the backend.
- Ensure the database is created and populated correctly.
