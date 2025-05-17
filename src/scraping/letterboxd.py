import requests 
from bs4 import BeautifulSoup 
import os 
import random
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0"
        }


def getWatchList(user):
    while True:
        page_number = random.randint(1,20)
        url = f"https://letterboxd.com/{user}/watchlist/page/{page_number}/"
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            continue


        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find_all("div", class_="really-lazy-load poster film-poster linked-film-poster")
        images = soup.find_all("img", class_="image")
        

        if not div or not images:
            continue

        names = []

        for trgt in div:
            nome = trgt.find("img", class_="image").get("alt")
            target = trgt.get("data-target-link")
            if nome and target:
                names.append({'name': nome, 'target': target})

        return random.choice(names)


def getIdMovie(link):
    url = link
    respose = requests.get(url=url, headers=headers)

    if respose.status_code != 200:
        return 'error'
    
    soup = BeautifulSoup(respose.text, 'html.parser')
    tag_p = soup.find("p", class_="text-link text-footer")
    tag_a = tag_p.find("a", attrs={'data-track-action': 'TMDB'})
    number = tag_a.get('href')[33:]
    return number.rsplit('/')[0]
        

print(getIdMovie("https://letterboxd.com/film/house-of-hummingbird/"))

