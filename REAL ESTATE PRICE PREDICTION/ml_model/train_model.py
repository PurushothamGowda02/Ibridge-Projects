import pandas as pd
import numpy as np
import pickle
import json
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

# Add parent directory to path to import fetch_data
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.fetch_from_db import fetch_data

def preprocess_sqft(x):
    tokens = str(x).split('-')
    if len(tokens) == 2:
        return (float(tokens[0]) + float(tokens[1])) / 2
    try:
        return float(x)
    except:
        return None

def train():
    print("Fetching data from database...")
    df = fetch_data()
    
    # 1. Cleaning
    print("Cleaning data...")
    df2 = df.drop(['area_type', 'society', 'balcony', 'availability'], axis='columns')
    df3 = df2.dropna()
    
    # 2. Feature Engineering: BHK
    df3['bhk'] = df3['size'].apply(lambda x: int(x.split(' ')[0]))
    
    # 3. Feature Engineering: total_sqft
    df4 = df3.copy()
    df4['total_sqft'] = df4['total_sqft'].apply(preprocess_sqft)
    df4 = df4.dropna(subset=['total_sqft'])
    
    # 4. Feature Engineering: Price per sqft (useful for outlier detection)
    df5 = df4.copy()
    df5['price_per_sqft'] = df5['price'] * 100000 / df5['total_sqft']
    
    # 5. Outlier Removal (Simplified)
    # Remove rows where sqft per bhk < 300
    df6 = df5[~(df5.total_sqft / df5.bhk < 300)]
    
    # Price per sqft outliers (per location)
    def remove_pps_outliers(df):
        df_out = pd.DataFrame()
        for key, subdf in df.groupby('location'):
            m = np.mean(subdf.price_per_sqft)
            st = np.std(subdf.price_per_sqft)
            reduced_df = subdf[(subdf.price_per_sqft > (m - st)) & (subdf.price_per_sqft <= (m + st))]
            df_out = pd.concat([df_out, reduced_df], ignore_index=True)
        return df_out
    
    df7 = remove_pps_outliers(df6)
    
    # 6. Location dimensionality reduction
    df7.location = df7.location.apply(lambda x: x.strip())
    location_stats = df7.groupby('location')['location'].agg('count').sort_values(ascending=False)
    location_stats_less_than_10 = location_stats[location_stats <= 10]
    df7.location = df7.location.apply(lambda x: 'other' if x in location_stats_less_than_10 else x)
    
    # 7. Final preparation for One-Hot Encoding
    dummies = pd.get_dummies(df7.location)
    df8 = pd.concat([df7, dummies.drop('other', axis='columns')], axis='columns')
    df9 = df8.drop('location', axis='columns')
    
    # 8. Training
    X = df9.drop(['price', 'size', 'price_per_sqft'], axis='columns')
    y = df9.price
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)
    
    print("Training Random Forest model...")
    rf_clf = RandomForestRegressor(n_estimators=100)
    rf_clf.fit(X_train, y_train)
    
    score = rf_clf.score(X_test, y_test)
    print(f"Model R2 Score: {score:.4f}")
    
    # 9. Saving the model
    os.makedirs('ml_model/artifacts', exist_ok=True)
    with open("ml_model/artifacts/real_estate_model.pkl", 'wb') as f:
        pickle.dump(rf_clf, f)
        
    # Save column structure
    columns = {
        'data_columns': [col.lower() for col in X.columns]
    }
    with open("ml_model/artifacts/columns.json", "w") as f:
        f.write(json.dumps(columns))
        
    print("Model and columns saved to ml_model/artifacts/.")

if __name__ == "__main__":
    train()
