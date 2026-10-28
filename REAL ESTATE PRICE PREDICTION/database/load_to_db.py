import pandas as pd
import sqlite3
from pathlib import Path

def load_data():
    base_dir = Path(__file__).resolve().parent
    dataset_path = base_dir / "data" / "Bengaluru_House_Data.csv"
    db_path = base_dir / "houses.db"

    if not dataset_path.exists():
        print(f"Dataset not found at {dataset_path}")
        return

    print(f"Loading data from {dataset_path}...")
    df = pd.read_csv(dataset_path)
    print(f"Data loaded successfully. Row count: {len(df)}")

    # Connect to SQLite
    conn = sqlite3.connect(db_path)
    df.to_sql('houses', conn, if_exists='replace', index=False)
    conn.close()
    print(f"Data saved to {db_path} in table 'houses'.")

if __name__ == "__main__":
    load_data()
