# # 1. read data into dataframe
# # 2. call apollo api to get email data
# # 3. write the data into new dataframe with emails

import pandas as pd
import requests
import json
import time
import os
import sys
import datetime
import logging
import re

df = pd.read_csv("comments-data.csv")

linkedin_urls = df["Profile Links"]
names = df["Names"]
emails = []
first_names = []
last_names = []
for index, row in df.iterrows():
    name = row["Names"]
    linkedin_url = row["Profile Links"]
    pattern = r"([A-Z][a-z]+(?: [A-Z][a-z]+)?),? [A-Z]+"
    match = re.search(pattern, name)

    first_name = ""
    last_name = ""
    if match:
        print("First Name:", match.group(1).split()[0])
        print("Last Name:", match.group(1).split()[-1])
        print("Linkedin URL:", linkedin_url)
        first_name = match.group(1).split()[0]
        last_name = match.group(1).split()[-1]
    else:
        print("No match found.")
    


    print("fetching email for: ", linkedin_url)
    # Define the payload

    payload = {"api_key": "35Gb6dnLzB-X5FyWmNunfQ", "linkedin_url": linkedin_url}
    if first_name:
        payload["first_name"] = first_name


    # API endpoint
    url = "https://api.apollo.io/v1/people/match"

    # Headers
    headers = {"Content-Type": "application/json", "Cache-Control": "no-cache"}

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # get the email from te response
        email = response.json()["person"]["email"]
        emails.append(email)
        print(email)
    else:
        emails.append("")
    first_names.append(first_name)
    last_names.append(last_name)

df["Emails"] = emails
df["First Name"] = first_names
#get the first two words of the name
df["Names"] = df["Names"].apply(lambda x: " ".join(x.split()[:2]))

# if name ends in view, remove the last4 characters

df["Names"] = df["Names"].apply(lambda x: x[:-4] if x.endswith("View") else x)

df = df[df["Emails"] != ""]

df.to_csv("comments-data-emails.csv", index=False)

