textDirectory = "ArticleText"

excelFileName = 'Sentiment.xlsx'

master_dictionary = 'Loughran-McDonald_MasterDictionary_1993-2021.csv'

sheetName = 'OVERALL'

extractionDetailsStruct = {
            'ExtractionError': False,
            'Headline': None,
            'SubTitle': None,
            'Author': None,
            'Date': None
        }

overallDatasetStruct = {
        'Country': [],
        'PositiveScore': [],
        'NegativeScore': [],
        'PolarityScore': [],
        'SubjectivityScore': []
    }

countryDatasetStruct = {
            'Headline': [],
            'URL': [],
            'Author': [],
            'Date': [],
            'PositiveScore': [],
            'NegativeScore': [],
            'PolarityScore': [],
            'SubjectivityScore': []
        }