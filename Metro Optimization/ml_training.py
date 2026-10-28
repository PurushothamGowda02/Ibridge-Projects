import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import os

def train_demand_model(data_path='data/passenger_data.csv', models_dir='models'):
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
        
    print(f"Loading data from {data_path}...")
    df = pd.read_csv(data_path)
    
    # Feature engineering for prediction
    # Predict 'total_traffic' using 'station_id', 'is_weekend', and 'hour'
    X = df[['station_id', 'is_weekend', 'hour']]
    y = df['total_traffic']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Random Forest Regressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    rmse = np.sqrt(mean_squared_error(y_test, predictions))
    
    print(f"Model Training Complete.")
    print(f"Mean Absolute Error: {mae:.2f}")
    print(f"Root Mean Squared Error: {rmse:.2f}")
    
    # Save model
    model_path = os.path.join(models_dir, 'demand_model.pkl')
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")
    
def optimize_schedule(predictions, base_trains=4, max_capacity=200):
    """
    Very basic rule-based schedule optimization:
    If predicted passengers > total capacity of base trains, add more trains.
    """
    optimized_schedules = []
    for pred in predictions:
        needed_capacity = pred
        trains_needed = (needed_capacity // max_capacity) + (1 if needed_capacity % max_capacity > 0 else 0)
        
        # Ensure at least base trains run
        trains_scheduled = max(int(trains_needed), base_trains)
        optimized_schedules.append({
            'predicted_demand': int(pred),
            'trains_scheduled': trains_scheduled,
            'frequency_minutes': 60 // trains_scheduled
        })
    return optimized_schedules

if __name__ == "__main__":
    train_demand_model()
