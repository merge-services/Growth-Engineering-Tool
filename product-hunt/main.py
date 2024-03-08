import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver

BY = By
import pandas as pd
from playsound import playsound
import random
import pyautogui as mouse
import re
import os


### SETTINGS ===================
use_product_hunt = False
links = ['snackpass.co']

use_limit = False
employee_min, employee_max = 0, 1000

founder_keywords = [
        "founder",
        "co-founder",
        "cofounder",
        "ceo",
        "chief executive officer"]

product_heads_keywords = [
        "head of product",
        "chief product officer",
        "VP of product",
        "product"
        ]

### END SETTINGS ===================

if use_product_hunt:
    URL = "https://www.producthunt.com/categories/team-collaboration"

    chrome_options = Options()
    chrome_options.add_argument("--auto-open-devtools-for-tabs")

    # make window skinny to make links show up
    chrome_options.add_argument("--window-size=300,1080")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(URL)


    time.sleep(3)
    # get all links
    links = driver.find_elements(
        BY.XPATH,
        "//*[contains(@class, 'color-dark-grey') and contains(@class, 'fontSize-16') and contains(@class, 'fontWeight-400')]",
    )

    # remove ref links
    links = [link.get_attribute("href").split("?")[0] for link in links]

    # remove links that are not product links
    links = [link for link in links if "producthunt" not in link]

# print(links)



##apollo part
import requests
import json

product_map = {links: {"founders": [], "product_heads": []} for links in links}



for link in links:
    ## call apollo api

    payload = {"api_key": "hxR8ka6QMNh_E-us3yaMtQ", "domain": link}

    # company size check

    url = "https://api.apollo.io/v1/organizations/enrich"
    headers = {"Content-Type": "application/json", "Cache-Control": "no-cache"}

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    print(response.json())
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # get the email from te response
        #print(response.json())
        response = response.json()
        number_of_employees = response["organization"]["estimated_num_employees"]
        if not use_limit:
            pass
        elif  number_of_employees > employee_max and number_of_employees < employee_min:
            print("company size check passed")
        else:
            print("company size check failed")
            continue
    else:
        print("company size check api failed")
        continue
    # search everyone in the company

    # API endpoint

    payload = {"api_key": "hxR8ka6QMNh_E-us3yaMtQ", "q_organization_domains": link}

    url = "https://api.apollo.io/v1/mixed_people/search"

    # Headers
    headers = {"Content-Type": "application/json", "Cache-Control": "no-cache"}

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # get the email from te response
        response = response.json()
        people = response["people"]




        for person in people:
            # check if the person is a founder

            if person["title"] and any(
                keyword in person["title"].lower() for keyword in founder_keywords
            ):
                #add the enitre json to the list
                product_map[link]["founders"].append(person)
            elif person["title"] and any(
                    keyword in person["title"].lower() for keyword in product_heads_keywords
                ): 
                product_map[link]["product_heads"].append(person)

#export product map to json
                
with open(f'product_map_{link}.json', 'w') as f:
    json.dump(product_map, f, indent=4)


        
