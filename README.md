# 📓 Overview
This project implements an end-to-end data engineering pipeline using Python and MySQL. <br>
It simulates a production-style architecture with: 
- Raw data ingestion (Data Lake simulation)
- Staging layer transformations and data validation
- Star / Snowflake schema Data Warehouse (fact & dimension tables)
- Incremental loading and basic CDC logic

The goal of the project is to demonstrate data modeling, ETL design, and warehouse loading strategies in a realistic scenario. 🤖 <br>
<br>
**Full ETL Pipeline**: 
```
Raw Data (CSV)
      ↓
Extract
      ↓
Data Transformation
(Cleaning + Feature Engineering)
      ↓
Staging Layer (MySQL - stg_orders)
      ↓
Dimensional Modeling
(Star Schema)
      ↓
Data Warehouse Tables
(dimensions + fact table)
      ↓
Change Data Capture
      ↓
Analytics / SQL Queries
```

## 1️⃣ Extracting CSV Data (E)
This project uses an **E-commerce dataset**, which provides a realistic business scenario for designing and evaluating Data Warehouse models.
The dataset is particularly suitable for schema modeling (Star Schema or Snowflake Schema) due to its relational structure, including orders, customers, and products.
The raw dataset is stored in the `data/source` directory.
A dedicated extraction step ingests the source files and moves them into the `data/raw` layer, simulating a Data Lake ingestion process. <br> 
Link to the dataset: https://www.kaggle.com/datasets/thedevastator/unlock-profits-with-e-commerce-sales-data   <br>
Results after this step:  <br>
<img width="381" height="125" alt="image" src="https://github.com/user-attachments/assets/dd9db1fa-a66b-4072-b5a3-74bd8cdad8f9" />

## 2️⃣ Data Transformation (T)
Before implementing core functions in Visual Studio Code, I conducted a thorough data exploration using Google Colab to better understand the dataset's structure and quality.
The analysis is documented in the following stages: 
- Data Overview & Missing Values: Detailed inspection of data types and null values. <br> 
[PANDAS_ANALYSIS/overview_and_missing_values.ipynb](PANDAS_ANALYSIS/overview_and_missing_values.ipynb)
- Dealing with duplicated values and **grain** search. <br>
[PANDAS_ANALYSIS/duplicates_analysis.ipynb](PANDAS_ANALYSIS/duplicates_analysis.ipynb) <br>
- Evaluation of column cardinality and identification of fields suitable for categorical encoding to improve memory efficiency and analytical performance.  
  Investigation of numerical distributions and categorical value patterns. <br>
[PANDAS_ANALYSIS/dtypes_and_optimalization.ipynb](PANDAS_ANALYSIS/dtypes_and_optimalization.ipynb) <br>
- Feature Engineering (adding new columns based on correlations) and further cleaning of column names. <br>
[PANDAS_ANALYSIS/Correlations_feature_engineering.ipynb](PANDAS_ANALYSIS/Correlations_feature_engineering.ipynb)



Based on the initial analysis, I implemented several utility functions in VS Code to automate the cleaning process: <br>
- **Row Cleanup:** Drops rows consisting entirely of missing values. <br>
- **Header Normalization:** Converts all column names to lowercase. <br>
- **Selective Column Removal:** Removes specified columns only if they exist in the dataset, ensuring pipeline robustness across schema variations. <br>
- **Schema-Aware Type Casting:** Enables controlled casting of selected columns to specified data types with configurable error handling. <br>
- **Flexible Missing Data Handling**: Supports both constant value replacement and aggregation-based imputation (mean, median, sum, mode) using a configuration-driven approach. <br>
- **Feature Engineering and Stripping column names**: New features were created to support analytical use cases and dimensional modeling.
These transformations enable time-based analysis, pricing calculations, and simplified business categorization.
Column names were also standardized by removing unnecessary spaces and applying a consistent naming convention.

Full implementation: [src/transform.py](src/transform.py)     
Resultats after ET process: <br>
<img width="745" height="591" alt="image" src="https://github.com/user-attachments/assets/0e9f0da9-711f-4163-a539-2f7134723e3f" />  <br>

