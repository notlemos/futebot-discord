import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.db import DBFute
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

        away_goals = match.select_one('strong.goals.away')
        home_goals = match.select_one('strong.goals.home')
            
        data = match.select_one('strong.time.sports-date-gmt.date-manager')

        home_goals_next = home_goals.text.strip() if home_goals else '-'
        away_goals_next = away_goals.text.strip() if away_goals else '-'
        data_next = data.text.strip() if data else '-'
        ano = datetime.now().year
        
        data_sem_dia = data_next[4:]  

        
        data_corrigida = data_sem_dia.replace("h", ":")  

        
        data_completa = f"{data_corrigida}/{ano}"  

        
        data_formatada = datetime.strptime(data_completa, "%d/%m %H:%M/%Y")
        matches.append({
            'Rodada': rodada_num,
            'id_jogo': id_jogo,
            'Mandante': home_team,
            'Visitante': away_team,
            'Gols Mandante': home_goals_next,
            'Gols Visitante': away_goals_next,
            'Data': data_formatada
        })
        id_jogo += 1
        if id_jogo > 10:
            rodada_num += 1
            id_jogo = 1
    return matches



