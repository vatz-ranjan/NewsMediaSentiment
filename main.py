from warnings import filterwarnings
import nltk
from pandas import DataFrame, ExcelWriter
from CNN.main_file import cnn_extraction, temp
from ALJAZEERA.main_file import aljazeera_extraction, temp


def generate_excel(writer, sheetNameToDataset):
    for (sheetName, dataset) in sheetNameToDataset:
        dataset.to_excel(writer, sheet_name=sheetName, index=False, na_rep='NaN', float_format="%.2f")

        for column in dataset:
            column_width = int(max(dataset[column].astype(str).map(len).max(), len(column)))
            col_idx = dataset.columns.get_loc(column)
            writer.sheets[sheetName].set_column(col_idx, col_idx, column_width)


def generate_ad_excel(writer, nameToDataset):
    pass


if __name__ == '__main__':

    filterwarnings('ignore')

    try:
        cnnSet = cnn_extraction()
    except: 
        cnnSet = DataFrame()
    
    try: 
        aljazeeraSet = aljazeera_extraction()
    except: 
        aljazeeraSet = DataFrame()
    
    nameToDataset = (('CNN', cnnSet), ('ALJAZEERA', aljazeeraSet))

    excelFile = 'NewsMediaSentiment.xlsx'
    writer = ExcelWriter(excelFile, engine='xlsxwriter')
    generate_excel(writer=writer, sheetNameToDataset=nameToDataset)
    # generate_ad_excel(writer=writer, nameToDataset=nameToDataset)
    writer.save()
    '''
    # If Newly Installed NLTK Library
    nltk.download('punkt')
    nltk.download(["names", "stopwords"])
    nltk.download(['wordnet', 'omw-1.4'])
    '''