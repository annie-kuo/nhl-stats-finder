import pandas as pd
import numpy as np
from urllib.request import urlopen

# retrieve stats
root = "https://statsapi.web.nhl.com"
filename = "nhl_stats.xlsx"

df = pd.read_excel(filename, sheet_name='Players IDs', engine="openpyxl")
df = df.set_index('Player')



# get user requests
names=[]

i = input("Enter the name of a player: ")
while (len(i) > 1) :
    names.append(i.title())
    i = input("Enter the name of a player: ")

rs = df.query('Player == @names')
rs.drop("Link", axis=1, inplace=True)
rs = rs.sort_values(by=["G", "A"], ascending=False)


print(rs)