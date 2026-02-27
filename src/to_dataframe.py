from pathlib import Path
import pandas as pd 


class CSVReader:
    '''
    Transform data into Data Frame
    '''
    def __init__(self, raw_path: str):
        self.raw_path = Path(raw_path)

    def to_df(self) -> pd.DataFrame:
        return pd.read_csv(self.raw_path)