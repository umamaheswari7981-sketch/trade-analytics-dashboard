-- sql/pareto_hsn.sql
WITH hsn_totals AS (
    SELECT
        COALESCE(hsn_code,'UNKNOWN') AS hsn_code,
        SUM(total_value_inr) AS total_value_inr
    FROM shipments
    GROUP BY COALESCE(hsn_code,'UNKNOWN')
),
ordered AS (
    SELECT
        hsn_code,
        total_value_inr,
        total_value_inr * 1.0 / SUM(total_value_inr) OVER () AS share_of_total,
        ROW_NUMBER() OVER (ORDER BY total_value_inr DESC) rn
    FROM hsn_totals
)
SELECT
    CASE WHEN rn <= 25 THEN hsn_code ELSE 'OTHERS' END AS hsn_bucket,
    SUM(total_value_inr) AS bucket_value,
    SUM(total_value_inr) * 1.0 / (SELECT SUM(total_value_inr) FROM hsn_totals) AS bucket_share
FROM ordered
GROUP BY CASE WHEN rn <= 25 THEN hsn_code ELSE 'OTHERS' END
ORDER BY bucket_value DESC;
