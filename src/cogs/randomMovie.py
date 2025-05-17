import discord
from discord.ext import commands
import aiohttp
import io
from src.scraping.letterboxd import getWatchList, getIdMovie
from apicalls.tmdbAPI import fetch_data


class randomMovieCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="randomwl")
    async def letterboxdwl(self, ctx, *, user: str):
        movie = getWatchList(user)
        name = movie['name']
        target = movie['target']
        id_movie = getIdMovie(f"https://letterboxd.com{target}")
        poster = fetch_data(id_movie)

        link = f"https://letterboxd.com{target}"

        if poster:
            if not poster.startswith("/"):
                poster = "/" + poster
            poster_url = f"https://image.tmdb.org/t/p/original{poster}"
        else:
            poster_url = None

        embed = discord.Embed(
            title=f"**{name}**",
            url=link,
            description="*• Foi o filme escolhido!*",
            color=discord.Color(0x000080)
        )

        if poster_url:
            async with aiohttp.ClientSession() as session:
                async with session.get(poster_url) as resp:
                    if resp.status == 200:
                        data = await resp.read()
                        image_file = discord.File(io.BytesIO(data), filename="poster.jpg")
                        embed.set_image(url="attachment://poster.jpg")
                        await ctx.send(file=image_file, embed=embed)
                        return
                    else:
                        embed.description += "\n\n:warning: Não consegui baixar o pôster."
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(randomMovieCog(bot))
async def setup(bot):
    await bot.add_cog(randomMovieCog(bot))
