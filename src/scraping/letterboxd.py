import requests 
from bs4 import BeautifulSoup 
import random
import time
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0"
        }


def getWatchList(user):
    pool = list(range(1,20))
    while True:
        if not pool:
            print("sem watchlist")
            return
        
        page_number = random.choice(pool)
        url = f"https://letterboxd.com/{user}/watchlist/page/{page_number}/"
        response = requests.get(url, headers=headers)
        pool.remove(page_number)

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
    number = tag_p.find("a", attrs={'data-track-action': 'TMDB'}).get('href')[33:]

    return number.rsplit('/')[0]

def getProfile(user):
   
    url = f'https://letterboxd.com/{user}'
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return 

    soup = BeautifulSoup(response.text, 'html.parser')

    span = soup.find('span', class_="avatar -a110 -large")
    img = span.find('img').get('src')
    
    return img


