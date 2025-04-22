import requests 
from bs4 import BeautifulSoup
import unicodedata

def horoscope_data(sign):
    
    signo_formated = ''.join(
        c for c in unicodedata.normalize('NFD', sign.lower())
        if unicodedata.category(c) != 'Mn'
    )
    
    signs = ['aries', 'touro', 'gemeos', 'cancer', 'leao', 'virgem', 'libra', 'escorpiao', 'sagitario', 'capricornio', 'aquario', 'peixes']
    
    
    if signo_formated in signs:
        url = f'https://joaobidu.com.br/horoscopo-do-dia/horoscopo-do-dia-para-{signo_formated}/'
        
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }  
        
        response = requests.get(url, headers=headers)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find('div', class_='zoxrel left')
        
        p = div.find('p')
        

        return p.text
    else:
        return None

    
    
