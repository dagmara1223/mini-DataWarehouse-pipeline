# 📓 Overview
This project implements an end-to-end data engineering pipeline using Python and MySQL. <br>
It simulates a production-style architecture with: 
- Raw data ingestion (Data Lake simulation)
- Staging layer transformations and data validation
- Star / Snowflake schema Data Warehouse (fact & dimension tables)
- Incremental loading and basic CDC logic

The goal of the project is to demonstrate data modeling, ETL design, and warehouse loading strategies in a realistic scenario. 🤖 <br>
<br>
**Desired Pipeline**: 
```
Synthetic data (CSV)
        ↓
Python ETL (extract, transform, load)
        ↓
MySQL (staging layer)
        ↓
MySQL (Data Warehouse – star schema)
        ↓
Dashboard / SQL analysis
```

## 1️⃣ Extracting CSV Data  
This project uses an **E-commerce dataset**, which provides a realistic business scenario for designing and evaluating Data Warehouse models.
The dataset is particularly suitable for schema modeling (Star Schema or Snowflake Schema) due to its relational structure, including orders, customers, and products.
The raw dataset is stored in the `data/source` directory.
A dedicated extraction step ingests the source files and moves them into the `data/raw` layer, simulating a Data Lake ingestion process. <br> 
Link to the dataset: https://www.kaggle.com/datasets/thedevastator/unlock-profits-with-e-commerce-sales-data   <br>
Results after this step:  <br>
<img width="381" height="125" alt="image" src="https://github.com/user-attachments/assets/dd9db1fa-a66b-4072-b5a3-74bd8cdad8f9" />

## 2️⃣ Data Transformation 
Before implementing core functions in Visual Studio Code, I conducted a thorough data exploration using Google Colab to better understand the dataset's structure and quality.
The analysis is documented in the following stages: 
- Data Overview & Missing Values: Detailed inspection of data types and null values. <br> 
[PANDAS_ANALYSIS/overview_and_missing_values.ipynb](PANDAS_ANALYSIS/overview_and_missing_values.ipynb) <br>
<br>
`to be continued`

<br>
As a result following functions were created: <br>
- `def clean_all_nulls` function that drops all rows with null-values only
- `lower_column` function that lowers column names


