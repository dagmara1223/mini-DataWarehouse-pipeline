USE mini_dwh;

CREATE TABLE dim_product(
	product_id INT AUTO_INCREMENT PRIMARY KEY,
    category VARCHAR(50),
    size VARCHAR(10),
    style VARCHAR(50),
    sku VARCHAR(100),
    asin VARCHAR(50)
);

INSERT INTO dim_product(category, size, style,sku, asin)
SELECT DISTINCT 
	category, size, style, sku, asin
FROM stg_orders;

SELECT * FROM dim_product;