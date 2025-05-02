import requests
from bs4 import BeautifulSoup


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0"
}


def getTabela():
    url = 'https://www.cnnbrasil.com.br/esportes/futebol/tabela-do-brasileirao/'

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    all_data = []
        
    divs = soup.find_all('div', class_='team__info')
    times = []
        
    for div in divs:
        span = div.find('span', class_='hide__s')
        if span:
                
            times.append(span.text.strip())

        pontos = []
        for ponto in soup.find_all('td', class_='teams__points table__body__cell--gray'):
            pontoss = ponto.text
            pontoss_a = int(pontoss)
            pontos.append(pontoss_a)
        for team, scores in zip (times, pontos):
            all_data.append((team, scores))
        
        return times, pontos
    return None