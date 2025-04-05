import requests 
from bs4 import BeautifulSoup
import datetime

def horoscope_data(sign):
    signs = ['aries', 'touro', 'gemeos', 'cancer', 'leao', 'virgem', 'libra', 'escorpiao', 'sagitario', 'capricornio', 'aquario', 'peixes']
    
    
    if sign in signs:
        url = f'https://joaobidu.com.br/horoscopo-do-dia/horoscopo-do-dia-para-{sign}/'
        
        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }  
        
        response = requests.get(url, headers=headers)
        
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find('div', class_='zoxrel left')
        
        p = div.find('p')
        
        data_atual = datetime.datetime.now()

        data_formated = data_atual.strftime("%d/%m/%Y")

        return p.text, data_formated
    else:
        msg = 'Signo digitado incorretamente.'
        return msg
        

teste = horoscope_data('aquario')
    
    
