USE mini_dwh;

CREATE TABLE dim_location (
    location_id INT AUTO_INCREMENT PRIMARY KEY,
    ship_city VARCHAR(100),
    ship_state VARCHAR(100),
    ship_postal_code VARCHAR(20),
    ship_country VARCHAR(10)
);

INSERT INTO dim_location(ship_city, ship_state, ship_postal_code, ship_country) 
SELECT DISTINCT 
	ship_city, ship_state, ship_postal_code, ship_country
FROM stg_orders;

SELECT * FROM dim_location;