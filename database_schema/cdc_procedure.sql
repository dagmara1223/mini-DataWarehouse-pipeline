USE mini_dwh;

DELIMITER //
CREATE PROCEDURE cdc_fact_orders()
BEGIN
	#inserting - if such order is not inside fact_orders then insert it to fact_orders table 
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

	JOIN dim_date d ON s.date = d.date
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
	AND s.ship_service_level = c.ship_service_level
    WHERE NOT EXISTS(SELECT 1 FROM fact_orders f WHERE f.order_id = s.order_id);
    #updating records - if order inside two tables then you may update it
    UPDATE fact_orders f
	JOIN stg_orders s
	ON f.order_id = s.order_id
	SET
	f.qty = s.qty,
	f.amount = s.amount;
    #deleting records - if order only in fact table but not in stg_orders then delete it
    DELETE f
	FROM fact_orders f
	LEFT JOIN stg_orders s
	ON f.order_id = s.order_id
	WHERE s.order_id IS NULL;
END //
DELIMITER ; 

