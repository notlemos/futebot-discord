import requests 
import os
from itertools import islice, chain
APITOKEN = os.getenv("TMBD_TOKEN")


async def fetch_data(session, endpoint, media_type):
    headers = {
        "Authorization": f"{APITOKEN}",
        "Accept": "application/json"
    }
    url = f"https://api.themoviedb.org/3/{media_type}/{endpoint}/images"
    async with session.get(url, headers=headers) as response:
        if response.status != 200:
            
            return None, None  
        
        data = await response.json()

        posters = data.get('posters', [])
        backdrops = data.get('backdrops', [])

        backdrop = next(islice((b for b in backdrops if b.get('iso_639_1') is None),0 , None), None)
        poster = next(
            chain(
                (p for p in posters if p.get('iso_639_1') == 'en'),
                (p for p in posters if p.get('iso_639_1') is None),
                
                ),
                None
        )

        poster_path = poster['file_path'] if poster else None
        backdrop_path = backdrop['file_path'] if backdrop else None
        
        return poster_path, backdrop_path

        
def fetchdata(endpoint, media_type):
    headers = {
    "accept": "application/json",
    "Authorization": APITOKEN
    }
    
    urll = f"https://api.themoviedb.org/3/{media_type}/{endpoint}/images"
    response = requests.get(urll, headers=headers)
    
    if response.status_code != 200:
        return 'erro'
    data = response.json()
    posters = data.get('posters', [])
    
    poster = next(
        (p for p in posters if p.get('iso_639_1') == 'en'),
            next(
                (p for p in posters if p.get('iso_639_1') is None),
                posters[0] if posters else None
            )
    )
    return poster['file_path']


