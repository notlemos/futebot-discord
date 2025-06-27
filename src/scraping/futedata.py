import requests
from bs4 import BeautifulSoup
import re
from functools import lru_cache

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0"
}


lru_cache(maxsize=50)
def getPlayers(time): 
    url = f'https://www.ogol.com.br/equipe/{time}'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Tenta encontrar o escudo
    escudo = None
    div2 = soup.find('div', class_='logo')
    if div2:
        img = div2.find('img')
        if img:
            escudo = img.get('src')
    
    jogadores = []

    titulos = soup.find_all('div', class_='innerbox')
    for i in titulos:
        titleDiv = i.find('div', class_='title')
        if not titleDiv:
            continue

        posicao = titleDiv.get_text(strip=True)
        infoStaff = i.find_all('div', class_='staff')

        for staff in infoStaff:
            nome = None
            idade = None
            numero = None

            nomeDiv = staff.find('div', class_='name')
            if nomeDiv:
                nomeDivText = nomeDiv.find('div', class_='text')
                if nomeDivText:
                    nome = nomeDivText.get_text(strip=True)

                idadeSpan = nomeDiv.find('span')
                if idadeSpan:
                    idade = idadeSpan.get_text(strip=True)
                    

                    # Usando regex para encontrar apenas os números na string
                    match = re.search(r'\d+', idade)
                    if match:
                        idade = int(match.group())  # Converte o primeiro número encontrado para inteiro
                          # Exibe a idade convertida
                    else:
                        idade = None  # Se não encontrar um número, define como None
        
            num = staff.find('div', class_='number')
            if num:
                numero = num.get_text(strip=True)
                
                if isinstance(numero, int):
                    numero = numero 
                
            jogadores.append({
                'Nome': nome or "Desconhecido",
                'Posicao': posicao or "N/A",
                'Idade': idade or "N/A",
                'Número': numero or "N/A"
            })

    if jogadores and escudo:
        jogadores[0]['Escudo'] = escudo

        return jogadores
    else:
        return None 


@lru_cache(maxsize=20)
def getEscudo(time): 
    url = f'https://www.ogol.com.br/equipe/{time}'
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Tenta encontrar o escudo
    escudo = None
    div2 = soup.find('div', class_='logo')
    if div2:
        img = div2.find('img')
        if img:
            escudo = img.get('src')
    
    return escudo


@lru_cache(maxsize=50)
def getArtilheiros(time): 
    url = f'https://www.ogol.com.br/equipe/{time}'
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    artilheiros = []

    # Encontrar o bloco que contém os artilheiros
    artilharia_box = soup.find_all('div', class_='zz-tpl-col is-6')
    if len(artilharia_box) < 2:
        return None  # estrutura não encontrada como esperado

    box = artilharia_box[1]

    # Artilheiro principal
    names = box.find('div', class_='names') 
    info = box.find('div', class_='info')
    if names and info:
        first = names.find('a', class_='first_name')
        second = names.find('a', class_='second_name')
        nome = (first.get_text(strip=True) if first else '') + ' ' + (second.get_text(strip=True) if second else '')
        gols_tag = info.find('p', class_='value')
        gols_txt = gols_tag.get_text(strip=True) if gols_tag else '0'
        gols_txt =  re.sub(r'[^\d]', '', gols_txt)
        artilheiros.append({'Posicao': 1, 'Nome': nome.strip(), 'Gols': gols_txt})

    # Demais artilheiros
    bottom = box.find('div', class_='bottom')
    if bottom:
        rows = bottom.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:
                pos = cols[0].get_text(strip=True)
                nome = cols[1].find('a', class_='first_name')
                nome_txt = nome.get_text(strip=True) if nome else ''
                gols_txt = re.sub(r'[^\d]', '', cols[2].get_text(strip=True))
                artilheiros.append({'Posicao': pos, 'Nome': nome_txt, 'Gols': gols_txt})
            
    return artilheiros


@lru_cache(maxsize=50)
def getJogos(time):
    url = f"https://www.ogol.com.br/equipe/{time}"
    response = requests.get(url, headers=headers)
    # Verificar se a resposta foi bem-sucedida
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        homeTeam = []
        awayTeam = []
        dataJogo = []
        statusJogo = []
        all_data = []
        div = soup.find('div', id='team_games')
        if div:
            for s in div.find_all('td',class_='date'):
                dates = s.text
                dataJogo.append(dates)
            for x in div.find_all('td', class_='text home'):
                teamsHome = x.text 
                homeTeam.append(teamsHome )
            for y in div.find_all('td', class_='text away'):
                teamsAway = y.text 
                awayTeam.append(teamsAway)
            for h in div.find_all('td', class_='vs'):
                statsJogo = h.text 
                statusJogo.append(statsJogo)
            for k in div.find_all('td', class_='result'):
                statsJogo = k.text 
                statusJogo.append(statsJogo)
            for data, timecasa, status, timefora in zip(dataJogo, homeTeam, statusJogo, awayTeam):
                all_data.append({
                    'Data': data,
                    'TeamHome': timecasa,
                    'Result': status,
                    'AwayTeam': timefora
                })
        return all_data
    else:
        return None

@lru_cache(maxsize=20)
def getTransfers(time):

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
        'sao-paulo': 'https://onefootball.com/pt-br/time/sao-paulo-1677/transferencias',
        'sport': 'https://onefootball.com/pt-br/time/sport-recife-1797/transferencias',
        'bragantino': 'https://onefootball.com/pt-br/time/rb-bragantino-4734/transferencias',
        'vitoria': 'https://onefootball.com/pt-br/time/vitoria-1861/transferencias'
    }
    if time not in links:
        return None, None
    url = links[f'{time}']
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
        timeEscudo = getPlayers(time)
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
        


