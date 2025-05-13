import discord 
from discord.ext import commands
from discord import app_commands
import logging
logger = logging.getLogger(__name__)

from apicalls.lastfmcalls import topalbums, toptracks

class lastfmcog(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot 
    
    async def toptracks(self, interaction: discord.Interaction, user: str):
        await interaction.response.defer()
        data = toptracks(user)

        if data:
            embed = discord.Embed(
                title=f'🎵 Top Tracks de {user.title()} 🎵',
                description='',
                color= 534759
            )
            for item in data:
                embed.add_field(name=f'{item['title']} - {item['artist'].title()}', value=f'Scrobbles: {item['playcount']}', inline=False)
            
        await interaction.followup.send(embed=embed)
    @app_commands.command(name='toptracks', description='Top Tracks')
    async def tt(self, interaction: discord.Interaction, user: str):
        await self.toptracks(interaction,user)

async def setup(bot):
    await bot.add_cog(lastfmcog(bot))