Columns: <br>
<img width="500" height="125" alt="image" src="https://github.com/user-attachments/assets/6ad8bf94-7db1-461e-8f4e-b61c0a4e38a4" />  <br>

First 10 rows: <br>
<img width="700" height="500" alt="image" src="https://github.com/user-attachments/assets/1dbebe08-1950-4f85-81aa-97e64f769cda" />

## 3️⃣ Dimensional Modeling – Star Schema 

After the data cleaning and transformation stage, a dimensional model was designed to support analytical queries in the Data Warehouse. <br>
A **Star Schema** was implemented, consisting of one fact table and multiple dimension tables. <br>
The **fact table (`fact_orders`)** represents transactional data at the grain level: <br>
> one row = one product in an order <br>
The fact table stores measurable metrics such as:
- `qty`
- `amount`
- `unit_price`
and references descriptive dimensions through foreign keys. <br>

The following dimension tables were created:
- **dim_date** – calendar attributes used for time-based analysis (date, year, month, day, week)
- **dim_product** – product-related information (SKU, category, size, style, asin)
- **dim_location** – shipping location details 
- **dim_channel** – order fulfilment, sales channel, and delivery information

The schema was designed using **DBML** and code can be found in: <br> 
[database_schema/star_schema.dbml](database_schema/star_schema.dbml)

Results: <br>
<img width="900" height="840" alt="image" src="https://github.com/user-attachments/assets/b952efb4-41b6-4d29-8156-c5bc41126401" />

## 4️⃣ Staging Layer and Data Loading (L)
As part of the Data Warehouse pipeline, a staging table was created in MySQL Workbench to store the transformed dataset before building the dimensional model. SQL script is available here: [database_schema/std_order.sql](database_schema/std_order.sql) <br>
Such script defines the structure of staging table used to temporaily hold cleaned and enriched data produced by transformation pipeline. <br>
<img width="400" height="400" alt="image" src="https://github.com/user-attachments/assets/3ab63a99-7763-4b22-863d-813fb36b8884" />  <br>

**Python Data Loader**  <br>
To complete the Load step of the ETL pipeline, a Python class was implemented to insert the transformed dataset into the staging table.
The loader connects to MySQL using SQLAlchemy and loads the Pandas DataFrame generated by the transformation pipeline into the stg_orders table.
This step finalizes the ETL workflow: <br>
`Extract → Transform → Load` 
where:
- Extract reads raw CSV files
- Transform cleans and enriches the dataset
- Load inserts the processed data into the staging table in MySQL

<img width="431" height="51" alt="image" src="https://github.com/user-attachments/assets/67d2623a-6592-4b75-bf33-2eeb166a56cc" /> <br>


**Effect in MySQL Workbench**: <br>
<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/8c93a3aa-9a8d-46c0-a470-b94346dccfde" />

## 5️⃣ DataWarehouse modeling 
Based on previously created **Star Schema**, following **Fact Table** and **Dimension Tables** were created in MySQL Workbench: 
1. Product Dimension Table: [database_schema/dim_product.sql](database_schema/dim_product.sql)
2. Date Dimension Table: [database_schema/dim_date.sql](database_schema/dim_date.sql)
3. Location Dimension Table: [database_schema/dim_location.sql](database_schema/dim_location.sql)
4. Channel Dimenstion Table: [database_schema/dim_channel.sql](database_schema/dim_channel.sql)
5. Fact Table: [database_schema/fact_orders.sql](database_schema/fact_orders.sql)

Our fact table : <br>
<img width="700" height="601" alt="image" src="https://github.com/user-attachments/assets/e117953b-3685-4510-ab66-085c1df41c00" />

## 6️⃣ CDC - Change Data Capture 
To avoid reloading the entire dataset during each internal piepline run, a manual Change Data Capture (CDC) mechanism was implemented. <br>
The goal is to load only new records from the staging table (stg_orders) into the fact table (fact_orders). Instead of performing a full refresh of the fact table, the pipeline compares records from the staging layer with existing records in the data warehouse. <br> 
Only records that do not yet exist in the fact table are inserted. Such approach is being implemented using **Stored Procedures**. 

**TO BE CONTINUED**


