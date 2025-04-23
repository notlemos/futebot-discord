import discord
from discord.ext import commands
from discord import app_commands
from src.scraping.get_fute import get_players
from src.utils.views import JogadoresView 
import logging
logger = logging.getLogger(__name__)

class JogadoresCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="jogadores", description="Lista de jogadores do se utime!")
    async def jogadores(self, interaction: discord.Interaction, time: str):
        await interaction.response.defer()
        jogadores = get_players(time.lower())
        if not jogadores:
            await interaction.followup.send(f"Time **{time}** não encontrado.")
            return
        view = JogadoresView(jogadores)
        embed = view.format_embed()
        
        await interaction.followup.send(embed=embed, view=view)
        
async def setup(bot):
    await bot.add_cog(JogadoresCog(bot))