import requests
import os
from dotenv import load_dotenv
load_dotenv()


apiWeatherKey= os.getenv("apiWeatherKey")


def date(endpoint):

    url = f'https://api.openweathermap.org/data/2.5/weather?q={endpoint}&units=metric&APPID={apiWeatherKey}' 
    headers = {
        "accept": "application/json",
        }

    response = requests.get(url, headers=headers)
        
    resposta = response.json()
    
    return resposta

def weatherdata(cidade):
    
    all = date(cidade)
    flag = f'https://flagsapi.com/{all['sys']['country']}/flat/64.png' 
    temp = all['main']['temp']
    sens = all['main']['feels_like']
    humidity = all['main']['humidity']
    name = all['name']
    cod = all['sys']['country'] 
    
    return flag, temp, sens, humidity, name, cod


