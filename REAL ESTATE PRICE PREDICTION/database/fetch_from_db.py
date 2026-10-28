import pandas as pd
import sqlite3
import os

def fetch_data():
    db_path = os.path.join('database', 'houses.db')
    if not os.path.exists(db_path):
        # Alternative for local execution if absolute path is needed
        db_path = 'database/houses.db'
        
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM houses", conn)
    conn.close()
    return df

if __name__ == "__main__":
    df = fetch_data()
    print(df.head())
    print(f"Total rows fetched: {len(df)}")
