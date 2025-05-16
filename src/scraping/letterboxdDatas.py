import requests 
from bs4 import BeautifulSoup 
import os 
import random




def getWatchList(user):
    names = []
    for i in range(1, 15):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0"
        }

        url = f"https://letterboxd.com/{user}/watchlist/page/{i}/"


        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')



        div = soup.find_all("div", class_="really-lazy-load poster film-poster linked-film-poster")
        

        images = soup.find_all("img", class_="image")
        if not div or not images:
            break
        
        for img, trgt in zip(images, div):
            nome = img.get("alt")
            target = trgt.get("data-target-link")
            nomereplace = nome.replace(" ", "-").lower()
            names.append({
                'name': nome,
                'target': target
            })
    return random.choice(names)


