# -*- coding: utf-8 -*-
"""
Created on Tue May 29 15:33:14 2018

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
    date = soup.findAll("span",{'class':'date-display-single'})[0]
    date = date.text
    
    try:
        date = datetime.datetime.strptime(date, "%d/%m/%Y").strftime('%Y-%m-%d')   
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




url1_base = 'https://www.cartacapital.com.br/@@search?advanced_search=False&b_start:int='
url2_base = '&created.query:date:list:record=1970/01/02%2000%3A00%3A00%20GMT%2B0&created.range:record=min&portal_type:list=ExternalBlogEntry&portal_type:list=Person&portal_type:list=collective.nitf.content&sort_on=&pt_toggle=%23&SearchableText=a'

page = 0

df_links = pd.DataFrame(columns = ["links_brutos","html"])
url_extract = url1_base + str(page) + url2_base
r = requests.get(url_extract)

while(r.status_code == 200):
    print("get page:" + str(page))
    url_extract = url1_base + str(page) + url2_base
    r = requests.get(url_extract)
    soup = BeautifulSoup(r.content, 'lxml')
    html = soup
    teste = soup.findAll('a')
    time.sleep(1)
    for i in range(len(teste)-2):
        if('https://www.cartacapital.com.br'  in teste[i].attrs['href']  and '/@@search?' not in teste[i].attrs['href']):
            df_links =  df_links.append({'links_brutos':  teste[i].attrs['href'],
                                         'html': html
                                         },ignore_index=True)
    page = page + 1        
df_links = df_links.drop_duplicates()
df_links = df_links.reset_index(drop=True ) 

