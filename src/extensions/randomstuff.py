import discord 
from discord.ext import commands 
import requests 
from api.woah import baixar_woah

class RandomsCogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.command(name="gato")
    async def gato(self, ctx):
            
        url =f'https://api.thecatapi.com/v1/images/search'
        response = requests.get(url)   
        resposta = response.json()

        img = '/tmp/gato.png'
        link = resposta[0]['url']
        with requests.get(link, stream=True) as r:
            r.raise_for_status()
            with open(img, 'wb') as f:
                for chunk in r.iter_content(chunk_size=200):
                    if chunk:
                        f.write(chunk)
        
        
        await ctx.send(file=discord.File(img))

    
    @commands.command(name="cafe")
    async def cafe(self, ctx):
        url = f'https://coffee.alexflipnote.dev/random.json'
        response = requests.get(url)
        resposta = response.json()
        img = resposta['file']
        await ctx.send(img)


    @commands.command(name="woah")
    async def woah(self, ctx):
        path = baixar_woah()
        await ctx.send(file=discord.File(path))


async def setup(bot):
    await bot.add_cog(RandomsCogs(bot))
    