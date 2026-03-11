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

# Comparison with global avg

SELECT ship_state, total_sales 
FROM (
	SELECT l.ship_state, ROUND(SUM(f.amount),2) AS total_sales
	FROM fact_orders f 
		JOIN dim_location l ON l.location_id = f.location_id
	GROUP BY l.ship_state) state_sales
WHERE total_sales > (
	SELECT AVG(state_total) FROM (
									SELECT SUM(f.amount) AS state_total FROM 	
                                    fact_orders f JOIN dim_location l ON l.location_id = f.location_id
                                    GROUP BY l.ship_state
                                    ) avg_table
)
ORDER BY total_sales DESC;

# b2b vs b2c shares
WITH order_type AS(
	SELECT c.order_type, ROUND(SUM(f.amount),2) AS amount
	FROM fact_orders f 
		JOIN dim_channel c ON c.channel_id = f.channel_id 
	GROUP BY c.order_type),
    total_sales AS (SELECT ROUND(SUM(amount),2) AS total_order_sales FROM order_type)
SELECT o.order_type, o.amount, ROUND(o.amount/ t.total_order_sales * 100, 2) AS sales_share
FROM order_type o CROSS JOIN total_sales t;
