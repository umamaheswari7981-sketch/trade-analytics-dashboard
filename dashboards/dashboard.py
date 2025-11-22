import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

# Connect to SQLite database
engine = create_engine('sqlite:///data/processed/trade_db.sqlite')

# Function to load data
def load_data(query):
    return pd.read_sql(query, engine)

# 1. Overview (Macro Trends)
def macro_trends():
    query = """
    SELECT year, SUM(total_value_inr) as total_value, SUM(duty_paid_inr) as duty_paid, SUM(grand_total_inr) as grand_total
    FROM shipments
    GROUP BY year
    ORDER BY year
    """
    df = load_data(query)
    fig = px.line(df, x='year', y=['total_value', 'duty_paid', 'grand_total'],
                  title='YoY Macro Trends')
    fig.write_html('dashboards/macro_trends.html')
    print("Macro trends chart saved to dashboards/macro_trends.html")

# 2. Category Drilldown
def category_drilldown():
    query = """
    SELECT category, sub_category, model_name, SUM(total_value_inr) as total_value
    FROM shipments
    GROUP BY category, sub_category, model_name
    """
    df = load_data(query)
    fig = px.treemap(df, path=['category', 'sub_category', 'model_name'], values='total_value',
                     title='Category > Sub-category > Model Drilldown')
    fig.write_html('dashboards/category_drilldown.html')
    print("Category drilldown chart saved to dashboards/category_drilldown.html")

# 3. Supplier Analysis
def supplier_analysis():
    # Top suppliers
    query_top = """
    SELECT supplier_name, SUM(grand_total_inr) as grand_total
    FROM shipments
    GROUP BY supplier_name
    ORDER BY grand_total DESC
    LIMIT 20
    """
    df_top = load_data(query_top)
    fig_bar = px.bar(df_top, x='supplier_name', y='grand_total', title='Top 20 Suppliers by Grand Total')
    fig_bar.write_html('dashboards/top_suppliers.html')

    # Supplier status (using the supplier_analysis.sql logic)
    query_status = """
    WITH supplier_years AS (
        SELECT supplier_name, year, COUNT(*) as shipments
        FROM shipments
        GROUP BY supplier_name, year
    ),
    suppliers AS (
        SELECT DISTINCT supplier_name FROM shipments
    )
    SELECT
        s.supplier_name,
        MAX(CASE WHEN sy.year = 2025 THEN 1 ELSE 0 END) AS active_in_2025,
        CASE
            WHEN MAX(CASE WHEN sy.year = 2025 THEN 1 ELSE 0 END) = 1 THEN 'Active_2025'
            WHEN SUM(CASE WHEN sy.year < 2025 THEN 1 ELSE 0 END) > 0 THEN 'Churned'
            ELSE 'New_or_Unknown'
        END AS status
    FROM suppliers s
    LEFT JOIN supplier_years sy ON s.supplier_name = sy.supplier_name
    GROUP BY s.supplier_name
    """
    df_status = load_data(query_status)
    status_summary = df_status.groupby('status').size().reset_index(name='count')
    fig_donut = px.pie(status_summary, names='status', values='count', title='Supplier Status Distribution', hole=0.4)
    fig_donut.write_html('dashboards/supplier_status.html')

    print("Supplier analysis charts saved to dashboards/top_suppliers.html and dashboards/supplier_status.html")

# 4. Unit Economics
def unit_economics():
    query = """
    SELECT capacity_spec, landed_cost_per_unit, quantity, category
    FROM shipments
    WHERE capacity_spec IS NOT NULL AND landed_cost_per_unit IS NOT NULL
    """
    df = load_data(query)
    # Assuming capacity_spec is numeric
    df['capacity_spec'] = pd.to_numeric(df['capacity_spec'], errors='coerce')
    fig = px.scatter(df, x='capacity_spec', y='landed_cost_per_unit', size='quantity', color='category',
                     title='Unit Economics Scatter Plot')
    fig.write_html('dashboards/unit_economics.html')
    print("Unit economics scatter plot saved to dashboards/unit_economics.html")

if __name__ == '__main__':
    macro_trends()
    category_drilldown()
    supplier_analysis()
    unit_economics()
    print("All dashboards generated.")
