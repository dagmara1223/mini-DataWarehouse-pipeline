CREATE DATABASE mini_dwh;
USE mini_dwh;

CREATE TABLE stg_orders(
	order_id VARCHAR(100),
    date DATE,
    status VARCHAR(50),
    fulfilment VARCHAR(50),
    sales_channel VARCHAR(20),
    ship_service_level VARCHAR(50),
    style VARCHAR(50),
    sku VARCHAR(100),
    category VARCHAR(50),
    size VARCHAR(10),
    asin VARCHAR(50),
    courier_status VARCHAR(30),
    qty INT,
    currency VARCHAR(50),
    amount FLOAT,
    ship_city VARCHAR(100),
	ship_state VARCHAR(100),
    ship_postal_code VARCHAR(20),
    ship_country VARCHAR(10),
    b2b BOOLEAN,
    year INT,
    month INT,
    day INT,
    week INT,
    unit_price FLOAT,
    order_type VARCHAR(4)
)