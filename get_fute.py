import requests
from bs4 import BeautifulSoup
import re


# Url a ser usada
url = 'https://www.sofascore.com/api/v1/tournament/57411/season/69522/standings/total'

# Headers para simular um navegador
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0"
}


# Funçao onde pego os dados atráves de uma raspagem de dados com request.

def get_standings(grupo_nome):
    response = requests.get(url, headers=headers)
    grupo = ''
    
    # Verificar se a resposta foi bem-sucedida
    
    if response.status_code == 200:
        data = response.json()
        if grupo_nome == 'A':
            grupo = "Group A"
        elif grupo_nome == 'B':
            grupo = "Group B"
        elif grupo_nome == "C":
            grupo = "Group C"
        elif grupo_nome == "D":
            grupo = "Group D"
        
        
        all_data = []
            
        for group_stat in data['standings']:
            group_name = group_stat['name']
                
            if group_stat['name'] == f'{grupo}':
                
                for team_info in group_stat['rows']:
                    team_name = team_info['team']['name']
                    team_points = team_info['points']
                        
                    all_data.append({
                        'Grupo': group_name, 
                        'Time': team_name,
                        'Pontos': team_points
                    })
                return all_data
    
        else:
            return []
        


def get_players(time): 
    url = f'https://www.ogol.com.br/equipe/{time}'
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0"
    }  # Adicione um User-Agent para evitar bloqueios
    response = requests.get(url, headers=headers)
    # Verificar se a resposta foi bem-sucedida
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        div2 = soup.find('div', class_='logo')
        
        jogadores = []
        
        img = div2.find('img')
        if img:
            escudo = img.get('src')
        else:
            escudo = None
        
        
        
        for box in soup.find_all('div', class_='innerbox'):
            # Verificação do título
            title_div = box.find('div', class_='title')
            
            if not title_div:
                continue

            posicao = title_div.get_text(strip=True)

            staff_list = box.find_all('div', class_='staff')

            for idx, staff in enumerate(staff_list):
                nome_div = staff.find('div', class_='name')

                if nome_div:
                    nome_text_div = nome_div.find('div', class_='text')

                    if nome_text_div:
                        nome = nome_text_div.get_text(strip=True)

                        idade_span = nome_div.find('span')
                        num = staff.find('div', class_='number')
                        
                        if num:
                            numero = num.text.strip()
                        else:
                            numero = None
                        
                        idade = idade_span.get_text(strip=True) if idade_span else None
                        jogadores.append({
                            'Nome': nome,
                            'Posicao': posicao,
                            'Idade': idade,
                            'Número': numero,
                            'Escudo': escudo
                            
                        })
        return jogadores



def get_artilheiros():
    url = 'https://www.espn.com.br/futebol/time/estatisticas/_/id/2674/liga/BRA.CAMP.PAULISTA/vista/gols'
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0"
    }  # Adicione um User-Agent para evitar bloqueios
    response = requests.get(url, headers=headers)
    # Verificar se a resposta foi bem-sucedida
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        artilheiros = []
        all_data = []
        gols = []
        cont = 0
        div = soup.find('tbody', class_='Table__TBODY')
        if div:
            for s in div.find_all('a', class_='AnchorLink'):
                names = s.text
                artilheiros.append(names)
            td = div.find_all('td', class_='tar Table__TD')
            if td:
                for x in div.find_all('span', class_='tar'):
                    gols.append(x.text)
            
            for i in range(0, 10, 2):
               
                all_data.append({
                        'Nome': artilheiros[i//2],
                        'Jogos': gols[i],
                        'Gols': gols[i+1] if i+1 < len(gols) else 0 
                })
            return all_data

def get_jogos(time):
    url = f"https://www.ogol.com.br/equipe/{time}"
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0"
    }  # Adicione um User-Agent para evitar bloqueios
    response = requests.get(url, headers=headers)
    # Verificar se a resposta foi bem-sucedida
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        home_team = []
        away_team = []
        data_jogo = []
        status_jogo = []
        all_data = []
        div = soup.find('div', id='team_games')
        if div:
            for s in div.find_all('td',class_='date'):
                dates = s.text
                data_jogo.append(dates)
            for x in div.find_all('td', class_='text home'):
                teamsHome = x.text 
                home_team.append(teamsHome )
            for y in div.find_all('td', class_='text away'):
                teamsAway = y.text 
                away_team.append(teamsAway)
            for h in div.find_all('td', class_='vs'):
                statsJogo = h.text 
                status_jogo.append(statsJogo)
            for k in div.find_all('td', class_='result'):
                statsJogo = k.text 
                status_jogo.append(statsJogo)
            for data, tc, sts, tf in zip(data_jogo, home_team, status_jogo, away_team):
                all_data.append({
                    'Data': data,
                    'TeamHome': tc,
                    'Result': sts,
                    'AwayTeam': tf
                })
        return all_data
    else:
        return None

   
