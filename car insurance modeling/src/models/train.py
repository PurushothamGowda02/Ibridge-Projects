"""Model training module."""
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
import joblib
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.config_loader import load_config, get_data_paths

def load_processed_data(config: dict) -> dict:
    """Load preprocessed data.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Dictionary with train/test data
    """
    _, processed_path = get_data_paths(config)
    
    X_train = pd.read_csv(f"{processed_path}/X_train.csv")
    X_test = pd.read_csv(f"{processed_path}/X_test.csv")
    y_train = pd.read_csv(f"{processed_path}/y_train.csv").squeeze()
    y_test = pd.read_csv(f"{processed_path}/y_test.csv").squeeze()
    
    return {
        'X_train': X_train,
        'X_test': X_test,
        'y_train': y_train,
        'y_test': y_test
    }

def train_linear_regression(X_train: pd.DataFrame, y_train: pd.Series, 
                           config: dict) -> LinearRegression:
    """Train Linear Regression model.
    
    Args:
        X_train: Training features
        y_train: Training target
        config: Configuration dictionary
        
    Returns:
        Trained model
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    print("Linear Regression trained")
    return model

def train_random_forest(X_train: pd.DataFrame, y_train: pd.Series, 
                       config: dict) -> RandomForestRegressor:
    """Train Random Forest model.
    
    Args:
        X_train: Training features
        y_train: Training target
        config: Configuration dictionary
        
    Returns:
        Trained model
    """
    model_config = config['models']['random_forest']
    model = RandomForestRegressor(
        n_estimators=model_config['n_estimators'],
        max_depth=model_config['max_depth'],
        random_state=model_config['random_state'],
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    print("Random Forest trained")
    return model

def train_xgboost(X_train: pd.DataFrame, y_train: pd.Series, 
                 config: dict) -> xgb.XGBRegressor:
    """Train XGBoost model.
    
    Args:
        X_train: Training features
        y_train: Training target
        config: Configuration dictionary
        
    Returns:
        Trained model
    """
    model_config = config['models']['xgboost']
    model = xgb.XGBRegressor(
        n_estimators=model_config['n_estimators'],
        max_depth=model_config['max_depth'],
        learning_rate=model_config['learning_rate'],
        random_state=model_config['random_state']
    )
    model.fit(X_train, y_train)
    print("XGBoost trained")
    return model

def train_all_models(config: dict) -> dict:
    """Train all models specified in config.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        Dictionary of trained models
    """
    # Load data
    data = load_processed_data(config)
    X_train = data['X_train']
    y_train = data['y_train']
    
    # Train models
    models = {}
    
    print("\nTraining models...")
    models['linear_regression'] = train_linear_regression(X_train, y_train, config)
    models['random_forest'] = train_random_forest(X_train, y_train, config)
    models['xgboost'] = train_xgboost(X_train, y_train, config)
    
    # Save models
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    for name, model in models.items():
        joblib.dump(model, f"models/{name}.pkl")
        print(f"Saved {name} to models/{name}.pkl")
    
    return models

if __name__ == "__main__":
    config = load_config()
    train_all_models(config)
