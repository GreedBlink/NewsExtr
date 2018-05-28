# -*- coding: utf-8 -*-
"""
Created on Fri May 18 11:41:21 2018

@author: jonatha.costa
"""

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

df_html = pd.DataFrame(columns = ["html"])

for i in range(len(df_links)):
    print("get html:" + str(i) + ' of ' + str(len(df_link)))
    r = requests.get(df_links['links_brutos'][i])
    time.sleep(2)
    df_html = df_html.append({'html': r.content},ignore_index=True)
            
df_links = pd.concat([df_links,df_html],axis = 1)   
  
columns = ['date','link','html','manchete','text','jornal']
df_noticias_extra = pd.DataFrame(columns = columns)

for i in range(len(df_links)):
        print("get news:" + str(i)+" of "+str(len(df_links)))
        #link = df_links['links_brutos'][i]
        #time.sleep(2)
        k = df_links['html'][i]
        date = get_date(k,jornal = 'extra')
        manchete = get_manchete(k)
        jornal = 'extra' 
        noticia = boilerpipe_api_article_extract(k)
            
        df_noticias_extra =  df_noticias_extra.append({'date': date,
                                              'link': link,
                                              'html': df_links['html'][i],
                                              'manchete':manchete ,
                                              'text': noticia,
                                              'jornal': jornal
                                             },ignore_index = True)
