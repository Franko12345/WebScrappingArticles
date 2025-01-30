import json
from regex import D
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
import requests

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = webdriver.ChromeOptions()
options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
options.page_load_strategy = 'eager'
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

driver.get("https://www.nsctotal.com.br/tag/tempo?page=1")


try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "date"))
    )
    print(element)
finally:
    driver.quit()
