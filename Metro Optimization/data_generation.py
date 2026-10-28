import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_synthetic_data(num_days=30, output_dir='data'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    start_date = datetime.now() - timedelta(days=num_days)
    
    data = []
    
    # Simulate 5 stations
    stations = [1, 2, 3, 4, 5]
    
    for day in range(num_days):
        current_date = start_date + timedelta(days=day)
        is_weekend = current_date.weekday() >= 5
        
        # Simulate hourly data
        for hour in range(6, 24):  # Metro hours 6 AM to Midnight
            for station in stations:
                # Base traffic 
                base_traffic = np.random.randint(50, 200)
                
                # Peak hours (8-10 AM, 5-7 PM)
                if (8 <= hour <= 10) or (17 <= hour <= 19):
                    multiplier = 3.0 if not is_weekend else 1.5
                else:
                    multiplier = 1.0 if not is_weekend else 0.8
                    
                # Station specific multiplier (Station 1 is busiest)
                station_multiplier = 1.5 if station == 1 else 1.0
                
                traffic = int(base_traffic * multiplier * station_multiplier)
                
                # Entries and exits roughly equal over the day, but might vary per hour
                entries = int(traffic * np.random.uniform(0.4, 0.6))
                exits = traffic - entries
                
                timestamp = current_date.replace(hour=hour, minute=0, second=0, microsecond=0)
                
                data.append({
                    'station_id': station,
                    'timestamp': timestamp,
                    'is_weekend': int(is_weekend),
                    'hour': hour,
                    'entries': entries,
                    'exits': exits,
                    'total_traffic': traffic
                })
                
    df = pd.DataFrame(data)
    
    # Save to CSV
    csv_path = os.path.join(output_dir, 'passenger_data.csv')
    df.to_csv(csv_path, index=False)
    print(f"Generated synthetic passenger data at {csv_path}")
    return df

if __name__ == "__main__":
    generate_synthetic_data()
