import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.db import DBFute
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0"
}


def getTabela():
    url = 'https://www.terra.com.br/esportes/futebol/brasileiro-serie-a/tabela/'

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    names = soup.select('td.main.team-name')
    posicoes = soup.select('td.main.position')
    pontos = soup.select('t')

    times = []
    pontos = []

    for name in names:
        nome = name.select_one('a')['title']
        times.append(nome)
    for posicao in posicoes:
        a = posicao.text 
        
    for ponto in soup.select('td.points'):
        txt = ponto.text
        pontos.append(int(txt))
    
    return times, pontos

def getRodada():
    url = 'https://p1.trrsf.com/api/musa-soccer/ms-standings-games-light?idChampionship=1436&idPhase=&language=pt-BR&country=BR&nav=N&timezone=BR'  # coloca aqui a URL que você quer extrair

    response = requests.get(url)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')
    jogos = soup.select('li.match')
    rodada_num = 1
    id_jogo = 1
    matches = []
    
    for match in jogos:
        
        away_team = match.select_one('.shield.away')['title']
        home_team = match.select_one('.shield.home')['title']
        acronym_away = match.select_one('.shield.away').select_one('span.acronym').text
        acronym_home = match.select_one('.shield.home').select_one('span.acronym').text
        away_goals = match.select_one('strong.goals.away')
        home_goals = match.select_one('strong.goals.home')
            
        data = match.select_one('strong.time.sports-date-gmt.date-manager')

        home_goals_next = home_goals.text.strip() if home_goals else '-'
        away_goals_next = away_goals.text.strip() if away_goals else '-'
        data_next = data.text.strip() if data else '-'
        
        matches.append({
            'Rodada': rodada_num,
            'id_jogo': id_jogo,
            'Sigla Mandante': acronym_home,
            'Mandante': home_team,
            'Sigla Visitante': acronym_away,
            'Visitante': away_team,
            'Gols Mandante': home_goals_next,
            'Gols Visitante': away_goals_next,
            'Data': data_next
        })
        id_jogo += 1
        if id_jogo > 10:
            rodada_num += 1
            id_jogo = 1
    return matches
def getTabela_user():
    url = 'https://www.terra.com.br/esportes/futebol/brasileiro-serie-a/tabela/'

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None
    all_data = []
    soup = BeautifulSoup(response.text, 'html.parser')
    names = soup.select('td.main.team-name')
    posicoes = soup.select('td.main.position')
    pontos = soup.select('t')
    

    times = []
    pontos = []
    siglas = []
    for name in names:
        nome = name.select_one('a')['title']
        times.append(nome)
    for posicao in posicoes:
        a = posicao.text 
        
    for ponto in soup.select('td.points'):
        txt = ponto.text
        pontos.append(int(txt))
    
    
    
    for time in range(20):
        all_data.append({
            'Time': times[time],
            'Sigla': DBFute().getAcronym(times[time]),
            'Pontos': pontos[time],
            'Posicao': time
        })
    return all_data



