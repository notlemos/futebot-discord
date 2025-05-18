import discord
from discord.ext import commands
import aiohttp
import io
from scraping.letterboxd import getWatchList, getIdMovie, getProfile
from apicalls.tmdbAPI import fetch_data
import sqlite3
import time





conn = sqlite3.connect("src/data/users.db")
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS users(
            discordId TEXT PRIMARY KEY,
            letterboxdUser TEXT NOT NULL
    )
''')
conn.commit()




class randomMovieCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="randomwl")
    async def letterboxdwl(self, ctx, *, user: str = None):
        

        discordId = str(ctx.author.id)
        if user:
            c.execute('REPLACE INTO users (discordId, letterboxdUser) VALUES (?, ?)', (discordId, user))
            conn.commit()
            savedUser = user
        else:
            c.execute('SELECT letterboxdUser FROM users WHERE discordId = ?', (discordId,))
            result = c.fetchone()
            if result:
                savedUser = result[0]
            else:
                await ctx.send("Use o comando uma vez com seu user para salvar.")
                return

        
        movie = getWatchList(savedUser)
        name = movie['name']
        target = movie['target']
        link = f"https://letterboxd.com{target}"
        id_movie = getIdMovie(link)
        poster = fetch_data(id_movie)
        avatar = getProfile(savedUser)

        

   
        poster_url = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{poster}"
      

        embed = discord.Embed(
            title=f"**{name}**",
            url=link,
            description="*• Foi o filme escolhido!*",
            color=discord.Color(0x000080)
        )
     
        
        embed.set_image(url=poster_url)
        embed.set_footer(text=savedUser, icon_url=avatar)
        await ctx.send(embed=embed)
        
        return
                   
async def setup(bot):
    await bot.add_cog(randomMovieCog(bot))
