import requests 
from bs4 import BeautifulSoup, SoupStrainer
import cloudscraper
import random
from curl_cffi.requests import AsyncSession
from curl_cffi import requests
from bs4 import BeautifulSoup
import time
import re
import cloudscraper
import asyncio
import aiohttp
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    }
HTML_HEADERS = {
    "User-Agent": "Mozilla/5.0"
}
async def getFilmsPages(user):
    
    async with AsyncSession(impersonate="chrome120") as session:
        url = f"https://letterboxd.com/{user}/films"
        headers = {"Referer": url}
        

        response = await session.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find('div', class_="pagination")
    
        a = div.find_all('a')
        
        return int(a[3].get_text())
def getpages(user):
    session = requests.Session(impersonate="chrome110")
    url = f"https://letterboxd.com/{user}/watchlist/"
    resp = session.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    div = soup.find_all('li', class_="paginate-page")
    return int(div[-1].get_text())
    

    
async def getFilmsList(user):
    pages = await getFilmsPages(user)
    page = random.randint(1, pages)
        
    async with AsyncSession(impersonate="chrome120") as session:
        
        url = f"https://letterboxd.com/{user}/films/page/{page}/"
        headers = {"Referer": url}

        response = await session.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        div = soup.find_all("li", class_="griditem")
        
            
        select = random.choice(div)
        
        movie = []
        
        nome = select.find("img", class_="image").get("alt")
        target = select.find('div', class_="react-component").get('data-target-link')
        rating = select.find("p", class_="poster-viewingdata").get_text()
        
        id, filter = await getIdMovie('https://letterboxd.com/' + target)
        
        movie.append({'name': nome, 'target': target, 'rating': rating, 'id': id, 'filter': filter})
        
        return movie
def getWatchList(user):
    scraper = cloudscraper.create_scraper()
    pages = getpages(user)
    page = random.randint(1, pages)
    
    url = f"https://letterboxd.com/{user}/watchlist/page/{page}"

    resp = scraper.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")

    items = soup.find_all("div", class_="react-component")

    if not items:
        print("Bloqueado ou sem dados")
        return None

    select = random.choice(items)

    name = select.get("data-item-name")
    link = select.get("data-target-link")

    return {
        "name": name,
        "link": f"https://letterboxd.com{link}"
    }


async def getIdMovie(url):
    async with AsyncSession(impersonate="chrome104") as s:
            resp = await s.get(url, timeout=15, headers=headers)
            
            if resp.status_code != 200:
                print(f"Erro HTTP: {resp.status_code}")
                return None, None

            html = resp.text

            soup = BeautifulSoup(html, "html.parser")

          
            a = soup.select_one("p.text-link.text-footer a[data-track-action='TMDB']")
            
            if not a:
                print("Link do TMDB não encontrado na página.")
                return None, None
            href = a["href"].strip("/")
            parts = href.split("/")
            return parts[-1], parts[-2]
async def getratings2(session, user):
    url = f"https://letterboxd.com/{user}/"
    async with session.get(url, headers=headers) as response:
        if response.status != 200:
            return None 
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        data = []
        divs = soup.find('div', class_="rating-histogram clear rating-histogram-exploded")
        li = divs.find_all('li', class_='rating-histogram-bar')
        for i in li:
            partes = i.text.strip().split(' ')
            data.append([partes[0], partes[-1]])
        return data

def getIdMovie2(url):
    scraper = cloudscraper.create_scraper()
    try:
        resp = scraper.get(url, timeout=10, headers=headers)
    except Exception as e:
        print(f'Error: {e}')
        return None, None
    soup = BeautifulSoup(resp.text, 'html.parser')
    tag_p = soup.find("p", class_="text-link text-footer")
    number = tag_p.find("a", attrs={'data-track-action': 'TMDB'}).get('href')
        
    id = number.strip('/').split('/')[-1]
    filter = number.strip('/').split('/')[-2]
   
    return id, filter


