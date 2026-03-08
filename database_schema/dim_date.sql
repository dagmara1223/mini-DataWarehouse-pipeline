USE mini_dwh;

CREATE TABLE dim_date (
    date_id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE,
    year INT,
    month INT,
    day INT,
    week INT
);

INSERT INTO dim_date(date, year, month, day, week)
SELECT DISTINCT 
	date, year, month, day, week
FROM stg_orders;

SELECT * FROM dim_date;