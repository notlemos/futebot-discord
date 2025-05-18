import requests 
import os
import time 
APITOKEN = os.getenv("TMBD_TOKEN")
def fetch_data(endpoint, filters={}):
    start = time.time()
    urll = f"https://api.themoviedb.org/3/movie/{endpoint}/images"
    headers = {
    "accept": "application/json",
    "Authorization": APITOKEN
    }

    response = requests.get(urll, headers=headers, params=filters)
    end = time.time()

    print(f"poster: {end - start:.2f} s")
    return response.json()['posters'][0]['file_path']



