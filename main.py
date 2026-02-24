from src.extract import DataExtractor

def main():
    extract = DataExtractor(source_dir='data/source', destination_dir='data/raw')
    extract.extract_csv("Amazon_Sale_Report.csv")

if __name__=='__main__':
    main()