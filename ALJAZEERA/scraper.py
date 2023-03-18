import os
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

class LinkScraper:

    def __init__(self):
        self.__baseUrl = 'https://www.aljazeera.com/where/'
        self.__driverPath = None
        self.__countryName = None
        self.__links = []
    
    def __scrape_links(self):
        url = self.__baseUrl + self.__countryName
        driver = webdriver.Chrome(self.__driverPath)
        driver.get(url)
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'ot-sdk-container')))
            cookiesSection = driver.find_element(by=By.CLASS_NAME, value='ot-sdk-container')
            acceptCookies = cookiesSection.find_element(by=By.ID, value='onetrust-accept-btn-handler')
            acceptCookies.click()
        except Exception as e:
            print(e)
        sleep(5)
        # driver.find_element(by=By.CLASS_NAME, value='show-more-button big-margin')
        soup = BeautifulSoup(driver.page_source, features='html.parser')
        firstMainMaterial = soup.find('main', attrs={'id': 'featured-news-container'})
        for element in firstMainMaterial.findAll('li', attrs={'class': 'featured-articles-list__item'}):
            self.__links.append('https://www.aljazeera.com' + element.find('a').get('href'))

        secondMainMaterial = soup.find('section', attrs={'id': 'news-feed-container'})
        for element in secondMainMaterial.findAll('article', attrs={'class': 'gc u-clickable-card gc--type-post gc--list gc--with-image'}):
            self.__links.append('https://www.aljazeera.com' + element.find('a').get('href'))
    
    def scrape(self, country_name, driver_path='D:/Application/ChromeDriver/chromedriver.exe'):
        self.__countryName = country_name
        self.__driverPath = driver_path
        self.__scrape_links()
        return self.__links


class ArticleScraper:

    def __init__(self):
        self.__url = None
        self.__articleText = None
        self.__details = {
            'ExtractionError': False,
            'Headline': None,
            'SubTitle': None,
            'Source': None,
            'Date': None
        }
    
    def __scrape_article(self):
        try:
            req = urllib.request.urlopen(self.__url).read().decode()
            soup = BeautifulSoup(req, features='lxml')
            mainMaterial = soup.find('main', attrs={'id': 'main-content-area'})
            header = mainMaterial.find('header', attrs={'class': 'article-header'})
            headline = header.find('h1').text.strip()
            sub_title = header.find('p', attrs={'class': 'article__subhead css-1wt8oh6'}).text.strip()
            source = mainMaterial.find('div', attrs={'class': 'article-source'}).text.strip()
            date = mainMaterial.find('div', attrs={'class': 'article-dates'}).find('span').text.strip()
            article = mainMaterial.find('div', attrs={'class': 'wysiwyg wysiwyg--all-content css-ibbk12'})
            requiredText = ""
            pTags = article.findAll('p')
            for pTag in pTags:
                requiredText = requiredText + pTag.text.strip() + '\n'
            
            self.__details['Headline'] = headline
            self.__details['SubTitle'] = headline
            self.__details['Source'] = source
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