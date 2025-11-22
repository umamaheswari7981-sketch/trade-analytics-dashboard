Power BI Dashboard Plan - Trade Analysis

Pages:
1. Overview (Macro)
   - Line chart: Year on X, Sum(Total Value INR), Sum(Duty Paid INR), Sum(Grand Total INR) as series.
   - KPI cards: Total Value (2025), YoY Growth %, Duty Paid (2025)
   - YoY Growth heatmap: Matrix with Year vs Metric (Total Value, Duty Paid, Grand Total) colored by YoY %

2. Category Drilldown
   - Sunburst / Treemap: Category -> Sub-Category -> Model
   - Filters: Year, Supplier

3. Supplier Analysis
   - Bar chart: Top Suppliers by Grand Total (top 20)
   - Donut: Active vs Churned supplier value share (2025)
   - Table: Suppliers with first shipment year, last shipment year, status

4. Unit Economics
   - Scatter plot: Capacity (numeric) on X vs Landed Cost Per Unit on Y, size=Qty, color=Category
   - Table: Top anomalous duty transactions

Tips:
- Create a Date table and relate shipments.date_of_shipment to Date[Date].
- Pre-calculate year, month, quarter in ETL to speed up visuals.
