from pathlib import Path
import pandas as pd
import re

'''
Based on Google Collab analysis, data is begin cleaned & transformed based on following scenario:
Applies predefined cleaning and schema transformations:
- Drops rows containing only null values
- Standardizes column names
- Removes selected columns if present
- Casts columns to specified data types
- Fills missing values using operations (mean/sum/mode/median) or specific values (ex: Unknown, 0, IR)
- Drops selected duplicates based on grain
- Creates new columns based on correlations between data
'''
    
class DataTransformer():
    
    def main_transform(self, df : pd.DataFrame) -> pd.DataFrame:
        df = self.clean_all_nulls(df) # drop all rows with all null values
        df = self.lower_column_name(df) # lower all column names
        df = self.delete_all_column(df, ['unnamed: 22', 'axz', 'fulfilled-by', 'promotion-ids']) # delete pointed columns
        df = self.retype_col_value(df, 'Int64', ['ship-postal-code'])
        df = self.fill_missing_values_value(df, {'currency':'INR',
                                                 'courier status': 'Unknown',
                                                 'ship-city': 'Unknown',
                                                 'ship-state':'Unknown',
                                                 'ship-country': 'IN',
                                                 'ship-postal-code': 0})
        df = self.fill_missing_values_operation(df, {'amount':'mean'})
        df = self.drop_duplicates(df, ['order id', 'sku'])
        df = self.retype_col_value(df, 'category', ['status', 'fulfilment', 'ship-service-level',
                                        'category', 'size', 'courier status',
                                        'currency', 'ship-state', 'ship-country'])
        df = self.adding_data_values(df)
        df = self.add_new_non_data_columns(df, 'unit_price', 'qty*amount')
        df = self.map_column_names(df, 'b2b', 'order-type', {True:"B2B", False:"B2C"})

        df = self.cleaning_column_names(df)
        
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
                        col_names: list[str],
                        errors: str = "raise") -> pd.DataFrame:
        for col_name in col_names:
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
    
    def drop_duplicates(self, df:pd.DataFrame, value_list: list[str]) -> pd.DataFrame:
        for col in value_list:
            if col not in df.columns:
                print(f"Value {col} not in DataFrame. Skipping.")
                return df
        df = df.drop_duplicates(keep='first').reset_index(drop=True)
        print(f"Duplicates dropped. Index restored.")
        return df

    def adding_data_values(self, df: pd.DataFrame) -> pd.DataFrame:
        df['date'] = pd.to_datetime(df['date'])

        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        df['week'] = df['date'].dt.isocalendar().week

        return df
    
    def cleaning_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        df.columns = (
            df.columns
            .str.strip()
            .str.replace(" ", "_")
            .str.replace("-", "_")
        )
        print("Columns normalized")
        return df
    
    @staticmethod
    def check_rule(rule:str):
        """
        Validate rule string.
        Allowed characters: letters, *, +, /
        """
        pattern = r'^[a-zA-Z*+/ ]+'
        return re.fullmatch(pattern, rule) is not None
    
    @staticmethod
    def extracting_rule(rule:str) -> list[str]:
        operators = ['*', '/', '+']
        for op in operators:
            rule = rule.replace(op, ' ')
        values = rule.split()
        return values
    
    def apply_rules(self, df:pd.DataFrame, rule:str)->pd.Series:

        if "*" in rule:
            left, right = rule.split("*")
            return df[left] * df[right]
        elif "+" in rule:
            left, right = rule.split("+")
            return df[left] + df[right]
        elif "/" in rule:
            left, right = rule.split("/")
            return df[left]/df[right]
        else:
            raise ValueError(f"Unnknow rule operation: {rule}")
        

    def add_new_non_data_columns(self, df: pd.DataFrame,new_col:str, rule: str) -> pd.DataFrame:
        
        # Validating rule syntax
        if not self.check_rule(rule):
            raise ValueError(f"Invalid rule: {rule}")

        # Extracting column names from rule
        columns = self.extracting_rule(rule)

        # Checking whether columns exits
        missing = [col for col in columns if col not in df.columns]

        if missing:
            raise ValueError(f"Unnknown values in columns: {missing}")

        df[new_col] = self.apply_rules(df, rule)

        print(f"Column {new_col} created using rule {rule}")

        return df
    
    def map_column_names(self, df:pd.DataFrame, column:str, new_column:str,
                         mapping: dict) -> pd.DataFrame:
        
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found")

        df[new_column] = df[column].map(mapping)

        print(f"Column {new_column} created from mapping: {mapping}")

        return df
        

        
            
