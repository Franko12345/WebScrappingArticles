from sys import executable
from bs4 import BeautifulSoup
try:
    from selenium import webdriver

    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    import pandas as pd
except:
    print("Configurando ambiente")
    import os
    os.system("pip install --upgrade selenium wget pandas openpyxl")
    import wget
    import zipfile
    
    if "chromedriver" not in os.listdir():
        print("Downloading chromedriver")
        filename = wget.download("https://storage.googleapis.com/chrome-for-testing-public/132.0.6834.159/win64/chrome-win64.zip")
        with zipfile.ZipFile(f"./{filename}", 'r') as zip_ref:
            zip_ref.extractall("./chromedriver")
    else:
        print("Chromedrive found")
    
    from selenium import webdriver
    from selenium.webdriver.support.wait import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    import pandas as pd

options = webdriver.ChromeOptions()

options.binary_location = "./chromedriver/chrome-win64/chrome.exe"

options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-web-security')
options.add_argument('--disable-site-isolation-trials')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument('--disable-notifications')
options.page_load_strategy = 'eager'

driver = webdriver.Chrome(options=options)

print(driver.service.path+"\n")

def articleFormatter(article, tag): 
    return {
        "title": article.find("h3").text.strip(),
        "link": article.find("a").get_attribute_list("href")[0],
        "data": article.find("div", class_="date").text.strip(),
        "tag": tag
    }


def SCfilter(article):
    cidades_sc1 = pd.read_excel('./planilhas/cidade_sc1.xlsx')
    
    for key in [" sc ", "santa catarina", " sc", "sc "]:
        if key in article["title"].lower():
            return True
        
        
    for key in ["-sc-", "santa-catarina", "-sc", "sc-"]:
        if key in article["link"].split("/")[-1].lower():
            return True

    for cidade in cidades_sc1["MUNICIPIO"]:
        if cidade.lower() in article["title"].lower() or cidade.lower() in article["link"].split("/")[-1].lower():
            return True

    return False

def getNewsByTags(tags):
    allNews = []

    pageCounter = 0
    for tag in tags.keys():
        for page in range(tags[tag]):
            if pageCounter % 10 == 0:
                print(f"\nPlanilha salva com {len(allNews)} notícias para backup...")
                storeAsExcel(allNews)
                print("Salvo\n")
                
            driver.get(f"https://www.nsctotal.com.br/tag/{tag}?page={page}")
            try:
                WebDriverWait(driver, 10).until( EC.presence_of_element_located( (By.CLASS_NAME, "date") ) )
                driver.implicitly_wait(5)
            except:
                continue            
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            news = soup.find_all('div', class_='featured-news-thumb')
            
            parsedNews = [articleFormatter(article, tag) for article in news]

            parsedNews = list(filter(SCfilter, parsedNews))
            
            allNews += parsedNews
            print(f"\nNoticias coletadas: {len(parsedNews)}\nTag: {tag}\nPágina:{page}\nTotal: {len(allNews)}\n")

            pageCounter += 1
        
        
            
    return allNews

def storeAsExcel(data):
    rows = list(map(lambda article: article.values(), data))
    df = pd.DataFrame(rows, columns=["title", "link", "data", "tag"])
    
    print(f"Número de noticias com duplicados: {len(df)}")
    
    df = df.drop("tag", axis=1)
    df = df.drop_duplicates()
    
    print(f"Número de noticias sem duplicados: {len(df)}")
    
    df.to_excel("./planilhas/noticias.xlsx", index=False)
    

searchReference = {
    "chuvas": 52,
    "chuva em sc": 35,
    "chuvas em sc": 60,
    "chuva": 395,
    "chuva forte": 5,
    "chuvarada": 11,
    "temporal": 109,
    "tempestade": 21,
    "ciclone": 32,
    "ciclone bomba": 5,
    "ciclone extratropical": 6,
    "previsao do tempo": 708,
    "frente fria": 9,
    "enchente": 92,
    "enchentes": 22,
    "alagamento": 61,
    "alagamentos": 20,
    "deslizamento": 36,
    "deslizamentos": 9,
    "deslizamento de terra": 5
}

searchReference = {tag.replace(" ", "-"): searchReference[tag] for tag in searchReference}
#teste
print(searchReference)
 
# data = getNewsByTags(searchReference)

# print(data)

# storeAsExcel(data)

