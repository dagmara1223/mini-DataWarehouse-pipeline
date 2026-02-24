import shutil 
from pathlib import Path 
from datetime import datetime

'''
The DataExtractor class is responsible for extracting CSV files from 
data/source directory and moving it into data/raw directory
'''

class DataExtractor():

    def __init__(self, source_dir: dir, destination_dir: dir):  
        self.source_dir = Path(source_dir)
        self.destination_dir = Path(destination_dir)
        
        # Create raw directory if does not exist
        self.destination_dir.mkdir(parents=True, exist_ok=True)

    def extract_csv(self, filename:str):
        time_stamp = datetime.now().strftime("%Y%m%d_%H%M%S") # Extracting date and time of the operation
        source_file = self.source_dir/filename # source file: data/source/examplename.csv
        if not source_file.exists():
            raise ValueError(f"No such file as {filename}")
        destination_file = self.destination_dir/f"{source_file.stem}_{time_stamp}.csv" # destination file: data/raw/example_filename.csv_24022026120000

        shutil.copy(source_file, destination_file) # copying contents

        print(f"File {filename} extracted from {self.source_dir} to {self.destination_dir}")
        
        return destination_file