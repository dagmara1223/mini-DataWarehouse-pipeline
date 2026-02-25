from src.extract import DataExtractor
from src.transform import DataTransformer

def main():
    # extract = DataExtractor(source_dir='data/source', destination_dir='data/raw')
    # data = extract.extract_csv("Amazon_Sale_Report.csv")
    # data_transformer = DataTransformer(data)
    # df = data_transformer.transform_to_DataFrame()

    data_transformer = DataTransformer("data/raw/Amazon_Sale_Report_20260225_151140.csv")
    # Load DataFrame 
    df = data_transformer.transform_to_DataFrame()
    
    #Clear all null rows
    df_cleaned = data_transformer.clean_all_nulls(df)

    print(df_cleaned.head(5))

if __name__=='__main__':
    main()