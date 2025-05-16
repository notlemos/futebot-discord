import discord
from discord.ext import commands
from discord import app_commands
from scraping.futedata import getPlayers, getArtilheiros, getEscudo
from utils.views import JogadoresView, ArtilheirosView
import logging
logger = logging.getLogger(__name__)

class JogadoresCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="jogadores", description="Lista de jogadores do seu time!")
    async def jogadores(self, interaction: discord.Interaction, time: str):
        await interaction.response.defer()
        jogadores = getPlayers(time.lower())
        escudo = getEscudo(time.lower())
        if not jogadores:
            await interaction.followup.send(f"Time **{time}** não encontrado.")
            return
        view = JogadoresView(jogadores)
        embed = view.format_embed()
        embed.set_thumbnail(url=escudo)
        await interaction.followup.send(embed=embed, view=view)
        
async def setup(bot):
    await bot.add_cog(JogadoresCog(bot))
    
class ArtilheirosCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    @app_commands.command(name='artilheiros', description='Lista dos artilheiros da temporada do seu time!')
    async def artilheiros(self, interaction: discord.Interaction, time: str):
            await interaction.response.defer()
            artilheiros = getArtilheiros(time.lower())
            escudo = getEscudo(time.lower())
            if not artilheiros:
                await interaction.followup.send(f"Time **{time}** não encontrado.")
                return
            view = ArtilheirosView(artilheiros)
            embed = view.format_embed()
            embed.set_thumbnail(url=escudo)
            await interaction.followup.send(embed=embed, view=view)
async def setup(bot):
    await bot.add_cog(ArtilheirosCog(bot))
    await bot.add_cog(JogadoresCog(bot))