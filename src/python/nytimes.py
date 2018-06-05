# -*- coding: utf-8 -*-
"""
Created on Mon Jun  4 15:23:53 2018

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


    
    
def get_date(k):
    soup = BeautifulSoup(k,'lxml')
    date = soup.find("time")
    date = date.attrs['datetime']
    
    try:
        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d')   
    except ValueError:
        date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").strftime('%Y-%m-%d')
    return(date)
    
    
    
    
def get_manchete(k):
    soup = BeautifulSoup(k, 'lxml')
    #manchete = soup.findAll('h1',{'class':'content-head__title'})
    manchete = soup.findAll('h1',{'property':'na:headline'})
    try:    
        manchete_ok = manchete[0].text
    except IndexError:   
        page_content = Document(k)
        manchete_ok = page_content.title()
    return(manchete_ok)
    



def boilerpipe_api_article_extract(k):
    soup = BeautifulSoup(k, 'lxml')
    text = soup.find_all('p')
    texto = ""
    for news in range(len(text)):
        #print('concatenate part '+ str(news) + ' of ' + str(len(text)))
        aux = text[news].text
        texto = texto +   aux
    return(texto)    


'https://www.nytimes.com/search?query=Date&sort=newest'


url = 'https://www.nytimes.com/search?query=Date&sort=newest'
page = 1
df_links = pd.DataFrame(columns = ["links_brutos"])
url_extract = url + str(page)
r = requests.get(url)
while(r.status_code == 200):
    page = page + 1
    print("get page:" + str(page))
    url_extract = url + str(page)
    r = requests.get(url_extract)
    soup = BeautifulSoup(r.content, 'lxml')
    teste = soup.findAll('a')
    teste2 = teste.find('a')
    time.sleep(1)
    for i in range(len(teste)):
        if('https://www.nytimes.com'  in teste[i].attrs['href']):
            print(i)
            df_links =  df_links.append({'links_brutos':  teste[i].attrs['href']},ignore_index=True)
            
df_links = df_links.drop_duplicates()
df_links = df_links.reset_index(drop=True )       

df_html = pd.DataFrame(columns = ["html"])

for i in range(len(df_links)):
    print("get html:" + str(i) + ' of ' + str(len(df_links)))
    r = requests.get(df_links['links_brutos'][i])
    time.sleep(2)
    df_html = df_html.append({'html': r.content},ignore_index=True)
            
df_links = pd.concat([df_links,df_html],axis = 1)   
  
columns = ['date','link','html','manchete','text','jornal']
df_noticias_extra = pd.DataFrame(columns = columns)