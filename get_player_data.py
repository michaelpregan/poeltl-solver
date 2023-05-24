#Import Libraries
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import requests

# Get NBA Players Table
driver = webdriver.Firefox()
url = 'https://www.nba.com/players'
driver.get(url)
select = Select(driver.find_element('xpath','//*[@id="__next"]/div[2]/div[2]/main/div[2]/section/div/div[2]/div[1]/div[7]/div/div[3]/div/label/div/select'))
select.select_by_index(0)
src = driver.page_source
parser = BeautifulSoup(src,'lxml')
table = parser.find('div',attrs={'class':'MockStatsTable_statsTable__V_Skx'})

# Getting Headers
headers = table.findAll('th')
headerlist = [h.text for h in headers]

# Getting Body
rows = table.findAll('tr')[1:]
all_player_info = []
for row in rows:
    player_info = [val.getText() for val in row.findAll('td')]
    all_player_info.append(player_info)

# Making df
df = pd.DataFrame(all_player_info,columns=headerlist)
df.to_csv('nba_player_info.csv')