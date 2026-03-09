USE mini_dwh;

# Top selling category
SELECT p.category, ROUND(SUM(f.unit_price),2) AS price
FROM dim_product p 
	JOIN fact_orders f ON f.product_id = p.product_id
GROUP BY p.category ORDER BY price DESC;

# Sales by month
SELECT d.year, d.month, SUM(f.amount) AS amount
FROM dim_date d 
	JOIN fact_orders f ON d.date_id = f.date_id
GROUP BY d.year, d.month 
ORDER BY d.month; 

# Top 3 products in each month
WITH monthly_product_sales AS(
	SELECT p.category, p.style, d.year, d.month, SUM(f.unit_price) AS unit_price
	FROM fact_orders f
		JOIN dim_date d 
			ON d.date_id = f.date_id
		JOIN dim_product p 
			ON p.product_id = f.product_id
	GROUP BY p.category, p.style, d.year, d.month),
	ordered_monthly_prods AS(SELECT *,
		ROW_NUMBER() OVER(PARTITION BY year, month ORDER BY unit_price DESC) AS ranks
		FROM monthly_product_sales)
SELECT * FROM ordered_monthly_prods WHERE ranks <= 3;
