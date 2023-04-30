from os import makedirs, path
from time import sleep
from copy import deepcopy
from numpy import mean
from pandas import DataFrame, ExcelWriter
from NM_ALJAZEERA.scraper import LinkScraper, ArticleScraper
from sentiment_analyzer import SentimentAnalyzer
from items import textDirectory, excelFileName, master_dictionary, sheetName, overallDatasetStruct, countryDatasetStruct


# Main Function
def aljazeera_extraction():
    curDirectory = 'NM_ALJAZEERA'
    folderName = path.join(curDirectory, textDirectory)
    makedirs(folderName, exist_ok=True)

    excelFile = path.join(curDirectory, excelFileName)
    writer = ExcelWriter(excelFile, engine='xlsxwriter')

    SentimentAnalyzer.define_master_dictionary(master_dictionary)

    countries = ['united-states', 'canada', 'israel', 'qatar', 'turkey', 'saudi-arabia', 'united-arab-emirates', 'iraq', 'iran', 'china', 'india', 'pakistan', 'japan', 'taiwan', 'north-korea', 'south-korea', 'australia', 'russia', 'united-kingdom', 'germany', 'france']
    renameCountries = {'united-states': 'USA', 'canada': 'CANADA', 'israel': 'ISRAEL', 'qatar': 'QATAR', 'turkey': 'TURKEY', 'saudi-arabia': 'SAUDI_ARABIA', 'united-arab-emirates': 'UAE', 'iraq': 'IRAQ', 'iran': 'IRAN', 'china': 'CHINA', 'india': 'INDIA', 'pakistan': 'PAKISTAN', 'japan': 'JAPAN', 'taiwan': 'TAIWAN', 'north-korea': 'NORTH_KOREA', 'south-korea': 'SOUTH_KOREA', 'australia': 'AUSTRALIA', 'russia': 'RUSSIA', 'united-kingdom': 'UK', 'germany': 'GERMANY', 'france': 'FRANCE'}
    
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


def temp():
    articleLink = 'https://www.aljazeera.com/news/2023/3/5/at-cpac-forum-trump-shows-why-he-will-be-tough-to-topple'
    articleScraper = ArticleScraper()
    details = articleScraper.scrape(url=articleLink)
    print(details)