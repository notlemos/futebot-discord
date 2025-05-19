import requests 
import os
import time 
APITOKEN = os.getenv("TMBD_TOKEN")
def fetch_data(endpoint, filters={}):
    
    urll = f"https://api.themoviedb.org/3/movie/{endpoint}/images"
    headers = {
    "accept": "application/json",
    "Authorization": APITOKEN
    }

    response = requests.get(urll, headers=headers, params=filters)
    
    return response.json()['posters'][0]['file_path']



