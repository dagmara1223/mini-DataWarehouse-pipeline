USE mini_dwh;

CREATE TABLE dim_channel (
    channel_id INT AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(50),
    fulfilment VARCHAR(50),
    sales_channel VARCHAR(20),
    courier_status VARCHAR(30),
    currency VARCHAR(50),
    order_type VARCHAR(4),
    ship_service_level VARCHAR(50)
);

INSERT INTO dim_channel (status, fulfilment, sales_channel, courier_status, currency, order_type, ship_service_level)
SELECT DISTINCT 
	status, fulfilment, sales_channel, courier_status, currency, order_type, ship_service_level
FROM stg_orders;

SELECT * FROM dim_channel
	