# siddharth_trade_pipeline

Project scaffold for the Siddharth Associates International Trade Data Analysis assignment.

Folders:
- data/raw: place the provided Excel here (sample_data.xlsx)
- data/processed: outputs from scripts
- src/*: python scripts for cleaning, parsing, feature engineering, and DB load
- sql/*: SQL scripts for schema and analysis queries
- dashboards/*: dashboard notes

Quick run:
1. python src/cleaning/clean_base.py
2. python src/parsing/parse_goods_description.py
3. python src/feature_engineering/features.py
4. python src/db/load_to_db.py
