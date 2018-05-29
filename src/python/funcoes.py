# -*- coding: utf-8 -*-
"""
Created on Fri May 25 15:24:05 2018

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