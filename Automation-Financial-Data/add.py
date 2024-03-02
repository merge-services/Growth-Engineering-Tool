import pandas as pd

df = pd.read_excel("output.xlsx")

# open text file

text = open("input.txt", "r")

# read the file
text = text.read()

# get every two lines
lines = text.strip().split('\n')

cat = df["SNFC"]

# get two lines at a time
for i in range(0, len(lines), 2):
    print(lines[i])
    print(lines[i+1])
    cat[int(lines[i])] = lines[i+1]


df["SNFC"] = cat

# save the file
df.to_excel("output2.xlsx")

