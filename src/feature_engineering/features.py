# src/feature_engineering/features.py
import pandas as pd
from pathlib import Path
import numpy as np

IN_FILE = Path("data/processed/trade_parsed.csv")
OUT_FILE = Path("data/processed/trade_cleaned.csv")

UNIT_MAP = {
    "PCS": "PCS", "PC": "PCS", "NOS": "PCS", "PIECES": "PCS", "PIECE": "PCS",
    "PKT": "PCS", "PACK": "PCS",
    "KG": "KG", "KGS": "KG", "G": "G",
    "MT": "MT", "MTS": "MT",
    "L": "LTR", "LTR": "LTR", "ML": "ML"
}

def normalize_unit(u):
    if not isinstance(u, str): return None
    key = u.strip().upper()
    return UNIT_MAP.get(key, key)

def assign_category(row):
    combined = f"{row.get('goods_description','')} {row.get('hsn_description','')}".upper()
    if "GLASS" in combined or "BOROSILICATE" in combined or "OPAL" in combined:
        return "Glass"
    if "WOOD" in combined or "WOODEN" in combined:
        return "Wooden"
    if "STEEL" in combined or "STAINLESS" in combined or "SS " in combined:
        return "Steel"
    if "PLASTIC" in combined or "POLY" in combined:
        return "Plastic"
    if "ELECTRON" in combined or "MACHINE" in combined or "MOTOR" in combined:
        return "Electronics"
    hsn = str(row.get("hsn_code",""))
    if len(hsn) >= 2:
        if hsn.startswith(("70","71","72")):
            return "Glass/Stone/Metal"
    return "Others"

def assign_subcategory(row):
    cat = row["category"]
    desc = f"{row.get('goods_description','')} {row.get('hsn_description','')}".upper()
    if cat == "Glass":
        if "BOROSILICATE" in desc:
            return "Borosilicate"
        if "OPAL" in desc or "OPALWARE" in desc:
            return "Opalware"
        return "General Glass"
    if cat == "Wooden":
        if "SPOON" in desc:
            return "Spoon"
        if "FORK" in desc:
            return "Fork"
        return "Wooden General"
    return "Other"

def compute_fields(df):
    df["grand_total_inr"] = df.get("total_value_inr", 0) + df.get("duty_paid_inr", 0)
    df["quantity"] = pd.to_numeric(df.get("quantity", 0), errors="coerce").fillna(0)
    df["landed_cost_per_unit"] = df.apply(
        lambda r: (r["grand_total_inr"] / r["quantity"]) if r["quantity"] > 0 else np.nan,
        axis=1
    )
    if "unit" in df.columns:
        df["unit_standardized"] = df["unit"].apply(normalize_unit)
    else:
        df["unit_standardized"] = None
    df["category"] = df.apply(assign_category, axis=1)
    df["sub_category"] = df.apply(assign_subcategory, axis=1)
    df["unit_price_usd"] = pd.to_numeric(df.get("unit_price_usd"), errors="coerce")
    return df

def main():
    df = pd.read_csv(IN_FILE)
    df = compute_fields(df)
    df.to_csv(OUT_FILE, index=False)
    print(f"Saved final cleaned dataset to {OUT_FILE}")

if __name__ == "__main__":
    main()
