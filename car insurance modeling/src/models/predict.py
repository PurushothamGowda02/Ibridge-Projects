"""Prediction module for new data."""
import pandas as pd
import joblib
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.config_loader import load_config, get_data_paths

def load_artifacts(config: dict) -> dict:
    """Load model and preprocessing artifacts.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Dictionary with model and artifacts
    """
    _, processed_path = get_data_paths(config)
    
    # Load best model (you can change this to load a specific model)
    model = joblib.load("models/xgboost.pkl")
    encoders = joblib.load(f"{processed_path}/encoders.pkl")
    scaler = joblib.load(f"{processed_path}/scaler.pkl")
    
    return {
        'model': model,
        'encoders': encoders,
        'scaler': scaler
    }

def preprocess_new_data(data: pd.DataFrame, encoders: dict, scaler, 
                       config: dict) -> pd.DataFrame:
    """Preprocess new data for prediction.
    
    Args:
        data: Raw input data
        encoders: Label encoders
        scaler: Feature scaler
        config: Configuration dictionary
        
    Returns:
        Preprocessed DataFrame
    """
    data = data.copy()
    
    # Encode categorical features
    categorical_features = config['features']['categorical_features']
    for feature in categorical_features:
        if feature in data.columns and feature in encoders:
            data[feature] = encoders[feature].transform(data[feature])
    
    # Scale numerical features
    numerical_features = config['features']['numerical_features']
    # Filter to only include features that exist in data
    numerical_features_to_scale = [f for f in numerical_features if f in data.columns]
    
    if numerical_features_to_scale:
        data[numerical_features_to_scale] = scaler.transform(data[numerical_features_to_scale])
    
    # Ensure correct column order (categorical first, then numerical)
    all_features = categorical_features + numerical_features
    # Filter to only include features that exist in data
    all_features = [f for f in all_features if f in data.columns]
    data = data[all_features]
    
    return data

def predict_premium(input_data: pd.DataFrame, config: dict = None) -> pd.DataFrame:
    """Predict insurance premium for new data.
    
    Args:
        input_data: DataFrame with input features
        config: Configuration dictionary
        
    Returns:
        DataFrame with predictions
    """
    if config is None:
        config = load_config()
    
    # Load artifacts
    artifacts = load_artifacts(config)
    model = artifacts['model']
    encoders = artifacts['encoders']
    scaler = artifacts['scaler']
    
    # Preprocess data
    processed_data = preprocess_new_data(input_data, encoders, scaler, config)
    
    # Make predictions
    predictions = model.predict(processed_data)
    
    # Add predictions to original data
    result = input_data.copy()
    result['predicted_premium'] = predictions.round(2)
    
    return result

def predict_single(age: int, gender: str, driving_experience: int,
                  vehicle_make: str, vehicle_model: str, vehicle_age: int,
                  engine_size: float, annual_mileage: int, credit_score: int,
                  previous_claims: int, region: str, education_level: str,
                  marital_status: str) -> float:
    """Predict premium for a single customer.
    
    Args:
        All customer and vehicle attributes
        
    Returns:
        Predicted premium amount
    """
    # Create DataFrame from inputs
    input_data = pd.DataFrame([{
        'age': age,
        'gender': gender,
        'driving_experience': driving_experience,
        'vehicle_make': vehicle_make,
        'vehicle_model': vehicle_model,
        'vehicle_age': vehicle_age,
        'engine_size': engine_size,
        'annual_mileage': annual_mileage,
        'credit_score': credit_score,
        'previous_claims': previous_claims,
        'region': region,
        'education_level': education_level,
        'marital_status': marital_status
    }])
    
    # Get prediction
    result = predict_premium(input_data)
    
    return result['predicted_premium'].iloc[0]

if __name__ == "__main__":
    # Example prediction
    premium = predict_single(
        age=35,
        gender='Male',
        driving_experience=15,
        vehicle_make='Toyota',
        vehicle_model='Sedan',
        vehicle_age=3,
        engine_size=2.0,
        annual_mileage=12000,
        credit_score=720,
        previous_claims=0,
        region='Suburban',
        education_level='Bachelor',
        marital_status='Married'
    )
    
    print(f"\nPredicted Premium: ${premium:.2f}")
