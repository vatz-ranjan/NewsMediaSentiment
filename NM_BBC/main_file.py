from os import makedirs, path
from time import sleep
from copy import deepcopy
from numpy import mean
from pandas import DataFrame, ExcelWriter
from NM_BBC.scraper import LinkScraper, ArticleScraper
from sentiment_analyzer import SentimentAnalyzer
from items import textDirectory, excelFileName, master_dictionary, sheetName, overallDatasetStruct, countryDatasetStruct


# Main Function
def bbc_extraction():
    curDirectory = 'NM_BBC'
    folderName = path.join(curDirectory, textDirectory)
    makedirs(folderName, exist_ok=True)

    excelFile = path.join(curDirectory, excelFileName)
    writer = ExcelWriter(excelFile, engine='xlsxwriter')

    SentimentAnalyzer.define_master_dictionary(master_dictionary)

    countries = ['africa', 'asia', 'australia', 'europe', 'latin_america', 'middle_east', 'us_and_canada']
    renameCountries = {'us_and_canada': 'USA-CANADA', 'africa': 'AFRICA', 'asia': 'ASIA', 'australia': 'AUSTRALIA', 'europe': 'EUROPE', 'middle_east': 'MIDDLE_EAST', 'latin_america': 'LATIN_AMERICA', 'europe': 'EUROPE'}
    
    overallSet = deepcopy(overallDatasetStruct)
    
    for country in countries:
        countryName = renameCountries.get(country, country)
        print("\nCountry - {}".format(countryName))
        
        countryFolder = path.join(folderName, countryName)
        makedirs(countryFolder, exist_ok=True)

        countrySet = deepcopy(countryDatasetStruct)
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
                countrySet['URL'].append(articleLink)
                countrySet['Author'].append(details['Author'])
                countrySet['Date'].append(details['Date'])
                countrySet['PositiveScore'].append(scores['PositiveScore'])
                countrySet['NegativeScore'].append(scores['NegativeScore'])
                countrySet['PolarityScore'].append(scores['PolarityScore'])
                countrySet['SubjectivityScore'].append(scores['SubjectivityScore'])

        countryDataset = DataFrame(countrySet)
        countryName = renameCountries.get(country, country)
        countryDataset.to_excel(writer, sheet_name=countryName, index=False, na_rep='NaN', float_format="%.2f")

        for column in countryDataset:
            column_width = int(max(countryDataset[column].astype(str).map(len).max(), len(column)))
            col_idx = countryDataset.columns.get_loc(column)
            writer.sheets[countryName].set_column(col_idx, col_idx, column_width)
        
        overallSet['Country'].append(countryName)
        overallSet['PositiveScore'].append(mean(countrySet['PositiveScore']))
        overallSet['NegativeScore'].append(mean(countrySet['NegativeScore']))
        overallSet['PolarityScore'].append(mean(countrySet['PolarityScore']))
        overallSet['SubjectivityScore'].append(mean(countrySet['SubjectivityScore']))
    
    overallDataset = DataFrame(overallSet)
    overallDataset.to_excel(writer, sheet_name=sheetName, index=False, na_rep='NaN', float_format="%.2f")

    for column in overallDataset:
        column_width = int(max(overallDataset[column].astype(str).map(len).max(), len(column)))
        col_idx = overallDataset.columns.get_loc(column)
        writer.sheets[sheetName].set_column(col_idx, col_idx, column_width)

    writer.save()


def bbc_temp():
    articleLink = 'https://www.bbc.com/news/world-asia-india-65134372'
    articleLink = 'https://www.bbc.com/news/world-us-canada-65150138'
    countries = ['africa', 'asia', 'australia', 'europe', 'latin_america', 'middle_east', 'us_and_canada']
    
    for country in countries:
        print("\nCountry - {}".format(country))
        linkScraper = LinkScraper()
        articleLinks = linkScraper.scrape(country_name=country)
        articleScraper = ArticleScraper()
        details = articleScraper.scrape(url=articleLinks[1])
        print(details)