# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 16:02:43 2018

@author: jonatha.costa
"""
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from pymongo import MongoClient
import pandas as pd 
import numpy as np
import requests
import json
import time
import os
os.chdir('elasticsearch')
credenciais = pd.read_table('credencias.txt')
es = Elasticsearch(str(credenciais['x'][0]))

results = json.loads(r.text)

page = es.search(
  index = 'extra',
  doc_type = 'noticias',
  scroll = '2m',
  size = 10000,
  body = {
        'query': {
            'match_all' : {}
            }
    })
    
sid = page['_scroll_id']
scroll_size = page['hits']['total']
  
Frame = pd.DataFrame()
  # Start scrolling
while (scroll_size > 0):
   print("Scrolling...")
   page = es.scroll(scroll_id = sid, scroll = '2m')
   # Update the scroll ID
   sid = page['_scroll_id']
   # Get the number of results that we returned in the last scroll
   scroll_size = len(page['hits']['hits'])
   kaux = pd.DataFrame(page['hits']['hits'])
   Frame = Frame.append(pd.DataFrame(data = kaux), ignore_index=True)
   print("scroll size: " + str(scroll_size))
   # Do something with the obtained page