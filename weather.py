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


def weatherdata(city):
    
    all = date(city)
    flag = f'https://flagsapi.com/{all['sys']['country']}/flat/64.png' 
    temp = all['main']['temp']
    tempmin = all['main']['temp_min']
    tempmax = all['main']['temp_max']
    humidity = all['main']['humidity']
    name = all['name']
    cod = all['sys']['country'] 
    
    return flag, temp, tempmin, tempmax, humidity, name, cod


