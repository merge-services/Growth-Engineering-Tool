import configparser
import pandas as pd
from openai import AsyncOpenAI, OpenAI
import asyncio

import time
config = configparser.ConfigParser()
config.read("config.ini")

API_KEY = config["API"]["API_KEY"]
PROMPT = "Categorize the  transaction description into the following categories, replying with just the category name:"
PROMPT2 = "Here is the transaction description: "

# open xlsx file
df = pd.read_excel("data.xlsx")

catergory = pd.read_excel("categories.xlsx")

# covert the column to a comma separated string
catergories_str = catergory["GL Accounts"].str.cat(sep=", ")


description = df["Descriptions  Clean "]


out_description = df["SNFC"]

# test the first row
print(description[0])




client = OpenAI(api_key=API_KEY, timeout=60, max_retries=2)

def openai_request(i, description):
    chat_completion =  client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": PROMPT2 + description + PROMPT + catergories_str,
        }
    ],
    model="gpt-3.5-turbo-0125",
    )
    print(chat_completion)
    print(chat_completion.choices[0].message.content)
    out_description[i] = chat_completion.choices[0].message.content




for i in range(0, len(description)):
    print(i)
    time.sleep(0.1) #bypass rate limit for now, can be adjusted
    openai_request(i, description[i])


### TRIED ASYNC BUT IT HAD RATE LIMITING ISSUES
# client = AsyncOpenAI(api_key=API_KEY)

# print(PROMPT2 + description[0] + PROMPT + catergories_str)

# async def openai_request(i, description):
#     chat_completion = await client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": PROMPT2 + description + PROMPT + catergories_str,
#         }
#     ],
#     model="gpt-3.5-turbo-0125",
#     )
#     out_description[i] = chat_completion.choices[0].message.content




# async def main():
#     tasks = []
#     for i in range(len(description)):
#         time.sleep(0.1)
#         print(i)
#         tasks.append(openai_request(i, description[i]))

#     await asyncio.gather(*tasks)

# asyncio.run(main())

print(description)
print(out_description)

# save the output to a new xlsx file
df["SNFC"] = out_description


df.to_excel("output3.xlsx")
