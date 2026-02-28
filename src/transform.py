from pathlib import Path
import pandas as pd
'''
Based on Google Collab analysis, data is begin cleaned & transformed based on following scenario:
Applies predefined cleaning and schema transformations:
- Drops rows containing only null values
- Standardizes column names
- Removes selected columns if present
- Casts columns to specified data types
'''
    
class DataTransformer():
    
    def main_transform(self, df : pd.DataFrame) -> pd.DataFrame:
        df = self.clean_all_nulls(df) # drop all rows with all null values
        df = self.lower_column_name(df) # lower all column names
        df = self.delete_all_column(df, ['unnamed: 22', 'axz', 'fulfilled-by', 'promotion-ids']) # delete pointed columns

        return df
    
    def clean_all_nulls(self, df: pd.DataFrame) -> pd.DataFrame:
        before = len(df)

        df_cleaned = df.dropna(how='all', axis=0)

        after = len(df_cleaned)
        rows_removed = before - after 

        print(f"Removed: {rows_removed} rows with all - null values")
        
        return df_cleaned
    
    def lower_column_name(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = df.columns.str.lower()
        print("All column names were lowered.")
        return df

    def delete_all_column(self, df:pd.DataFrame, col_names : list[str]) -> pd.DataFrame:
        df = df.copy()

        for col in col_names:
            if col not in df.columns:
                print(f"Column {col} not found in DataFrame Columns. Skipped.")
            else:
                df = df.drop(col, axis=1)
                print(f"Dropped column: {col} ")

        return df

    def retype_col_value(self, 
                        df: pd.DataFrame, new_type:str, 
                        col_name: str,
                        errors: str = "raise") -> pd.DataFrame:
        
        if col_name not in df.columns:
            print(f"Column {col_name} not in DataFrame.Skipping cast.")
            return df 
        
        try:
            df = df.copy()
            df[col_name] = df[col_name].astype(new_type)
            print(f"Column {col_name} casted to type: {new_type}")
        except Exception as e:
            if errors == 'raise':
                raise 
            elif errors == 'ignore':
                print(f"Failed to cast to type: {new_type}. Skipping.")
        
        return df
