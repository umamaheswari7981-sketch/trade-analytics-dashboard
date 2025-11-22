-- sql/supplier_analysis.sql
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
ORDER BY status, supplier_name;
