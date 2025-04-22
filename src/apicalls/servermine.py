import requests
import os
IP = os.getenv("IpServer")

def serverOn():
    url = f"https://mcapi.us/server/status?ip={IP}"
    headers = {
            "accept": "application/json",
            }

    response = requests.get(url, headers=headers)
    resposta = response.json()
    
    if response.status_code == 200: 
        
        
        status = resposta['online']
        
        if status == True:
            playerList = resposta['players']['now']
            print(playerList)
            if playerList > 0:
                players = []
                for i in range(playerList):
                    playersNomes = resposta['players']['sample'][i]['name']
                    players.append(playersNomes)
                return status, playerList, players
            else:
                return status, playerList, None     
        else:
            return status, None, None

    

