import discord
from discord.ext import commands
from discord import app_commands 
import datetime
from scraping.horoscope import horoscope_data
import logging
logger = logging.getLogger(__name__)

class Horoscope(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    @app_commands.command(name="horoscope", description="Horoscopo do seu signo!")
    async def horoscope(self, interaction: discord.Integration, signo: str):
        horoscopo  = await horoscope_data(signo)
        
        if horoscopo:
            data_atual = datetime.datetime.now()
            data_formated = data_atual.strftime("%d/%m/%Y")
            await interaction.response.send_message(f'**Horóscopo do Signo {signo.title()} - {data_formated}**\n\n {horoscopo[6:]}')
        else:
            await interaction.response.send_message(f'SIGNO {signo} NAO EXISTE')
            return
        
async def setup(bot):
    await bot.add_cog(Horoscope(bot))