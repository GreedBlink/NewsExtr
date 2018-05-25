# -*- coding: utf-8 -*-
"""
Created on Fri May 18 11:41:21 2018

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

%run -i funcoes.py









url = 'https://extra.globo.com/noticias/plantao.html?page='   
page = 1
df_links = pd.DataFrame(columns = ["links_brutos"])
url_extract = url + str(page)
r = requests.get(url_extract)
while(r.status_code == 200):
    page = page + 1
    print("get page:" + str(page))
    url_extract = url + str(page)
    r = requests.get(url_extract)
    soup = BeautifulSoup(r.content, 'lxml')
    teste = soup.findAll('a')
    time.sleep(1)
    for i in range(len(teste)):
        if('https://extra.globo.com/noticias/'  in teste[i].attrs['href'] and 'html' in teste[i].attrs['href'] and '?page=' not in teste[i].attrs['href']):
            df_links =  df_links.append({'links_brutos':  teste[i].attrs['href']},ignore_index=True)


            
df_links = df_links.drop_duplicates()
df_links = df_links.reset_index(drop=True )        
columns = ['date','link', 'manchete','text','jornal']
df_noticias_extra = pd.DataFrame(columns = columns)

for i in range(len(df_links)):
        print("get news:" + str(i)+" of "+str(len(df_links)))
        link = df_links['links_brutos'][i]
        time.sleep(2.5)
        #k = requests.get(link)
        #if k.ok != True:
           # i = i+1
           # link = df_links_only['links_brutos'][i]
        k = requests.get(link)
        date = get_date(k,jornal = 'extra')
        manchete = get_manchete(k)
        jornal = 'extra' 
        noticia = boilerpipe_api_article_extract(link)
            
        df_noticias_extra =  df_noticias_extra.append({'date': date,
                                              'link': link,
                                              'manchete':manchete ,
                                              'text': noticia,
                                              'jornal': jornal
                                             },ignore_index = True)
