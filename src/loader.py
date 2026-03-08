from sqlalchemy import create_engine
import pandas as pd
'''
Connects to MySQL and loads tranfsormed data into SQL table. 
'''
class DataLoader:

    def __init__(self, user, password, host, database):
        self.engine = create_engine(
            f"mysql+pymysql://{user}:{password}@{host}/{database}"
        )

    def load_to_staging(self, df: pd.DataFrame, table_name:str):
        df = df.drop(columns=["index"], errors="ignore")
        df.to_sql(
            table_name,
            self.engine,
            if_exists='append',
            index=False 
        )
        print(f"Loaded {len(df)} rows into {table_name}")