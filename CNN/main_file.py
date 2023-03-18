from os import makedirs, path
from time import sleep
from numpy import mean
from pandas import DataFrame, ExcelWriter
from CNN.scraper import LinkScraper, ArticleScraper
from sentiment_analyzer import SentimentAnalyzer


# Main Function
def cnn_extraction():
    curDirectory = 'CNN'
    textDirectory = "ArticleText"
    folderName = path.join(curDirectory, textDirectory)
    makedirs(folderName, exist_ok=True)

    excelFileName = 'Sentiment.xlsx'
    excelFile = path.join(curDirectory, excelFileName)
    writer = ExcelWriter(excelFile, engine='xlsxwriter')

    master_dictionary = 'Loughran-McDonald_MasterDictionary_1993-2021.csv'
    SentimentAnalyzer.define_master_dictionary(master_dictionary)

    # countries = ['americas', 'africa']
    countries = ['americas', 'africa', 'asia', 'china', 'india', 'australia', 'europe', 'middle-east', 'united-kingdom']
    renameCountries = {'americas': 'USA', 'africa': 'AFRICA', 'asia': 'ASIA', 'australia': 'AUSTRALIA', 'china': 'CHINA', 'europe': 'EUROPE', 'india': 'INDIA', 'middle-east': 'MIDDLEEAST', 'united-kingdom': 'UK'}
    
    overallSet = {
        'Country': [],
        'PositiveScore': [],
        'NegativeScore': [],
        'PolarityScore': [],
        'SubjectivityScore': []
    }
    
    for country in countries:
        print("\nCountry - {}".format(country))
        countrySet = {
            'Headline': [],
            'Author': [],
            'Date': [],
            'PositiveScore': [],
            'NegativeScore': [],
            'PolarityScore': [],
            'SubjectivityScore': []
        }
        countryFolder = path.join(folderName, country)
        makedirs(countryFolder, exist_ok=True)

        linkScraper = LinkScraper()
        articleLinks = linkScraper.scrape(country_name=country)

        for (linkNo, articleLink) in enumerate(articleLinks):
            if (linkNo % 5 == 0): sleep(5)
            print("Processing {} {} ......".format(linkNo, articleLink))
            articleScraper = ArticleScraper()
            details = articleScraper.scrape(url=articleLink)
            if not details['ExtractionError']:
                fileName = str(linkNo) + '.txt'
                fileLoc = path.join(countryFolder, fileName)
                articleScraper.save_text(file_loc=fileLoc)
                sentimentAnalyzer = SentimentAnalyzer()
                scores = sentimentAnalyzer.analyze(file_loc=fileLoc)
                countrySet['Headline'].append(details['Headline'])
                countrySet['Author'].append(details['Author'])
                countrySet['Date'].append(details['Date'])
                countrySet['PositiveScore'].append(scores['PositiveScore'])
                countrySet['NegativeScore'].append(scores['NegativeScore'])
                countrySet['PolarityScore'].append(scores['PolarityScore'])
                countrySet['SubjectivityScore'].append(scores['SubjectivityScore'])

        countryDataset = DataFrame(countrySet)
        sheetName = renameCountries.get(country, country)
        countryDataset.to_excel(writer, sheet_name=sheetName, index=False, na_rep='NaN', float_format="%.2f")

        for column in countryDataset:
            column_width = int(max(countryDataset[column].astype(str).map(len).max(), len(column)))
            col_idx = countryDataset.columns.get_loc(column)
            writer.sheets[sheetName].set_column(col_idx, col_idx, column_width)
        
        overallSet['Country'].append(sheetName)
        overallSet['PositiveScore'].append(mean(countrySet['PositiveScore']))
        overallSet['NegativeScore'].append(mean(countrySet['NegativeScore']))
        overallSet['PolarityScore'].append(mean(countrySet['PolarityScore']))
        overallSet['SubjectivityScore'].append(mean(countrySet['SubjectivityScore']))
    
    overallDataset = DataFrame(overallSet)
    sheetName = 'OVERALL'
    overallDataset.to_excel(writer, sheet_name=sheetName, index=False, na_rep='NaN', float_format="%.2f")

    for column in overallDataset:
        column_width = int(max(overallDataset[column].astype(str).map(len).max(), len(column)))
        col_idx = overallDataset.columns.get_loc(column)
        writer.sheets[sheetName].set_column(col_idx, col_idx, column_width)

    writer.save()
    return overallDataset
