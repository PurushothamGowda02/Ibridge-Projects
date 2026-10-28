"""Model evaluation module."""
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score
import joblib
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.config_loader import load_config, get_data_paths

def load_models() -> dict:
    """Load trained models.
    
    Returns:
        Dictionary of loaded models
    """
    models = {}
    models_dir = Path("models")
    
    for model_file in models_dir.glob("*.pkl"):
        model_name = model_file.stem
        models[model_name] = joblib.load(model_file)
    
    return models

def calculate_metrics(y_true: pd.Series, y_pred: np.ndarray) -> dict:
    """Calculate evaluation metrics.
    
    Args:
        y_true: True values
        y_pred: Predicted values
        
    Returns:
        Dictionary of metrics
    """
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    
    return {
        'mae': mae,
        'mse': mse,
        'rmse': rmse,
        'r2_score': r2
    }

def evaluate_model(model, X_test: pd.DataFrame, y_test: pd.Series, 
                  model_name: str) -> dict:
    """Evaluate a single model.
    
    Args:
        model: Trained model
        X_test: Test features
        y_test: Test target
        model_name: Name of the model
        
    Returns:
        Dictionary of evaluation results
    """
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    metrics = calculate_metrics(y_test, y_pred)
    
    print(f"\n{model_name.upper()} Results:")
    print(f"  MAE: ${metrics['mae']:.2f}")
    print(f"  RMSE: ${metrics['rmse']:.2f}")
    print(f"  R² Score: {metrics['r2_score']:.4f}")
    
    return {
        'model_name': model_name,
        'predictions': y_pred,
        **metrics
    }

def cross_validate_model(model, X: pd.DataFrame, y: pd.Series, 
                        cv_folds: int = 5) -> dict:
    """Perform cross-validation.
    
    Args:
        model: Model to validate
        X: Features
        y: Target
        cv_folds: Number of CV folds
        
    Returns:
        Dictionary of CV results
    """
    cv_scores = cross_val_score(
        model, X, y, 
        cv=cv_folds, 
        scoring='neg_mean_squared_error'
    )
    
    rmse_scores = np.sqrt(-cv_scores)
    
    return {
        'cv_rmse_mean': rmse_scores.mean(),
        'cv_rmse_std': rmse_scores.std()
    }

def evaluate_all_models(config: dict) -> pd.DataFrame:
    """Evaluate all trained models.
    
    Args:
        config: Configuration dictionary
        
    Returns:
        DataFrame with evaluation results
    """
    # Load data
    _, processed_path = get_data_paths(config)
    X_test = pd.read_csv(f"{processed_path}/X_test.csv")
    y_test = pd.read_csv(f"{processed_path}/y_test.csv").squeeze()
    
    # Load models
    models = load_models()
    
    # Evaluate each model
    results = []
    for model_name, model in models.items():
        result = evaluate_model(model, X_test, y_test, model_name)
        results.append(result)
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    results_df = results_df.drop(columns=['predictions'])
    
    # Save results
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    results_df.to_csv("reports/model_comparison.csv", index=False)
    
    print("\n" + "="*60)
    print("MODEL COMPARISON")
    print("="*60)
    print(results_df.to_string(index=False))
    
    # Find best model
    best_model = results_df.loc[results_df['r2_score'].idxmax()]
    print(f"\nBest Model: {best_model['model_name']} (R² = {best_model['r2_score']:.4f})")
    
    return results_df

if __name__ == "__main__":
    config = load_config()
    evaluate_all_models(config)
