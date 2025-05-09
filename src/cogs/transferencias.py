import discord 
from discord.ext import commands
from discord import app_commands
from scraping.futedata import getTransfers
from utils.views import TransfersViews
import logging
logger = logging.getLogger(__name__)
class TransfersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="transferencias", description="Mostra as ultimas transferências do seu time")
    async def transfers_command(self, interaction: discord.Interaction, time:str):
        await interaction.response.defer()
        transferencias, escudo = getTransfers(time.lower())
        if transferencias is None: 
            await interaction.followup.send(f"⚠️ Time **{time}** não encontrado! Verifique o nome e tente novamente.")
            return 
        if not transferencias:
            await interaction.followup.send("Não foi possível obter os dados das transferências!")
            return  
        view = TransfersViews(transferencias, escudo)
        embed = view.format_embed()
        
        await interaction.followup.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(TransfersCog(bot))