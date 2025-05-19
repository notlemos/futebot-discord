import os
import requests


def baixar_woah():
    url = "https://whoa.onrender.com/whoas/random"

    response = requests.get(url=url)

    resposta = response.json()

    video = resposta[0]['video']['1080p']

    file = '/tmp/woah.mp4'

    with requests.get(video, stream=True) as r:
        r.raise_for_status()
        with open(file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=200):
                if chunk:
                    f.write(chunk)

    return file

