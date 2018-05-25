# -*- coding: utf-8 -*-
"""
Created on Fri May 25 15:24:05 2018

@author: jonatha.costa
"""

def get_date(k, jornal):
    soup = BeautifulSoup(k.content,'lxml')
    try:
        date = soup.find("time")
        date = date.attrs['datetime']
        date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime('%Y-%m-%d')
        return(date)
        
    except ValueError:
        date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").strftime('%Y-%m-%d')
        return(date)
        if('horas' in str(date) or 'hora' in str(date) or 'minutos' in str(date)):
            date = time.strftime("%Y-%m-%d")
            return(date)
        if(jornal == 'extra'):
            date = date.split(" ")[4]
        else:
            date = date.split(" ")[1]
    except AttributeError:
        date = soup.find("abbr").text
        date = date.split(" ")[3]
    try:    
        date = datetime.datetime.strptime(date, "%d/%m/%Y").strftime('%Y-%m-%d')
    except ValueError:   
        date = datetime.datetime.strptime(date, "%d/%m/%y").strftime('%Y-%m-%d')
    return(date)
    
    
    
    
def get_manchete(k):
    soup = BeautifulSoup(k.content, 'lxml')
    manchete = soup.findAll('h1',{'class':'content-head__title'})
    try:    
        manchete_ok = manchete[0].text
    except IndexError:   
        page_content = Document(k.content)
        manchete_ok = page_content.title()
    return(manchete_ok)
    



def boilerpipe_api_article_extract(url):
    
    url_extract =  url
    
    r = requests.get(url_extract)
    soup = BeautifulSoup(r.content, 'lxml')
    text = soup.find_all('p')
    texto = ""
    for news in range(len(text)):
        #print('concatenate part '+ str(news) + ' of ' + str(len(text)))
        aux = text[news].text
        texto = texto +   aux
    return(texto)    