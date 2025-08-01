import discord
from discord.ext import commands
from scraping.letterboxd import getWatchList, getIdMovie2, getpic, getRandomList
from api.tmdbAPI import fetchdata
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

    @commands.command(name="randomwl", aliases=['rwl'])
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
        id_movie = getIdMovie2(link)
        poster = fetchdata(id_movie)
        avatar, _ = getpic(savedUser)

        

   
        poster_url = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{poster}"
        

        embed = discord.Embed(
            title=f"**{name}**",
            url=link,
            description="*• Foi o filme escolhido!*",
            color = discord.Color(0x000c7c)
        )
     
        
        embed.set_image(url=poster_url)
        embed.set_footer(text=savedUser, icon_url=avatar)
        

        
        await ctx.send(embed=embed)
        
        return
    
    @commands.command(name='rm')
    async def top250random(self, ctx):
        def getRandom(db='src/data/top250.db'):
            conn = sqlite3.connect(db)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM filmes ORDER BY RANDOM() LIMIT 1;')
            movie = cursor.fetchone()
            return movie 
        movie = getRandom()
        if movie:
            position = movie[0]
            name = movie[1]
            link = movie[2]
            id_tmdb = movie[3]
            

            poster = fetchdata(id_tmdb)
            embed  = discord.Embed(
                title=f"**{position} - {name}**",
                url=link,
                description="*• Foi o filme escolhido!*",
                color = discord.Color(0x202830)

            )
            embed.set_image(url=f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{poster}")
            embed.set_footer(text="Official Top 250 Narrative 👑", icon_url="https://a.ltrbxd.com/logos/letterboxd-mac-icon.png")
            await ctx.send(embed=embed)
    @commands.command(name='randomList', aliases=['rl'])
    async def randomlist(self, ctx, link: str):
        if not link:
            await ctx.send("Necessário inserir o link de uma lista do letterboxd.")
        movie = getRandomList(link)
        if movie:
            namelist = movie['namelist']
            name = movie['name']
            target = movie['link']
            id = getIdMovie2(target)
            poster = fetchdata(id)
            embed = discord.Embed(
                title=f"{name}",
                url=target,
                description="*• Foi o filme escolhido!*",
                color = discord.Color(0x202830)
            )
            embed.set_image(url=f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{poster}")
            embed.set_footer(text=f"{namelist}", icon_url="https://a.ltrbxd.com/logos/letterboxd-mac-icon.png")
            await ctx.send(embed=embed)
async def setup(bot):
    await bot.add_cog(randomMovieCog(bot))
