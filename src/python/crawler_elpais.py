# -*- coding: utf-8 -*-
"""
Created on Mon May 28 11:08:00 2018

@author: jonatha.costa
"""


import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import re
import numpy  as np
from readability import Document
import requests
from readability.readability import Document
import time



url = 'https://brasil.elpais.com/seccion/politica'   
page = 0
df_links = pd.DataFrame(columns = ["links_brutos"])
url_extract = url + '/' + str(page)
r = requests.get(url_extract)
while(r.status_code == 200):
    page = page + 1
    print("get page:" + str(page))
    url_extract = url + '/' + str(page)
    r = requests.get(url_extract)
    soup = BeautifulSoup(r.content, 'lxml')
    teste = soup.findAll('a')
    time.sleep(1)
    for i in range(len(teste)):
        if('//brasil.elpais.com/brasil'  in teste[i].attrs['href'] and 'html' in teste[i].attrs['href'] and '?page=' not in teste[i].attrs['href']):
            df_links =  df_links.append({'links_brutos': 'https:'+ teste[i].attrs['href']},ignore_index=True)
            
                        
df_links = df_links.drop_duplicates()
df_links = df_links.reset_index(drop=True)       



df_html = pd.DataFrame(columns = ["html"])

for i in range(len(df_links)):
    print("get html:" + str(i) + ' of ' + str(len(df_links)))
    r = requests.get(df_links['links_brutos'][i])
    time.sleep(2)
    df_html = df_html.append({'html': r.content},ignore_index=True)
            
df_links = pd.concat([df_links,df_html],axis = 1)   
  
columns = ['date','link','html','manchete','text','jornal']
df_noticias_extra = pd.DataFrame(columns = columns)





