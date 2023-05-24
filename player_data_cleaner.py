# Importing libraries
import pandas as pd
import re

# Dropping unnecessary columns
df = pd.read_csv('nba_player_info.csv',index_col=False)
df = df.drop(columns=['Last Attended','Country','Weight'])

# Converting height to inches
r = re.compile(r'([5-7]+)-(\d{1,2})')
def convert_to_inches(row):
    m = r.match(row)
    m_num = int(m.group(1))*12+float(m.group(2))
    return int(m_num)
df['Height']=df['Height'].apply(convert_to_inches)

# Getting rid of players without data
df = df.dropna()

# Converting number column to int
df = df.astype({'Number':'int64'})

df.to_csv('nba_player_info_updated.csv',index=False)