
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import pandas as pd

#TODO change where your chrome webdriver is
service = Service("C:\\Users\\henle\\Desktop\\chromedriver.exe")

options = webdriver.ChromeOptions()
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")

#TODO Replace "henle" with your user folder name
options.add_argument("user-data-dir=C:\\Users\\henle\\AppData\\Local\\Google\\Chrome\\User Data")

driver = webdriver.Chrome(service=service, options=options)

df = pd.read_csv("comments-data.csv")  
linkedin_urls = df["Profile Links"]
new_links = []  
i = 0
for linkedin_url in linkedin_urls:
    driver.get(linkedin_url)
    linkedin_url = driver.current_url
    new_links.append(linkedin_url)
    print(linkedin_url)

df["Profile Links"] = new_links

df.to_csv("comments-data.csv", index=False)
driver.quit()