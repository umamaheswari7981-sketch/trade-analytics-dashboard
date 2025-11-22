# src/cleaning/clean_base.py
"""Load raw Excel, standardize columns, convert dates, basic cleaning.
Assumes file: data/raw/sample_data.xlsx
"""
import pandas as pd
from pathlib import Path

RAW_PATH = Path("data/raw/sample_data.xlsx")
OUT_DIR = Path("data/processed")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def load_raw(path=RAW_PATH):
    df = pd.read_excel(path, sheet_name=0, engine="openpyxl")
    return df

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    rename_map = {}
    for c in df.columns:
        nc = c.strip().lower().replace(" ", "_").replace("/", "_").replace("-", "_")
        rename_map[c] = nc
    df = df.rename(columns=rename_map)
    return df

def convert_dates(df: pd.DataFrame, col="date_of_shipment"):
    if col not in df.columns:
        print(f"Warning: {col} not in columns")
        return df
    df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")
    df["year"] = df[col].dt.year
    df["month"] = df[col].dt.month
    df["quarter"] = df[col].dt.to_period("Q")
    return df

def basic_fill_and_cast(df: pd.DataFrame):
    numeric_cols = ["quantity", "unit_price_inr", "total_value_inr", "duty_paid_inr"]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)
    return df

def save_preview(df, out=OUT_DIR / "01_clean_preview.csv"):
    df.head(50).to_csv(out, index=False)
    print(f"Saved preview to {out}")

def main():
    df = load_raw()
    df = standardize_columns(df)
    df = convert_dates(df, col="date_of_shipment")
    df = basic_fill_and_cast(df)
    save_preview(df)
    df.to_csv(OUT_DIR / "clean_base.csv", index=False)
    print("Saved clean_base.csv to data/processed/")

if __name__ == "__main__":
    main()
