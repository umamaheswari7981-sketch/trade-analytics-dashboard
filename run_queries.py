import pandas as pd
from sqlalchemy import create_engine, text

db_path = 'sqlite:///data/processed/trade_db.sqlite'
engine = create_engine(db_path)

def run_sql_file(filename):
    print(f"\n--- Running analysis: {filename} ---")
    try:
        with open(f'sql/{filename}', 'r') as file:
            sql_query = file.read()
        
        # Use pandas to run the query and display results nicely
        with engine.connect() as connection:
            result_df = pd.read_sql_query(text(sql_query), connection)
            print(result_df)
            print("-" * 30)
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    except Exception as e:
        print(f"An error occurred running query: {e}")

# Run the analyses
run_sql_file('macro_trends.sql')
run_sql_file('pareto_hsn.sql')
run_sql_file('supplier_analysis.sql')
