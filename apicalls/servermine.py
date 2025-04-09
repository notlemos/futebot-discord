import requests
import os
IP = os.getenv("IpServer")

def serverOn():
    url = f"https://api.mcsrvstat.us/3/{IP}"
    headers = {
            "accept": "application/json",
            }

    response = requests.get(url, headers=headers)
    resposta = response.json()
    
    if response.status_code == 200: 
        
        
        status = resposta['online']
        
        if status == True:
            
            playerList = resposta['players']['online']
            if playerList > 0:
                playersNomes = resposta['players']['list']
                players = []
                
                for player in playersNomes:
                    players.append(player['name'])
                
                return status, playerList, players
            else:
                   
                
                return status, playerList, None
                   
        else:
            return status, None, None
    

