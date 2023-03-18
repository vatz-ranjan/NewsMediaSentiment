from os import makedirs, path
from time import sleep
from numpy import mean
from pandas import DataFrame, ExcelWriter
from ALJAZEERA.scraper import LinkScraper, ArticleScraper
from sentiment_analyzer import SentimentAnalyzer


# Main Function
def aljazeera_extraction():
    curDirectory = 'ALJAZEERA'
    textDirectory = "ArticleText"
    folderName = path.join(curDirectory, textDirectory)
    makedirs(folderName, exist_ok=True)

    excelFileName = 'Sentiment.xlsx'
    excelFile = path.join(curDirectory, excelFileName)
    writer = ExcelWriter(excelFile, engine='xlsxwriter')

    master_dictionary = 'Loughran-McDonald_MasterDictionary_1993-2021.csv'
    SentimentAnalyzer.define_master_dictionary(master_dictionary)

    # countries = ['united-states', 'canada']
    countries = ['united-states', 'canada', 'israel', 'qatar', 'turkey', 'saudi-arabia', 'united-arab-emirates', 'iraq', 'iran', 'china', 'india', 'pakistan', 'japan', 'taiwan', 'north-korea', 'south-korea', 'australia', 'russia', 'united-kingdom', 'germany', 'france']
    renameCountries = {'united-states': 'USA', 'canada': 'CANADA', 'israel': 'ISRAEL', 'qatar': 'QATAR', 'turkey': 'TURKEY', 'saudi-arabia': 'SAUDIARABIA', 'united-arab-emirates': 'UAE', 'iraq': 'IRAQ', 'iran': 'IRAN', 'china': 'CHINA', 'india': 'INDIA', 'pakistan': 'PAKISTAN', 'japan': 'JAPAN', 'taiwan': 'TAIWAN', 'north-korea': 'NORTHKOREA', 'south-korea': 'SOUTHKOREA', 'australia': 'AUSTRALIA', 'russia': 'RUSSIA', 'united-kingdom': 'UK', 'germany': 'GERMANY', 'france': 'FRANCE'}

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
            'SubTitle': [],
            'Source': [],
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
                countrySet['SubTitle'].append(details['SubTitle'])
                countrySet['Source'].append(details['Source'])
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


def temp():
    articleLink = 'https://www.aljazeera.com/news/2023/3/5/at-cpac-forum-trump-shows-why-he-will-be-tough-to-topple'
    articleScraper = ArticleScraper()
    details = articleScraper.scrape(url=articleLink)
    print(details)