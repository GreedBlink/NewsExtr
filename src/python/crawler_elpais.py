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


def get_date(k):
    soup = k
    #soup = BeautifulSoup(k,'lxml')
    date = soup.findAll("meta",{'itemprop':'datePublished'})[1]
    date = date.attrs['content']
    
    try:
        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d')   
    except ValueError:
        date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").strftime('%Y-%m-%d')
    return(date)
    
    
    
    
def get_manchete(k):
    #soup = BeautifulSoup(k, 'lxml')
    soup = k
    #manchete = soup.findAll('h1',{'class':'content-head__title'})
    manchete = soup.findAll('h1',{'class':'articulo-titulo'})
    try:      
        manchete_ok = manchete[0].text
    except IndexError:   
        page_content = Document(k)
        manchete_ok = page_content.title()
    return(manchete_ok)
    



def boilerpipe_api_article_extract(k):
    soup = k
    #soup = BeautifulSoup(k, 'lxml')
    text = soup.find_all('p')
    texto = ""
    for news in range(len(text)):
        #print('concatenate part '+ str(news) + ' of ' + str(len(text)))
        aux = text[news].text
        texto = texto +   aux
    return(texto)    



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
    #html = soup
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
df_noticias_elpais = pd.DataFrame(columns = columns)

for i in range(len(df_links)):
        print("get news:" + str(i)+" of "+str(len(df_links)))
        k = df_links['html'][i]
        link = df_links['links_brutos'][i]
        date = get_date(k)
        manchete = get_manchete(k)
        jornal = 'extra' 
        noticia = boilerpipe_api_article_extract(k)
            
        df_noticias_elpais =  df_noticias_elpais.append({'date': date,
                                              'link': link,
                                              'html': df_links['html'][i],
                                              'manchete':manchete ,
                                              'text': noticia,
                                              'jornal': jornal
                                             },ignore_index = True)



