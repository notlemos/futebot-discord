import requests 
import os


APITOKEN = os.getenv("TMBD_TOKEN")
def fetch_data(endpoint, filters={}):
    
    url = f'https://api.themoviedb.org/3/search/movie?query={endpoint}&include_adult=false&language=en-US&page=1'
    headers = {
    "accept": "application/json",
    "Authorization": APITOKEN
    }

    response = requests.get(url, headers=headers, params=filters)
    
    return response.json()


def get_items(name):
    filme = fetch_data(f"{name}")

    #movie_id = filme["results"][0]['id']
    movie_poster = filme["results"][0]['poster_path']
   # print(filme['results'][0])
    return movie_poster


