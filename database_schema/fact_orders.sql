USE mini_dwh;

CREATE TABLE fact_orders (
    order_item_key INT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(100),
    date_id INT,
    product_id INT,
    location_id INT,
    channel_id INT,
    qty INT,
    amount FLOAT,
    unit_price FLOAT
);

INSERT INTO fact_orders(order_id, date_id, product_id, location_id, channel_id, qty, amount, unit_price)
SELECT 
    s.order_id,
    d.date_id,
    p.product_id,
    l.location_id,
    c.channel_id,
    s.qty,
    s.amount,
    s.unit_price
FROM stg_orders s 
JOIN dim_date d 
	ON s.date = d.date
JOIN dim_product p 
	ON s.sku = p.sku
	AND s.size = p.size
	AND s.style = p.style
	AND s.category = p.category
	AND s.asin = p.asin
JOIN dim_location l 
	ON s.ship_city = l.ship_city
	AND s.ship_state = l.ship_state
	AND s.ship_postal_code = l.ship_postal_code
	AND s.ship_country = l.ship_country
JOIN dim_channel c 
	ON s.status = c.status
	AND s.fulfilment = c.fulfilment
	AND s.sales_channel = c.sales_channel
	AND s.courier_status = c.courier_status
	AND s.currency = c.currency
	AND s.order_type = c.order_type
	AND s.ship_service_level = c.ship_service_level;
   
SELECT COUNT(*) FROM fact_orders;
