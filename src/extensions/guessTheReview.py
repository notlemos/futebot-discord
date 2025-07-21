import requests 
from bs4 import BeautifulSoup 
import random
import time
import re
import asyncio
import aiohttp

from discord.ext import commands 
from scraping.letterboxd import randomreview 
import sqlite3
conn = sqlite3.connect("src/data/users.db")
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS users(
            discordId TEXT PRIMARY KEY,
            letterboxdUser TEXT NOT NULL
    )
''')
conn.commit()

class GuessTheReviewCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    
    @commands.command(name="guessthereview", aliases=['gtr'])
    @commands.cooldown(rate=1, per=15, type=commands.BucketType.channel)
    async def guessthereview(self, ctx, *, user: str = None):

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
            
        async with aiohttp.ClientSession() as session:
                review, link, nome, releaseDate, rating, logDate = await randomreview(savedUser, session)

                await ctx.send(f"{review}\n\n Guess The Movie! In 30 Seconds..!")

                def check(m):
                    return m.channel == ctx.channel and not m.author.bot and m.content != "%gtr" and m.content != "%guessthereview"
                
                timeout = 30
                starttime = asyncio.get_event_loop().time()

                over = asyncio.Event()

                async def send_clue():
                    await asyncio.sleep(10) 
                    if not over.is_set():
                        await ctx.send(f"*Clue 01* 🕵️‍♂️\n\nWatch Date: {logDate}")
                        
                    await asyncio.sleep(15)
                    if not over.is_set():
                        await ctx.send(f"*Clue 02* 🕵️‍♂️\n\nYour Rating: {rating}")
                    

                asyncio.create_task(send_clue())
                
                try:
                    while True:
                        timeLeft = timeout - (asyncio.get_event_loop().time() - starttime)
                        resposta = await self.bot.wait_for('message', check=check, timeout=timeLeft)
                        if resposta.content.lower().strip() == nome.lower().strip():
                            over.set()
                            await resposta.add_reaction("✅")
                            await resposta.reply(f"{resposta.author.mention} [Acertou Parabéns!!]({link})")
                                
                            break 
                        else:
                            await resposta.add_reaction("❌")
                except asyncio.TimeoutError:
                    over.set()
                    await ctx.send(f"⏰ Tempo Esgotado! A resposta era... [{nome}]({link})")    

async def setup(bot):
    await bot.add_cog(GuessTheReviewCog(bot))