async def getProfile(session, user):
    url = f"https://letterboxd.com/{user}/"

    async with session.get(url, headers=headers) as response:
        print("STATUS:", response.status)

        if response.status != 200:
            return None

        html = await response.text()

     

        soup = BeautifulSoup(html, "html.parser")

        img_tag = soup.find("meta", property="og:image")
        img = img_tag["content"] if img_tag else None

        name_tag = soup.find("span", class_="displayname tooltip")
        name = name_tag.get_text(strip=True) if name_tag else "Desconhecido"

        patron_tag = soup.find("span", class_="badge -patron")
        patron = patron_tag.get_text(strip=True) if patron_tag else None

        return img, name, patron
async def getPfp(session, user):
   
    url = f'https://letterboxd.com/{user}/'
    async with session.get(url, headers=headers) as response:

        if response.status != 200:
            return None, "Desconhecido"

        html = await response.text()
        

        soup = BeautifulSoup(html, 'html.parser')

        img = soup.find('meta', property="og:image").get('content')
        
        
        return img
def getpic(user):
    scraper = cloudscraper.create_scraper()
    url = f"https://letterboxd.com/{user}/"
    try:
        resp = scraper.get(url, timeout=10)
    except Exception as e:
        print(f"Error; {e}")
        return None, None

    
   
        

    soup = BeautifulSoup(resp.text, 'html.parser')

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
    url = f"https://letterboxd.com/{user}/"
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)

    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    
    movies = soup.select("li.griditem .favourite-production-poster-container")
    all_data = []

    for movie in movies:
        react = movie.select_one("div.react-component")

        img = movie.select_one("img")

        if not react or not img:
            continue

        target = react.get("data-item-link")
        fav = img.get("alt")

        if not target or not fav:
            continue

        all_data.append({
            "filme": fav,
            "target": "https://letterboxd.com" + target
        })
    return all_data
    
def getLastFourWatched(user):
    url = f'https://letterboxd.com/{user}/' 
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    
    if response.status_code != 200:
        return 
    soup = BeautifulSoup(response.text, 'html.parser')

    movies = soup.select('li.griditem .viewing-poster-container')
    
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

def getpagesreviews(user):
    session = requests.Session(impersonate="chrome120")
    url = f'https://letterboxd.com/{user}/films/reviews/'
    
    try:
        response = session.get(url, timeout=10, headers=headers)
        if response.status_code != 200:
            return 1
        
        soup = BeautifulSoup(response.text, 'html.parser') 
        pages = soup.find_all('li', class_="paginate-page")
        if not pages:
            return 1
        return int(pages[-1].get_text(strip=True))
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


def randomreview(user):
    number = getpagesreviews(user)
    if not number:
        number = 1
    
    page = random.randint(1, number)
    scraper = cloudscraper.create_scraper()
    
    print(f"Total de páginas: {number}, sorteada: {page}")
    
    url = f"https://letterboxd.com/{user}/films/reviews/page/{page}/"
    
   
    response = scraper.get(url)
    if response.status_code != 200:
        return 
        
    soup = BeautifulSoup(response.text, 'html.parser') 
        
    
    reviews = soup.select("article.production-viewing")
    if not reviews:
        print("Nenhuma review encontrada (provável Cloudflare)")
        return
        
    chosen = random.choice(reviews)
    movie_name = chosen.select_one('h2.primaryname.prettify').get_text()
    release_date = chosen.select_one('span.releasedate').get_text()
    link = chosen.select_one('h2.primaryname.prettify').get('href')
    review = chosen.select_one('div.body-text.-prose.-reset.js-review-body.js-collapsible-text').get_text().strip()
    target = "https://letterboxd.com" + chosen.select_one('div.react-component.figure').get('data-target-link')
    logDate = chosen.select_one('time.timestamp').get_text()
    rating = chosen.select_one('svg').get('aria-label')
    return review, link, movie_name, release_date, rating, logDate, target
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