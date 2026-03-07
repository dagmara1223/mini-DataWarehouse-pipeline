# 📓 Overview
This project implements an end-to-end data engineering pipeline using Python and MySQL. <br>
It simulates a production-style architecture with: 
- Raw data ingestion (Data Lake simulation)
- Staging layer transformations and data validation
- Star / Snowflake schema Data Warehouse (fact & dimension tables)
- Incremental loading and basic CDC logic

The goal of the project is to demonstrate data modeling, ETL design, and warehouse loading strategies in a realistic scenario. 🤖 <br>
<br>
**Desired ETL Pipeline**: 
```
Synthetic data (CSV)
        ↓
EDA / profiling
        ↓
cleaning + feature engineering
        ↓
staging dataframe
        ↓
dimensional modeling (Star Schema)
        ↓
load to warehouse
        ↓
Dashboard / SQL analysis
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
## Dimensional Modeling – Star Schema

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

Results: <br>
<img width="900" height="840" alt="image" src="https://github.com/user-attachments/assets/b952efb4-41b6-4d29-8156-c5bc41126401" />


**TO BE CONTINUED**


