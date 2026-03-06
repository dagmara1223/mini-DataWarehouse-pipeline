from src.extract import DataExtractor
from src.transform import DataTransformer
from src.to_dataframe import CSVReader

def main():
    # extract = DataExtractor(source_dir='data/source', destination_dir='data/raw')
    # data = extract.extract_csv("Amazon_Sale_Report.csv")
    # data_reader = CSVReader(data)

    data_reader = CSVReader("data/raw/Amazon_Sale_Report_20260225_151140.csv")
    # Load DataFrame 
    df = data_reader.to_df()
    
    # create data copy
    df_copy = df.copy()
    
    transformer = DataTransformer()
    df_transformed = transformer.main_transform(df_copy)
    print(df_transformed.columns)

if __name__=='__main__':
    main()