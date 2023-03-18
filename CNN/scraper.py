import os
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error

class LinkScraper:

    def __init__(self):
        self.__baseUrl = 'https://edition.cnn.com/'
        self.__countryName = None
        self.__links = []
    
    def __scrape_links(self):
        url = self.__baseUrl + 'world/' + self.__countryName
        req = urllib.request.urlopen(url).read().decode()
        soup = BeautifulSoup(req, features='lxml')
        material = soup.find('section', attrs={'class': 'body tabcontent active'})
        for link in material.findAll('a'):
            self.__links.append(self.__baseUrl + link.get('href'))
    
    def scrape(self, country_name):
        self.__countryName = country_name
        self.__scrape_links()
        return self.__links


class ArticleScraper:

    def __init__(self):
        self.__url = None
        self.__articleText = None
        self.__details = {
            'ExtractionError': False,
            'Headline': None,
            'Author': None,
            'Date': None
        }
    
    def __scrape_article(self):
        try:
            req = urllib.request.urlopen(self.__url).read().decode()
            soup = BeautifulSoup(req, features='lxml')
            mainMaterial = soup.find('div', attrs={'class': 'layout__content-wrapper layout-with-rail__content-wrapper'})
            headline = mainMaterial.find('div', attrs={'class': 'headline__wrapper'}).text.strip()
            author = mainMaterial.find('div', attrs={'class': 'byline'}).text.strip()
            date = mainMaterial.find('div', attrs={'class': 'timestamp'}).text.strip()
            article = mainMaterial.find('div', attrs={'class': 'article__content'})
            requiredText = ""
            pTags = article.findAll('p', attrs={'class': 'paragraph inline-placeholder'})
            for pTag in pTags:
                requiredText = requiredText + pTag.text.strip() + '\n'
            
            self.__details['Headline'] = headline
            self.__details['Author'] = author
            self.__details['Date'] = date
            self.__articleText = requiredText
        
        except:
            self.__details['ExtractionError'] = True

    def scrape(self, url):
        self.__url = url
        self.__scrape_article()
        return self.__details
    
    def save_text(self, file_loc):
        if not self.__details['ExtractionError']:
            try:
                file = open(file_loc, "w")
                file.write(self.__articleText)
            except:
                file = open(file_loc, "wb")
                file.write(self.__articleText.encode('utf-8', 'ignore'))
            file.close()