from pathlib import Path
import pandas as pd
'''
Based on Google Collab analysis, data is begin cleaned & transformed following such scenario:
- Removing all-null rows
- Lowering all column names
'''
    
class DataTransformer():
    
    def main_transform(self, df) -> pd.DataFrame:
        df = self.clean_all_nulls(df) # drop all rows with all null values
        df = self.lower_column(df) # lower all column names

        return df
    
    def clean_all_nulls(self, df: pd.DataFrame) -> pd.DataFrame:
        before = len(df)

        df_cleaned = df.dropna(how='all', axis=0)

        after = len(df_cleaned)
        rows_removed = before - after 

        print(f"Removed: {rows_removed} rows with all - null values")
        
        return df_cleaned
    
    def lower_column(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = df.columns.str.lower()
        return df

