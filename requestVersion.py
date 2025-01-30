import json
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions()
options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
# options.add_argument('--headless')
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

def articleFormatter(article): 
    return {
        "title": article.find("h3").text.strip(),
        "link": article.find("a").get_attribute_list("href")[0],
        "data": article.find("div", class_="date").text.strip(),
    }


def getNewsByTags(tags, pages):
    allNews = {tag:[] for tag in tags}
    for page in pages:
        for tag in tags:
            print(f'Buscando notícias com a tag: {tag}')
            pageNews = requests.get(f"https://www.nsctotal.com.br/tag/{tag}?page={page}")
            
            if pageNews.status_code == 200:
                print("Página acessada com sucesso")
                soup = BeautifulSoup(pageNews.content, 'html.parser')
                            
                news = soup.find_all('div', class_='featured-news-thumb')
                
                parsedNews = [articleFormatter(article) for article in news]

                print(parsedNews)
                
                allNews[tag] += parsedNews
            else:
                print(f'Erro ao acessar a página {page}, status: {pageNews.status_code}')

    return allNews


data = getNewsByTags(["tempo", "clima"], range(1,5))

print(json.dumps(data, indent=2))