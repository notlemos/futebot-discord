import discord
from discord.ext import commands
from discord import app_commands 
from scraping.letterboxdDatas import getWatchList 
from apicalls.tmdbAPI import get_items
import time
class randomMovieCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.command(name="randomwl")
    async def letterboxdwl(self, ctx, *, user: str):
        start = time.time()
        movie = getWatchList(user)
        name = movie['name']
        target = movie['target']
        if movie:

            poster = get_items(name)
            link = f"https://letterboxd.com{target}"

        embed = discord.Embed(title=f"**{movie['name']}**", url=link, description="*• Foi o filme escolhido!*", color=discord.Color(0x000080))
        embed.set_image(url=f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{poster}")
        

        await ctx.send(embed=embed)
        print(f"Demorou: {time.time() - start:.2f} segundos")
async def setup(bot):
    await bot.add_cog(randomMovieCog(bot))
