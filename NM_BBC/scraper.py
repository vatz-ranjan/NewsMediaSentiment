import os
from copy import deepcopy
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
from items import extractionDetailsStruct

class LinkScraper:

    def __init__(self):
        self.__baseUrl = 'https://www.bbc.com'
        self.__countryName = None
        self.__links = []
    
    def __scrape_links(self):
        newsSource = '/news/world/'
        country = self.__countryName.find('_')
        url = self.__baseUrl + newsSource + self.__countryName
        req = urllib.request.urlopen(url).read().decode()
        soup = BeautifulSoup(req, features='lxml')
        mainMaterial = soup.find('div', attrs={'id': 'site-container'})
        material = mainMaterial.find('div', attrs={'id': 'index-page'})
        topContent = material.find('div', attrs={'id': 'topos-component'}).find('div', attrs={'class': 'mpu-available'})
        middleContents = material.findAll('div', attrs={'class': 'nw-c-5-slice gel-layout gel-layout--equal b-pw-1280'})
        childrens = mainMaterial.children
        childrens = list(childrens)
        endContent = childrens[5]

        firstLink = topContent.find('div', attrs={'class': 'b-pw-1280 gel-layout'}).find('a').get('href')
        if firstLink.startswith(newsSource[:-1] + '-' + self.__countryName[:country]):
            self.__links.append(self.__baseUrl + firstLink)

        secondPart = topContent.find('div', attrs={'class': 'gel-layout gel-layout--equal'})
        for tag in secondPart.findAll('a'):
            curLink = tag.get('href')
            if curLink.startswith(newsSource[:-1] + '-' + self.__countryName[:country]):
                self.__links.append(self.__baseUrl + curLink)

        for middleContent in middleContents:
            for tag in middleContent.findAll('a'):
                curLink = tag.get('href')
                if curLink.startswith(newsSource[:-1] + '-' + self.__countryName[:country]):
                    self.__links.append(self.__baseUrl + curLink)

        lastPart = endContent.find('div', attrs={'id': 'lx-stream'}).find('ol')
        for tag in lastPart.findAll('li'):
            try:
                curLink = tag.find('article').find('a').get('href')
                if curLink.startswith(newsSource[:-1] + '-' + self.__countryName[:country]):
                    self.__links.append(self.__baseUrl + curLink)
            except: pass
    
    def scrape(self, country_name):
        self.__countryName = country_name
        self.__scrape_links()
        return self.__links


class ArticleScraper:

    def __init__(self):
        self.__url = None
        self.__articleText = None
        self.__details = deepcopy(extractionDetailsStruct)
    
    def __scrape_article(self):
        try:
            req = urllib.request.urlopen(self.__url).read().decode()
            soup = BeautifulSoup(req, features='lxml')
            mainMaterial = soup.find('main', attrs={'id': 'main-content'})
            header = mainMaterial.find('header', attrs={'class': 'ssrcss-1eqcsb1-HeadingWrapper e1nh2i2l5'})
            headline = header.text.strip()
            author = mainMaterial.find('div', attrs={'class': 'ssrcss-1bdte2-BylineComponentWrapper e8mq1e90'}).text.strip()
            date = mainMaterial.find('time').text.strip()
            article = mainMaterial.findAll('div', attrs={'class': 'ssrcss-11r1m41-RichTextComponentWrapper ep2nwvo0'})
            requiredText = ""
            for pTag in article:
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