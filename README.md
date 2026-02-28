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
[PANDAS_ANALYSIS/overview_and_missing_values.ipynb](PANDAS_ANALYSIS/overview_and_missing_values.ipynb)

**TO BE CONTINUED**

<br>
Based on the initial analysis, I implemented several utility functions in VS Code to automate the cleaning process: <br>
- Row Cleanup: Drops rows consisting entirely of missing values. <br>
- Header Normalization: Converts all column names to lowercase. <br>
- Selective Column Removal : Removes specified columns only if they exist in the dataset, ensuring pipeline robustness across schema variations. <br>
- Schema-Aware Type Casting: Enables controlled casting of selected columns to specified data types with configurable error handling (raise / ignore). <br>


