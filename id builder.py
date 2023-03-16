import pandas as pd
import numpy as np
from urllib.request import urlopen

root = "https://statsapi.web.nhl.com"
path = "nhl_stats.xlsx"
writer = pd.ExcelWriter(path, engine = 'xlsxwriter')





# TEAMS
t_cols = ["Team", "ID", "Link"]
t_df = pd.DataFrame(columns = t_cols)

teams_url = "/api/v1/teams"
page = urlopen(root+teams_url)
t_html_bytes = page.read()
t_html = t_html_bytes.decode("utf-8")

# parse data
t_info = t_html.split('\n')
del t_info[0:3]

count = 1
i = 0

while i+2 < len(t_info):
    # retrieve info
    t_id = t_info[i][-3:-1].strip()
    t_name = t_info[i+1][14:-2]
    t_link = t_info[i+2][14:-2]
    
    # add info
    new_row = {'Team': t_name, 'ID': t_id, 'Link': t_link}
    t_df = t_df.append(new_row, ignore_index = True)
    
    # update pointer
    if count in [1,2,10,13,25,26,30]:
        i += 39
    else:
        i += 40
    count += 1

# write into the excel file
t_df.to_excel(writer, sheet_name = 'Teams IDs', index = False)





# PLAYERS
p_cols = ["Player", "ID", "Link", "Position"]
p_df = pd.DataFrame(columns = p_cols)

# get players' ids
i = 0


while i < len(t_df):
    roster_url = root+t_df.iat[i, 2]+"/roster"
    page = urlopen(roster_url)
    r_html_bytes = page.read()
    r_html = r_html_bytes.decode("utf-8")
    
    # parse data
    r_info = r_html.split('\n')
    del r_info[0:4]
    
    j = 0
    count = 1
    
    while j+2 < len(r_info):     
        # retrieve info
        p_id = r_info[j][-9:-1].strip()
        p_name = r_info[j+1][20:-2]
        p_link = r_info[j+2][16:-1]
        p_pos = r_info[j+9][-3:-1].strip("\"")
    
        # add info
        new_row = {'Player': p_name, 'ID': p_id, 'Link': p_link, 'Position': p_pos}
        p_df = p_df.append(new_row, ignore_index = True)
    
        # update pointer
        j += 13
        count += 1
    i += 1

# write into the excel file
p_df.to_excel(writer, sheet_name = 'Players IDs', index = False)



# quit
writer.close()