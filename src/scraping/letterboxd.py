import requests 
from bs4 import BeautifulSoup, SoupStrainer
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
def getpages(user):
    url = f"https://letterboxd.com/{user}/watchlist"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return


    soup = BeautifulSoup(response.text, 'html.parser')
    div = soup.find('div', class_="pagination")
    a = div.find_all('a')
    
    return int(a[3].get_text())
    
def getWatchList(user):
    pages = getpages(user)
    page = random.randint(1, pages)
        
    
    url = f"https://letterboxd.com/{user}/watchlist/page/{page}/"
    response = requests.get(url, headers=headers)
    

    if response.status_code != 200:
        return


    soup = BeautifulSoup(response.text, 'html.parser')
    div = soup.find_all("div", class_="react-component")
    
        
    select = random.choice(div)
    
    movie = []
    
    nome = select.find("img", class_="image").get("alt")
    
    target = select.get("data-target-link")
    
    
    movie.append({'name': nome, 'target': target})
    
    return movie


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

        
        img = soup.find('meta', property="og:image").get('content')
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

        img = soup.find('meta', property="og:image").get('content')
        
        
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
        

def getListPages(link):
    url = link
    response = requests.get(url=url, headers=headers)
    
    
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        div = soup.select('li.paginate-page')
        numberOfPages = div[-1].get_text()
    except:
        numberOfPages = 1

    return numberOfPages
        



def getRandomList(link):
    
    all_data = []
    page = getListPages(link)
    url = f"{link}/page/{page}/"
    respose = requests.get(url=url, headers=headers)
   
    soup = BeautifulSoup(respose.text, 'html.parser')
    movies = soup.select('div.react-component')
    name_list = soup.select_one('h1.title-1.prettify').get_text()
    movie = random.choice(movies)
    target = movie.get('data-item-link')
    name = movie.get('data-item-name')
    linkFull = "https://letterboxd.com" + target
    all_data.append({
        'namelist': name_list,
        'name': name,
        'link': linkFull
    })
    return all_data
def getFavs(user):
   
    url = f'https://letterboxd.com/{user}'
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return 
    
    soup = BeautifulSoup(response.text, 'html.parser')
   
    movies = soup.select('li.posteritem.favourite-production-poster-container')
    
    favs = []
    targets = []
    all_data = []
    
    for movie in movies:
        target = movie.select_one('div.react-component').get('data-item-link')
        fav = movie.select_one('img').get('alt')
        favs.append(fav)
        targets.append("https://letterboxd.com" + target)
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

    movies = soup.select('li.posteritem.viewing-poster-container')
    
    lastFourWatched = []
    targets = []
    all_data = []

    for movie in movies:
        target = movie.select_one('div.react-component').get('data-item-link')
        last = movie.select_one('img').get('alt')
        lastFourWatched.append(last)
        
        targets.append("https://letterboxd.com" + target)
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

        director = soup.find('a', class_="contributor").find('span').get_text()
        
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
        target = chosen.find('div', class_="react-component figure").get('data-target-link')
        
        return review[1:], movie_link, movie_name, date, rating, dateLog, target
async def getRatings(session, nick):
    url = f"https://letterboxd.com/{nick}/"
    async with session.get(url, headers=headers) as response:

        if response.status!= 200:
            return 
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser') 
        section = soup.select_one('section.section.ratings-histogram-chart')
        ratings = section.select_one('div.rating-histogram.clear.rating-histogram-exploded')
        
        texto = ratings.get_text(separator=" ", strip=True).split(" ")[1:-1]
        texto = [r.replace('\xa0', ' ') for r in texto if '\xa0' in r or r.startswith('(')]
        numberss = []
        percentss = []
        for i in range(0, len(texto), 2):
            temp_list = texto[i].split(" ")
            if len(temp_list) < 2:
                continue
            numbers = temp_list[0]
        
            percent = texto[i + 1] if i + 1 < len(texto) else "0%"  
            numberss.append(numbers)
            percentss.append(percent)
        return numberss, percentss
async def getDiary(session, user, year, month):
    url = f"https://letterboxd.com/{user}/films/diary/for/{year}/{month}/"
    async with session.get(url, headers=headers) as response:

        if response.status!= 200:
            return 
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser') 
        diary = soup.select('tr.diary-entry-row.viewing-poster-container')
        

        names = []
    
        days =[]
        
        stars = []
        
        for i in diary:
            days.append(i.select_one('a.daydate').get_text().strip())
            names.append(i.select_one('h2.name.-primary.prettify').get_text())
            stars.append(i.select_one('div.hide-for-owner').get_text().strip())
        return names, days, stars
async def getYears(session, user):
    url = f"https://letterboxd.com/{user}/films/diary/"
    async with session.get(url, headers=headers) as response:
        if response.status != 200:
            return
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser') 
        sections = soup.select('section.smenu-wrapper')[5].find_all('li')
        years = []
        for x in sections[1:]:
            years.append(int(x.get_text()))
        
        return years
async def fetch_quantity(session, user, year):
    url = f"https://letterboxd.com/{user}/films/diary/for/{year}/"
    async with session.get(url, headers=headers) as response:
        if response.status != 200:
            return 0
        html = await response.text()
        only_sections = SoupStrainer("p", class_="ui-block-heading")
        soup = BeautifulSoup(html, 'html.parser', parse_only=only_sections)
        text = soup.select_one('p')
        if not text:
            return 0
        raw = text.get_text().strip()
        match = re.search(r"\d+", raw)
        return int(match.group()) if match else 0
async def getHowMuchMovies(session, user):
    years = await getYears(session, user)
    tasks = [fetch_quantity(session, user, year) for year in years]
    quantities = await asyncio.gather(*tasks)
    return quantities 