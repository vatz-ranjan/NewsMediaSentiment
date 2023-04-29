from warnings import filterwarnings
import os
import nltk
from pandas import DataFrame, ExcelWriter, read_excel
from NM_CNN.main_file import cnn_extraction, cnn_temp
from NM_ALJAZEERA.main_file import aljazeera_extraction
from NM_BBC.main_file import bbc_extraction, bbc_temp
from items import excelFileName, sheetName


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
    newsMedia = lambda name: print("*"*40, f"{name}", "*"*40, sep="\n")
    
    '''
    try:
        newsMedia("CNN")
        cnn_extraction()
    except: 
        pass
    
    try: 
        newsMedia("Al-Jazeera")
        aljazeera_extraction()
    except: 
        pass
    
    try: 
        newsMedia("BBC")
        bbc_extraction()
    except: 
        pass
    
    '''
    nameToDataset = []
    rootdir = os.getcwd()
    dirs = os.listdir(rootdir)

    for dir in dirs:
        if dir.startswith('NM_'):
            folderPath = os.path.join(rootdir, dir)
            try:
                filePath = os.path.join(folderPath, excelFileName)
                dataSet = read_excel(filePath, sheet_name=sheetName)
                nameToDataset.append((dir[3:], dataSet))
            except:
                pass

    excelFile = 'NewsMediaSentiment.xlsx'
    writer = ExcelWriter(excelFile, engine='xlsxwriter')
    generate_excel(writer=writer, sheetNameToDataset=nameToDataset)
    # generate_ad_excel(writer=writer, nameToDataset=nameToDataset)
    writer.save()
    # '''

'''
    # If Newly Installed NLTK Library
    nltk.download('punkt')
    nltk.download(["names", "stopwords"])
    nltk.download(['wordnet', 'omw-1.4'])
'''