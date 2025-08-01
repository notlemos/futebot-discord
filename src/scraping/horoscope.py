import aiohttp
from bs4 import BeautifulSoup
import unicodedata
async def horoscope_data(sign):
    signo_formated = ''.join(
        c for c in unicodedata.normalize('NFD', sign.lower())
        if unicodedata.category(c) != 'Mn'
    )
    signs = ['aries', 'touro', 'gemeos', 'cancer', 'leao', 'virgem', 'libra', 'escorpiao', 'sagitario', 'capricornio', 'aquario', 'peixes']
    if signo_formated in signs:
        url = f'https://www.personare.com.br/horoscopo-do-dia/{signo_formated}'
        
        headers = {
        "User-Agent": "Mozilla/5.0"
        }  
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        h2 = soup.select_one('h2').get_text()
        divs = soup.select('p')
        imgs = soup.select('img')
        horoscopo = divs[3].get_text()
        imagem = imgs[13].get('src')
        footer = soup.select_one('h1').get_text()
        return h2, horoscopo, imagem, footer
    else:
        return None

    
    
