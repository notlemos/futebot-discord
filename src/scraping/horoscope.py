import aiohttp
from bs4 import BeautifulSoup
import unicodedata
import asyncio
async def horoscope_data(sign):
    
    signo_formated = ''.join(
        c for c in unicodedata.normalize('NFD', sign.lower())
        if unicodedata.category(c) != 'Mn'
    )
    
    
    signs = ['aries', 'touro', 'gemeos', 'cancer', 'leao', 'virgem', 'libra', 'escorpiao', 'sagitario', 'capricornio', 'aquario', 'peixes']
    
    
    if signo_formated in signs:
        url = f'https://joaobidu.com.br/horoscopo-do-dia/horoscopo-do-dia-para-{signo_formated}/'
        
        headers = {
        "User-Agent": "Mozilla/5.0"
        }  
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                html = await response.text()
        
        
        soup = BeautifulSoup(html, 'html.parser')
        div = soup.find('div', class_='zoxrel left')
        
        p = div.find('p', class_='MsoNormal')
        

        return p.text
    else:
        return None

    
    
