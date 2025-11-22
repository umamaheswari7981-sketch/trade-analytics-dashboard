# src/parsing/parse_goods_description.py
import re
import pandas as pd
from pathlib import Path

IN_FILE = Path("data/processed/clean_base.csv")
OUT_FILE = Path("data/processed/trade_parsed.csv")

USD_PRICE_PATTERN = re.compile(r"(?:USD|\$)\s*([0-9]+(?:\.[0-9]+)?)", re.IGNORECASE)
CAPACITY_PATTERN = re.compile(r"(\d+(?:\.\d+)?\s*(?:ML|L|LTR|CC|G|KG|INCH|MM|CM|M))", re.IGNORECASE)
MODEL_NUMBER_PATTERN = re.compile(r"\b([A-Z0-9]+[-_][A-Z0-9]+)\b", re.IGNORECASE)
EMBEDDED_QTY_PATTERN = re.compile(r"(?:PACK OF|PKT OF|P/BOX|PACKAGING\s*:\s*)(\d+)", re.IGNORECASE)
MATERIAL_PATTERN = re.compile(r"\b(BOROSILICATE|OPALWARE|GLASS|WOOD|PLASTIC|POLY|STEEL|SS|STAINLESS|CERAMIC|ALUMINUM|ALUMINIUM)\b", re.IGNORECASE)

def extract_unit_price_usd(text):
    if not isinstance(text, str): return None
    m = USD_PRICE_PATTERN.search(text)
    if m:
        try:
            return float(m.group(1))
        except:
            return None
    return None

def extract_capacity(text):
    if not isinstance(text, str): return None
    m = CAPACITY_PATTERN.search(text)
    return m.group(1) if m else None

def extract_model_number(text):
    if not isinstance(text, str): return None
    m = MODEL_NUMBER_PATTERN.search(text)
    return m.group(1) if m else None

def extract_material(text):
    if not isinstance(text, str): return None
    m = MATERIAL_PATTERN.search(text)
    return m.group(1).title() if m else None

def extract_embedded_qty(text):
    if not isinstance(text, str): return None
    m = EMBEDDED_QTY_PATTERN.search(text)
    return int(m.group(1)) if m else None

def extract_model_name(text, model_number=None):
    if not isinstance(text, str): return None
    txt = text.strip()
    if model_number and model_number in txt:
        idx = txt.index(model_number)
        left = txt[:idx].strip()
        parts = left.split()
        return " ".join(parts[-4:]).strip() if parts else None
    parts = txt.split()
    if len(parts) >= 3:
        return " ".join(parts[:4])
    return txt

def parse_row(row):
    desc = row.get("goods_description", "") or ""
    desc_up = desc.upper()
    model_number = extract_model_number(desc_up)
    return {
        "model_name": extract_model_name(desc, model_number),
        "model_number": model_number,
        "capacity_spec": extract_capacity(desc_up),
        "material_type": extract_material(desc_up),
        "embedded_quantity": extract_embedded_qty(desc_up),
        "unit_price_usd": extract_unit_price_usd(desc_up)
    }

def main():
    df = pd.read_csv(IN_FILE)
    if "goods_description" not in df.columns:
        raise ValueError("goods_description column not found in clean_base.csv")
    parsed = df.apply(parse_row, axis=1, result_type="expand")
    out = pd.concat([df, parsed], axis=1)
    out.to_csv(OUT_FILE, index=False)
    print(f"Saved parsed file to {OUT_FILE}")

if __name__ == "__main__":
    main()
