# src/db/load_to_db.py
import pandas as pd
from sqlalchemy import create_engine
import os
from pathlib import Path

CLEAN_FILE = Path("data/processed/trade_cleaned.csv")
DB_URL = os.getenv("TRADE_DB_URL", "sqlite:///data/processed/trade_db.sqlite")

def load_to_db(csv_path=CLEAN_FILE, db_url=DB_URL, table_name="shipments"):
    df = pd.read_csv(csv_path)
    engine = create_engine(db_url)
    df.to_sql(table_name, engine, if_exists="replace", index=False, chunksize=1000)
    print(f"Loaded {len(df)} rows into table '{table_name}' at {db_url}")

if __name__ == "__main__":
    load_to_db()
