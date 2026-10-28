"""Data preprocessing module."""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from pathlib import Path
import joblib
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.config_loader import load_config, get_data_paths

def load_raw_data(config: dict) -> pd.DataFrame:
    """Load raw data from CSV.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Raw DataFrame
    """
    raw_path, _ = get_data_paths(config)
    data = pd.read_csv(raw_path)
    print(f"Loaded {len(data)} rows from {raw_path}")
    return data

def clean_data(data: pd.DataFrame) -> pd.DataFrame:
    """Clean the dataset.
    
    Args:
        data: Raw DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    # Remove duplicates
    data = data.drop_duplicates()
    
    # Handle missing values
    data = data.dropna()
    
    # Remove outliers in premium (using IQR method)
    Q1 = data['premium_amount'].quantile(0.25)
    Q3 = data['premium_amount'].quantile(0.75)
    IQR = Q3 - Q1
    data = data[
        (data['premium_amount'] >= Q1 - 1.5 * IQR) & 
        (data['premium_amount'] <= Q3 + 1.5 * IQR)
    ]
    
    print(f"After cleaning: {len(data)} rows")
    return data

def encode_features(data: pd.DataFrame, config: dict, fit: bool = True, 
                   encoders: dict = None) -> tuple:
    """Encode categorical features.
    
    Args:
        data: DataFrame to encode
        config: Configuration dictionary
        fit: Whether to fit new encoders
        encoders: Pre-fitted encoders (if fit=False)
        
    Returns:
        Tuple of (encoded_data, encoders_dict)
    """
    data = data.copy()
    categorical_features = config['features']['categorical_features']
    
    if fit:
        encoders = {}
        for feature in categorical_features:
            le = LabelEncoder()
            data[feature] = le.fit_transform(data[feature])
            encoders[feature] = le
    else:
        for feature in categorical_features:
            data[feature] = encoders[feature].transform(data[feature])
    
    return data, encoders

def scale_features(X_train: pd.DataFrame, X_test: pd.DataFrame, 
                  config: dict) -> tuple:
    """Scale numerical features.
    
    Args:
        X_train: Training features
        X_test: Test features
        config: Configuration dictionary
        
    Returns:
        Tuple of (X_train_scaled, X_test_scaled, scaler)
    """
    numerical_features = config['features']['numerical_features']
    # Filter to only include features that exist in X_train
    numerical_features = [f for f in numerical_features if f in X_train.columns]
    
    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    
    if numerical_features:
        X_train_scaled[numerical_features] = scaler.fit_transform(X_train[numerical_features])
        X_test_scaled[numerical_features] = scaler.transform(X_test[numerical_features])
    
    return X_train_scaled, X_test_scaled, scaler

def preprocess_data(config: dict) -> dict:
    """Complete preprocessing pipeline.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Dictionary containing processed data and artifacts
    """
    # Load and clean data
    data = load_raw_data(config)
    data = clean_data(data)
    
    # Encode categorical features
    data, encoders = encode_features(data, config, fit=True)
    
    # Split features and target
    target = config['features']['target']
    X = data.drop(columns=[target])
    y = data[target]
    
    # Train-test split
    test_size = config['data']['test_size']
    random_state = config['data']['random_state']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # Scale features
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test, config)
    
    # Save processed data and artifacts
    _, processed_path = get_data_paths(config)
    Path(processed_path).mkdir(parents=True, exist_ok=True)
    
    X_train_scaled.to_csv(f"{processed_path}/X_train.csv", index=False)
    X_test_scaled.to_csv(f"{processed_path}/X_test.csv", index=False)
    y_train.to_csv(f"{processed_path}/y_train.csv", index=False)
    y_test.to_csv(f"{processed_path}/y_test.csv", index=False)
    
    joblib.dump(encoders, f"{processed_path}/encoders.pkl")
    joblib.dump(scaler, f"{processed_path}/scaler.pkl")
    
    print(f"\nProcessed data saved to {processed_path}")
    print(f"Training set: {X_train_scaled.shape}")
    print(f"Test set: {X_test_scaled.shape}")
    
    return {
        'X_train': X_train_scaled,
        'X_test': X_test_scaled,
        'y_train': y_train,
        'y_test': y_test,
        'encoders': encoders,
        'scaler': scaler
    }

if __name__ == "__main__":
    config = load_config()
    preprocess_data(config)
