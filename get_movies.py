import requests 

def fetch_data(endpoint, filters={}):
    def carregar_token():
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('TMBD_TOKEN'):
                    return line.strip().split('=')[1]  # Retorna o token sem espaços extras
    APITOKEN = carregar_token()
    url = f'https://api.themoviedb.org/3/search/movie?query={endpoint}&include_adult=false&language=en-US&page=1'
    headers = {
    "accept": "application/json",
    "Authorization": APITOKEN
    }

    response = requests.get(url, headers=headers, params=filters)
    
    return response.json()

filme = fetch_data("16 desejos")

movie_id = filme["results"][0]['id']

def get_items(name):
    filme = fetch_data(f"{name}")

    movie_id = filme["results"][0]['id']
    movie_poster = filme["results"][0]['poster_path']
    
    return movie_poster

print(get_items('16 desejos'))