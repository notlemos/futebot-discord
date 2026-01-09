import aiohttp
from discord.ext import commands 
import discord
from scraping.letterboxd import getFilmsList, getPfp, getDirector
from utils.views import GuessTheMovie
from utils.db import DBUsers, DBRank
from PIL import Image, ImageDraw, ImageFont
import asyncio
from api.tmdbAPI import fetchdata
from io import BytesIO
import re
import requests
class GuessTheMovieCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    @commands.command(name='pixel', aliases=['px'])
    async def guessthemovie(self, ctx, *, user: str = None):
        guildId = ctx.guild.id
        DBUsers.create(guildId)
        discordId = str(ctx.author.id)
        if user:
            DBUsers.replace(guildId, discordId, user)
            savedUser = DBUsers.select(guildId, discordId)
        else:
            savedUser = DBUsers.select(guildId, discordId)
            if not savedUser:
                await ctx.send("Use o comando uma vez com seu user para salvar.")
                return
        async with aiohttp.ClientSession() as session:
            data = await getFilmsList(savedUser, session)
            nome_limpo = re.sub(r'[^\w]', '', data[0]['name']).lower().strip()
            link = "https://letterboxd.com" + data[0]['target']
            diretor = await getDirector(link, session)
            
            poster = "https://image.tmdb.org/t/p/w600_and_h900_bestv2" + fetchdata(data[0]['id'], data[0]['filter'])
            response = requests.get(poster)
            img = Image.open(BytesIO(response.content))
            w, h = img.size
            p = 128
            
            
            small = img.resize((max(1, w//p), max(1, h//p)), Image.NEAREST)
            pixelated = small.resize((w, h), Image.NEAREST)

            buffer = BytesIO()
            pixelated.save(buffer, format="PNG")
            buffer.seek(0)
            embed = discord.Embed(
                title="\n",
                description=f'**What’s the Movie? | Filme Cover Edition** \n\n "**Your Rating: {data[0]['rating']}**"'
            )
            view = GuessTheMovie(img, diretor, data[0]['name'])
            sent = await ctx.send(file=discord.File(buffer, filename="pixel.png"), embed=embed, view=view)
            def check(m):
                    return m.channel == ctx.channel and not m.author.bot and '%' not in m.content
            timeout = 30
            starttime = asyncio.get_event_loop().time()
            try: 
                while True:
                    timeLeft = timeout - (asyncio.get_event_loop().time() - starttime)
                    resposta = await self.bot.wait_for('message', check=check, timeout=timeLeft)
                    resposta_limpa = re.sub(r'[^\w]', '', resposta.content).lower().strip()
                    
                    if nome_limpo in resposta_limpa:
                        buffer2 = BytesIO()
                        img.save(buffer2, format="PNG")
                        buffer2.seek(0)
                        
                        await sent.edit(
                            
                            attachments=[discord.File(buffer2, filename="poster.png")],
                        )
                        await resposta.add_reaction("✅")
                        await resposta.reply(f"{resposta.author.mention} [Acertou Parabéns!!]({link})")
                        break
                    else:
                        await resposta.add_reaction("❌")
                        
            except asyncio.TimeoutError:
                buffer2 = BytesIO()
                img.save(buffer2, format="PNG")
                buffer2.seek(0)
                
                await sent.edit(
                    attachments=[discord.File(buffer2, filename="poster.png")],
                    )
                await ctx.send(f"⏰ Tempo Esgotado! A resposta era... [{data[0]['name']}]({link})")    
                    
async def setup(bot):
    await bot.add_cog(GuessTheMovieCog(bot))