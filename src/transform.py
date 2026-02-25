from pathlib import Path
import pandas as pd
'''
This class transforms data into DataFrame. Then data is begin cleaned :
- Removing all-null rows
-...
'''

class DataTransformer():
    # constructor
    def __init__(self, raw_dir: str):
        self.raw_dir = Path(raw_dir) # ex: data\raw\Amazon_Sale_Report_20260225_150528.csv

    # Transform data into df 
    def transform_to_DataFrame(self) -> pd.DataFrame:
        return pd.read_csv(self.raw_dir)
    
    def clean_all_nulls(self, df: pd.DataFrame) -> pd.DataFrame:
        before = len(df)

        df_cleaned = df.dropna(how='all', axis=0)

        after = len(df_cleaned)
        rows_removed = before - after # Informs how many rows contained all null values

        print(f"Removed: {rows_removed} rows with all - null values")
        
        return df_cleaned
    
