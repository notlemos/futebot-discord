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
        
    times = []
    pontos = []     
    
    for nome in soup.find_all('span', class_='hide__s'):
        times.append(nome.get_text(strip=True))
        
    
    for ponto in soup.find_all('td', class_='teams__points table__body__cell--gray'):
        pontoss = ponto.text
        pontoss_a = int(pontoss)
        pontos.append(pontoss_a)
    
        
    return times, pontos