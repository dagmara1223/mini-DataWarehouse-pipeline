from pathlib import Path
import pandas as pd
'''
Based on Google Collab analysis, data is begin cleaned & transformed based on following scenario:
Applies predefined cleaning and schema transformations:
- Drops rows containing only null values
- Standardizes column names
- Removes selected columns if present
- Casts columns to specified data types
- Fills missing values using operations (mean/sum/mode/median) or specific values (ex: Unknown, 0, IR)
'''
    
class DataTransformer():
    
    def main_transform(self, df : pd.DataFrame) -> pd.DataFrame:
        df = self.clean_all_nulls(df) # drop all rows with all null values
        df = self.lower_column_name(df) # lower all column names
        df = self.delete_all_column(df, ['unnamed: 22', 'axz', 'fulfilled-by', 'promotion-ids']) # delete pointed columns
        df = self.retype_col_value(df, 'Int64', 'ship-postal-code')
        df = self.fill_missing_values_value(df, {'currency':'INR',
                                                 'courier status': 'Unknown',
                                                 'ship-city': 'Unknown',
                                                 'ship-state':'Unknown',
                                                 'ship-country': 'IN',
                                                 'ship-postal-code': 0})
        df = self.fill_missing_values_operation(df, {'amount':'mean'})
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
            df[col_name] = df[col_name].astype(new_type)
            print(f"Column {col_name} casted to type: {new_type}")
        except (ValueError, TypeError) as e:
            if errors == "raise":
                raise
            print(f"Failed casting column '{col_name}' to {new_type}. Skipped.")
        
        return df

    def fill_missing_values_value(self, df : pd.DataFrame, 
                                fill_map : dict[str,any]) -> pd.DataFrame:
        
        for column_name, value in fill_map.items():
            if column_name not in df.columns:
                print(f"Column {column_name} not found in DataFrame. Skipped")
            else:
                df[column_name] = df[column_name].fillna(value)
                print(f"Column {column_name} filled nulls with value {value}.")
        return df


    def fill_missing_values_operation(self, df:pd.DataFrame, fill_map:dict[str,any]) -> pd.DataFrame:
        
        for column_name, operation in fill_map.items():
            if column_name not in df.columns:
                print(f"Column {column_name} not found in DataFrame. Skipped.")
                continue
                
            if operation == 'sum':
                value = round(df[column_name].sum(),2)
            elif operation == 'mean':
                value = round(df[column_name].mean(),2)
            elif operation == 'median':
                value = round(df[column_name].median(),2)
            elif operation == "mode":
                mode_series = df[column_name].mode()
                value = mode_series.iloc[0] if not mode_series.empty else None
            else:
                print(f"Unsupported operation: {operation}. Skipped.")
                continue
        
        df[column_name] = df[column_name].fillna(value)
        print(f"Filled {column_name} with value {value} Based on {operation}.")
        return df
            
