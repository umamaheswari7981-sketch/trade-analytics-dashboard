import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('data/processed/trade_db.sqlite')
cursor = conn.cursor()

# Execute schema.sql to create the table if it doesn't exist
with open('sql/schema.sql', 'r') as f:
    schema_sql = f.read()
cursor.executescript(schema_sql)
conn.commit()
print("Schema executed successfully.")

# List of query files
query_files = ['macro_trends.sql', 'pareto_hsn.sql', 'supplier_analysis.sql']

# Execute each query and print results
for file in query_files:
    with open(f'sql/{file}', 'r') as f:
        query_sql = f.read()
    try:
        result = cursor.execute(query_sql).fetchall()
        print(f"\nResults for {file}:")
        if result:
            for row in result:
                print(row)
        else:
            print("No results.")
    except Exception as e:
        print(f"Error executing {file}: {e}")

# Close the connection
conn.close()
print("\nAll SQL scripts executed.")
