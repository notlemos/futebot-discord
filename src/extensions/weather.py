import discord 
from discord.ext import commands
from discord import app_commands
from api.weather import weatherdata, date
import logging
logger = logging.getLogger(__name__)



class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        
        
    async def clima(self, interaction: discord.Interaction, cidade: str):
        await interaction.response.defer()
        
        if not date(cidade):
            await interaction.followup.send(f"A cidade {cidade.title()} não foi encontrada.")
            return
        flag, temp, sens, humidity, name, cod = weatherdata(cidade)
        embed = discord.Embed(
            title=f'{name} ',
            description='',
            color=0x93B7C3
        )
        embed.add_field(name=f'Temperatura Atual:', value=f'{temp:.1f}°C', inline=True)
        embed.add_field(name='Sensação: ', value=f'{sens:.1f}°C', inline=True)
        embed.add_field(name=f'Umidade:', value=f'{humidity}%', inline=True)
        embed.set_footer(icon_url=flag, text=f'{cod}')
        embed.set_thumbnail(url='https://em-content.zobj.net/source/apple/391/cloud_2601-fe0f.png')
        await interaction.followup.send(embed=embed)
    @app_commands.command(name="weather", description="Temperatura da cidade.")
    async def weather(self, interaction: discord.Interaction, cidade: str):
        await self.clima(interaction, cidade)

    @app_commands.command(name="clima", description="Temperatura da cidade (apelido).")
    async def clima_alias(self, interaction: discord.Interaction, cidade: str):
        await self.clima(interaction, cidade)    
        
        
    
    @commands.command(name="weather", aliases=["clima", "w"])
    async def weather(self, ctx, *, cidade: str):
        if not date(cidade):
            await ctx.send(f"A cidade {cidade.title()} não foi encontrada.")
            return 
        flag, temp, sens, humidity, name, cod = weatherdata(cidade)
        embed = discord.Embed(
            title=f'{name} ',
            description='',
            color=0x93B7C3
        )
        embed.add_field(name=f'Temperatura Atual:', value=f'{temp:.1f}°C', inline=True)
        embed.add_field(name='Sensação: ', value=f'{sens:.1f}°C', inline=True)
        embed.add_field(name=f'Umidade:', value=f'{humidity}%', inline=True)
        embed.set_footer(icon_url=flag, text=f'{cod}')
        embed.set_thumbnail(url='https://em-content.zobj.net/source/apple/391/cloud_2601-fe0f.png')
        await ctx.send(embed=embed)
async def setup(bot):
    await bot.add_cog(Weather(bot))