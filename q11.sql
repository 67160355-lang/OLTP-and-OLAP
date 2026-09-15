SELECT
    (SELECT COUNT(*) FROM fact_sales) AS rows_before_join,
    (SELECT SUM(quantity * unit_price) FROM fact_sales) AS revenue_before_join,
    (SELECT COUNT(*) FROM sales) AS rows_after_join,
    (SELECT SUM(amount) FROM sales) AS revenue_after_join;
