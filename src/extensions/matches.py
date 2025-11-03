import discord 
from discord.ext import commands
from discord import app_commands 
from scraping.futedata import getJogos, getPlayers, getEscudo
from scraping.futedata import getMatchsToday
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import logging
logger = logging.getLogger(__name__)

class JogosView(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
   
    @app_commands.command(name="jogos", description="Jogos do seu Time.")
    async def jogos(self, interaction: discord.Interaction, time: str):
        await interaction.response.defer()
        
        jogos_data = getJogos(time)
        jogadores = getPlayers(time)
        jogadores = jogadores 
        index = 0
        
        jogador = jogadores[index]
        embed =  discord.Embed(title=f'⚔️ Tabela de jogos do {time.capitalize()} ⚔️', description='')
        
        for row in  jogos_data:
            embed.add_field(
                name=f'{row['TeamHome']} {row['Result']} {row['AwayTeam']}',
                value=f'{row['Data']}',
                inline=False
            )
        escudo = getEscudo((time))
        embed.set_thumbnail(url=escudo)
        await interaction.followup.send(embed=embed)
    @app_commands.command(name="matchs", description="Jogos do dia.")
    async def matchs(self, interactions: discord.Interaction):
        await interactions.response.defer()
        jogos = getMatchsToday()
        print(jogos)
        embed =  discord.Embed(title=f'⚔️ Tabela de jogos de hoje ⚔️', description='')
        for row in jogos:
            data_og = row['date']
            dt = datetime.fromisoformat(data_og.replace("Z", "+00:00")).astimezone(ZoneInfo("America/Sao_Paulo"))
            
            data = dt.strftime("%H:%M")
            embed.add_field(
                
                name=f'{row['home_team']} x {row['away_tem']} - {data}',
                value=f'{row['leaguename']}'
            )
        await interactions.followup.send(embed=embed)
        

async def setup(bot):
    await bot.add_cog(JogosView(bot))