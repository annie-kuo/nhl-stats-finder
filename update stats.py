import pandas as pd
import numpy as np
import math
from urllib.request import urlopen
from datetime import datetime

root = "https://statsapi.web.nhl.com"
filename = "nhl_stats.xlsx"

p_df = pd.read_excel(filename, sheet_name='Players IDs', engine="openpyxl")
t_df = pd.read_excel(filename, sheet_name='Teams IDs', engine="openpyxl")

# check if last two rows are relevant
l = len(p_df)
penult = p_df.iat[l-2, 0]
ult = p_df.iat[l-1, 0]

if ((isinstance(penult, float) and math.isnan(penult))
    or (isinstance(ult, str) and 'Last updated' in ult)):
    p_df = p_df.drop([l-1, l-2])

# get player stats
i = 1


for i in range(0, len(p_df)):
    
    # ignore goalies
    if p_df.iat[i, 3] == "G":
        continue
    
    player_url = root+p_df.iat[i, 2]+ "/stats?stats=statsSingleSeason&season=20222023"
    page = urlopen(player_url)
    p_html_bytes = page.read()
    p_html = p_html_bytes.decode("utf-8")
    
    # parse data
    p_info = p_html.split('\n')
    
    if p_info[13] == '}':
        continue
    
    p_df.iat[i, 4] = p_info[19][-3:-1].strip()
    p_df.iat[i, 5] = p_info[16][-3:-1].strip()
    p_df.iat[i, 6] = p_info[15][-3:-1].strip()
    p_df.iat[i, 7] = p_info[35][-4:-1].strip().strip(":")

# add timestamp to the update
now = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
timestamp = "Last updated: " + now
update_info = pd.DataFrame({'Player' : ["", timestamp]})
p_df = p_df.append(update_info)

writer = pd.ExcelWriter(filename, engine = 'xlsxwriter')
t_df.to_excel(writer, sheet_name = 'Teams IDs', index = False)
p_df.to_excel(writer, sheet_name = 'Players IDs', index = False)

# quit
writer.close()