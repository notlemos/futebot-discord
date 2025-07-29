import requests 
from bs4 import BeautifulSoup 
import random
import time
import re
import asyncio
import aiohttp
headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0"
        }
HTML_HEADERS = {
    "User-Agent": "Mozilla/5.0"
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


async def getIdMovie(session, url):
    async with session.get(url, headers=HTML_HEADERS) as response:
    
    

        if response.status != 200:
            return None, None 
        
        html = await response.text()
        
        soup = BeautifulSoup(html, 'html.parser')


        tag_p = soup.find("p", class_="text-link text-footer")
        number = tag_p.find("a", attrs={'data-track-action': 'TMDB'}).get('href')
        
        id = number.strip('/').split('/')[-1]
        filter = number.strip('/').split('/')[-2]
        
        return id, filter
    

def getIdMovie2(url):
    response = requests.get(url, headers=headers)
    response = response.text
    soup = BeautifulSoup(response, 'html.parser')
    tag_p = soup.find("p", class_="text-link text-footer")
    number = tag_p.find("a", attrs={'data-track-action': 'TMDB'}).get('href')
        
    id = number.strip('/').split('/')[-1]
    filter = number.strip('/').split('/')[-2]
        
    return id


async def getProfile(session, user):
   
    url = f'https://letterboxd.com/{user}'
    async with session.get(url, headers=HTML_HEADERS) as response:

        if response.status != 200:
            return None, "Desconhecido"

        html = await response.text()
        

        soup = BeautifulSoup(html, 'html.parser')

        span = soup.find('span', class_="avatar -a110 -large")
        img = span.find('img').get('src')
        nameSpan = soup.find('span', class_="displayname tooltip").get_text()
        try:
            patron = soup.find('span', class_="badge -patron").get_text()
        except:
            patron = None
        return img, nameSpan, patron
async def getPfp(session, user):
   
    url = f'https://letterboxd.com/{user}'
    async with session.get(url, headers=HTML_HEADERS) as response:

        if response.status != 200:
            return None, "Desconhecido"

        html = await response.text()
        

        soup = BeautifulSoup(html, 'html.parser')

        span = soup.find('span', class_="avatar -a110 -large")
        img = span.find('img').get('src')
        
        
        return img
def getpic(user):
    url = f"https://letterboxd.com/{user}"
    response = requests.get(url, headers=headers)

    html = response.text 
   
        

    soup = BeautifulSoup(html, 'html.parser')

    span = soup.find('span', class_="avatar -a110 -large")
    img = span.find('img').get('src')
    nameSpan = soup.find('span', class_="displayname tooltip").get_text()
        
    return img, nameSpan
    

def get():
    all_data = []
    for j in range(1,4):
        url = f"https://letterboxd.com/dave/list/official-top-250-narrative-feature-films/page/{j}/"
        respose = requests.get(url=url, headers=headers)
        
        if respose.status_code != 200:
            return 'error'
        
        soup = BeautifulSoup(respose.text, 'html.parser')
        li = soup.find_all("li", class_="poster-container numbered-list-item")

        for i in li:
            div = i.find('div', class_="really-lazy-load poster film-poster linked-film-poster")
            if not div:
                continue
            target = div.get("data-target-link") 
            name = div.find("img").get('alt')

            link = "https://letterboxd.com" + target


            #d = getIdMovie(link)    
            

            all_data.append({
                'position': len(all_data)+1,
                'name': name,
                'link': link,
                #'id': id,
            })
            if len(all_data) >= 250:
                return all_data
    return all_data
        


def getRandomList(link):
    while True:
        all_data = []
        page = random.randint(1,8)
        url = f"{link}/page/{page}/"
        respose = requests.get(url=url, headers=headers)
        if respose.status_code != 200:
            continue
            
        soup = BeautifulSoup(respose.text, 'html.parser')
            
        li = soup.find_all("li", class_="poster-container")
        if not li:
            continue
        nameList = soup.find("h1", class_="title-1 prettify has-notes")
        if nameList:
            nameList = nameList.text 
        else:
            nameList = soup.find("h1", class_="title-1 prettify").text
        
        for i in li:
            div = i.find('div', class_="really-lazy-load poster film-poster linked-film-poster")
            if not div:
                continue
            target = div.get("data-target-link") 
            
            name = div.find("img").get('alt')
            link = "https://letterboxd.com" + target
        
            
            all_data.append({
                'namelist': nameList,
                'name': name,
                'link': link,
                
            })
        return random.choice(all_data)
def getFavs(user):
   
    url = f'https://letterboxd.com/{user}'
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return 
    
    soup = BeautifulSoup(response.text, 'html.parser')
    movies = soup.select('li.poster-container.favourite-film-poster-container')
    favs = []
    targets = []
    all_data = []
    for movie in movies:
        target = movie.select_one('div.really-lazy-load.poster.film-poster.linked-film-poster').get('data-details-endpoint')
        fav = movie.select_one('img').get('alt')
        favs.append(fav)
        targets.append("https://letterboxd.com" + target[:-5])
    for targett, filme in zip(targets, favs):
        all_data.append({
            'filme': filme,
            'target': targett
        })   
    return all_data
def getLastFourWatched(user):
    url = f'https://letterboxd.com/{user}' 
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return 
    soup = BeautifulSoup(response.text, 'html.parser')

    movies = soup.select('li.poster-container.viewing-poster-container')
    
    lastFourWatched = []
    targets = []
    all_data = []

    for movie in movies:
        target = movie.select_one('div.really-lazy-load.poster.film-poster.linked-film-poster').get('data-details-endpoint')
        last = movie.select_one('img').get('alt')
        lastFourWatched.append(last)
        
        targets.append("https://letterboxd.com" + target[:-5])
    for targett, filme in zip(targets, lastFourWatched):
        all_data.append({
            'filme': filme, 
            'target': targett
        })
    return all_data

async def getpagesreviews(user, session):
    url = f'https://letterboxd.com/{user}/films/reviews/'
    async with session.get(url, headers=headers) as response:

        if response.status != 200:
            return 1
        
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser') 

        pages = soup.find_all('li', class_="paginate-page")
        if not pages:
            return 1
        try:
            return int(pages[-1].get_text())
        except:
            return 1 
        
async def getDirector(url, session):
    url = url
    async with session.get(url, headers=headers) as response:
        if response.status != 200:
            return 1 
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')

        director = soup.find('p', class_="credits").find('span', class_="prettify").get_text().strip()
        return director




async def randomreview(user, session):
    number = await getpagesreviews(user, session)
    page = random.randint(1, number)
    url = f"https://letterboxd.com/{user}/films/reviews/page/{page}/"
    async with session.get(url, headers=headers) as response:
        
        

        if response.status!= 200:
            return 
        
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser') 
        reviews = soup.find_all('div', class_="listitem js-listitem")
        if not reviews:
            return 
        chosen = random.choice(reviews)
        review = chosen.find('div', class_='body-text -prose -reset js-review-body js-collapsible-text').get_text()        
        movie_link = "https://letterboxd.com" + chosen.find('h2', class_="name -primary prettify").find('a').get('href')
        movie_name = chosen.find('h2', class_="name -primary prettify").find('a').get_text()
        date = chosen.find('span', class_='releasedate').find('a').get_text()
        rating = chosen.find('span', class_='content-reactions-strip -viewing').find('span').get_text()
        dateLog = chosen.find('span', class_='date').find('time').get_text()
        target = chosen.find('div', class_="really-lazy-load poster film-poster linked-film-poster").get('data-target-link')
        
        return review[1:], movie_link, movie_name, date, rating, dateLog, target

        