def get_transfers(time):

    links = {
        'flamengo': 'https://onefootball.com/pt-br/time/flamengo-1802/transferencias',
        'corinthians': 'https://onefootball.com/pt-br/time/corinthians-1649/transferencias',
        'santos': 'https://onefootball.com/pt-br/time/santos-1798/transferencias',
        'atletico-mg': 'https://onefootball.com/pt-br/time/atletico-mg-1683/transferencias',
        'bahia': 'https://onefootball.com/pt-br/time/bahia-1795/transferencias',
        'botafogo': 'https://onefootball.com/pt-br/time/botafogo-1792/transferencias',
        'ceara': 'https://onefootball.com/pt-br/time/ceara-4833/transferencias',
        'fortaleza': 'https://onefootball.com/pt-br/time/fortaleza-4831/transferencias',
        'gremio': 'https://onefootball.com/pt-br/time/gremio-1670/transferencias',
        'internacional': 'https://onefootball.com/pt-br/time/internacional-1799/transferencias',
        'juventude': 'https://onefootball.com/pt-br/time/juventude-4779/transferencias',
        'mirassol': 'https://onefootball.com/pt-br/time/mirassol-7396/transferencias',
        'palmeiras': 'https://onefootball.com/pt-br/time/palmeiras-1693/transferencias',
        'cruzeiro': 'https://onefootball.com/pt-br/time/cruzeiro-1794/transferencias',
        'fluminense': 'https://onefootball.com/pt-br/time/fluminense-1666/transferencias',
        'vasco': 'https://onefootball.com/pt-br/time/vasco-da-gama-1790/transferencias',
        'sao paulo': 'https://onefootball.com/pt-br/time/sao-paulo-1677/transferencias',
        'sport': 'https://onefootball.com/pt-br/time/sport-recife-1797/transferencias',
        'bragantino': 'https://onefootball.com/pt-br/time/rb-bragantino-4734/transferencias',
        'vitoria': 'https://onefootball.com/pt-br/time/vitoria-1861/transferencias'
    }
    if time not in links:
        return None, None
    url = links[f'{time}']
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }  # Adicione um User-Agent para evitar bloqueios
    response = requests.get(url, headers=headers)
    # Verificar se a resposta foi bem-sucedida
    
    
    if response.status_code == 200:
        transfersDates = []
        transfersNames = []
        transfersPositions = []
        originTeam = []
        currentTeam = []
        transfersPrice_sujo = []
        transfersPrice = []
        all_data = []
        timeEscudo = []
        exception = []
        soup = BeautifulSoup(response.text, 'html.parser')
        li = soup.find_all('li', class_='TransferCardsList_transferCard__ZGCh4')
        timeEscudo = get_players(time)
        escudo = timeEscudo[0]['Escudo']
        
        if li:
            for item in li:
                datas = item.find('time').get_text(strip=True)
                nomes = item.find('p', class_='title-7-bold TransferCard_contentPlayerInfoName__pHlPG').get_text(strip=True)
                posicoess = item.find('p', class_='title-8-regular TransferCard_contentPlayerInfoPosition__5VIBY').get_text(strip=True)
                
                time1 = item.find('p', class_='title-8-regular TransferCard_secondaryContentText__FozCP')
                
                time2 = item.find('p', class_='title-8-regular TransferCard_secondaryContentText__FozCP TransferCard_secondaryContentTextRight__dZyex')
                
                precoo = item.find('p', class_='title-8-bold TransferCard_footer__xus_5')
                
                
                
                try:
                    exception = item.find('p', class_='title-8-regular TransferCard_contentRenewal__dLjKO')
                except:
                    pass
                if exception:
                    times = time1
                    originTeam.append(times)
                
                if datas:
                    
                        data_transfer =  datas
                        transfersDates.append(data_transfer)
                if nomes:
                        nomees = nomes
                        transfersNames.append(nomees)
                if posicoess:
                    
                        posicoes = posicoess
                        transfersPositions.append(posicoes)
                if time1:
                    
                        
                    times = time1
                    originTeam.append(times.text)
                
                
                if time2:
                    times = time2
                    currentTeam.append(times.text)
                else:
                    currentTeam.append(f'{time.capitalize()}')
                    
                # Função de limpar o preço (tirar o '\xa0')    
                def limpar_preco(preco):
                    # Verificar se o preço contém números
                    if preco and re.search(r'\d', preco):
                        return preco.replace('\xa0', '')
                    return preco
                
                # Condição se tiver preço 
                
                if precoo:
                    preco_sujo = precoo.get_text(strip=True)
                    preco_limpo = limpar_preco(preco_sujo)  # Limpa o preço
                    transfersPrice_sujo.append(preco_sujo)
                    transfersPrice.append(preco_limpo)
                else:
                    transfersPrice_sujo.append('-')
                    
                    
            #  Adicionando os parametros no all_data
            
            
            for data, name, pos, team1, team2, preco in zip(transfersDates, transfersNames, transfersPositions, originTeam, currentTeam, transfersPrice):
                    all_data.append({
                        'Nome': name,
                        'Posicao': pos,
                        'Data': data,
                        'LastTeam': team1,
                        'CurrentTeam': team2,
                        'Preco': preco
            })
            return all_data, escudo
        else:
            return 'NO TRANSFERS'
        

