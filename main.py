import json
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

options = webdriver.ChromeOptions()
options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
options.add_argument('--headless')
options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--disable-web-security')
options.add_argument('--disable-site-isolation-trials')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument('--disable-notifications')
options.page_load_strategy = 'eager'

driver = webdriver.Chrome(options=options)

def articleFormatter(article, tag): 
    return {
        "title": article.find("h3").text.strip(),
        "link": article.find("a").get_attribute_list("href")[0],
        "data": article.find("div", class_="date").text.strip(),
        "tag": tag
    }


def getNewsByTags(tags, pages):
    allNews = []

    for tag in tags:
        for page in pages:

            print(f'Buscando notícias com a tag: {tag}')

            driver.get(f"https://www.nsctotal.com.br/tag/{tag}?page={page}")
            
            WebDriverWait(driver, 10).until( EC.presence_of_element_located( (By.CLASS_NAME, "date") ) )
            driver.implicitly_wait(5)
            
            print("Página acessada com sucesso")
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
                        
            news = soup.find_all('div', class_='featured-news-thumb')
            
            parsedNews = [articleFormatter(article, tag) for article in news]

            
            allNews += parsedNews
            print(f"Coletadas mais {len(parsedNews)} notícias, total {len(allNews)}")

    return allNews

def storeAsExcel(data):
    rows = list(map(lambda article: article.values(), data))
    df = pd.DataFrame(rows, columns=["title", "link", "data", "tag"])
    df.to_excel("noticias.xlsx", index=False)


data = getNewsByTags(["tempo", "clima"], range(1,20))

storeAsExcel(data)