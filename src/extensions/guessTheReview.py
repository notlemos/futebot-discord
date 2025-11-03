import re
import asyncio
import aiohttp
import discord
from discord.ext import commands 
from scraping.letterboxd import randomreview, getPfp, getDirector
from utils.views import GuessThereVIEW
from utils.db import DBUsers, DBRank




class GuessTheReviewCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    
    @commands.command(name="guessthereview", aliases=['gtr'])
    async def guessthereview(self, ctx, *, user: str = None):
        guildId = ctx.guild.id
        DBUsers.create(guildId)
        DBRank.create(guildId)
        discordId = str(ctx.author.id)
        if user:
            DBUsers.replace(guildId, discordId, user)
            savedUser = DBUsers.selectOneRandom(guildId)[0]
        else:
            result = DBUsers.select(guildId, discordId)
            if result:
                savedUser = DBUsers.selectOneRandom(guildId)[0]
            else:
                await ctx.send("Use o comando uma vez com seu user para salvar.")
                return
        
        async with aiohttp.ClientSession() as session:
                review, link, nome, releaseDate, rating, logDate, target = await randomreview(savedUser, session)
                nome_limpo = re.sub(r'[^\w]', '', nome).lower().strip()
                
                
                embed = discord.Embed(
                    title="\n",
                    description=f'**What’s the Movie? | Review Edition** \n\n "*{review.capitalize()}*"\n\n - **Released on: `{releaseDate}`** \n- **Your Rating:  {rating.strip()}**\n- **Watched on: `{logDate}`**',
                    color=0x000000
                )
                pic = await getPfp(session, savedUser)
                embed.set_footer(text=savedUser, icon_url=pic)
                director = await getDirector(f"https://letterboxd.com{target}", session)
                view = GuessThereVIEW(director, nome)
                await ctx.send(embed=embed, view=view)
                
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
                            if DBRank.getUserById(guildId, resposta.author.id):
                                DBRank.incrementScore(guildId, resposta.author.id)
                            else:
                                DBRank.addPerson(guildId, resposta.author.id, resposta.author.name)
                                DBRank.incrementScore(guildId, resposta.author.id)
                            await resposta.add_reaction("✅")
                            await resposta.reply(f"{resposta.author.mention} [Acertou Parabéns!!]({link})")
                                
                            break 
                        else:
                            await resposta.add_reaction("❌")
                except asyncio.TimeoutError:
                    await ctx.send(f"⏰ Tempo Esgotado! A resposta era... [{nome}]({link})")    
                    


    @commands.command(name="top")
    async def top(self, ctx):
        guildId = ctx.guild.id
        rank = DBRank.getRankOrder(guildId)
        avatar = False
        description = "1. Vazio."
        if rank:
            user = await self.bot.fetch_user(int(rank[0][2]))
            avatar = user.display_avatar
            description = ""
            
            max_nome = max(len(i[0]) for i in rank)
            max_idx = len(str(len(rank)))

            lines = [
                f"{str(idx).zfill(2).rjust(max_idx)}. {i[0].ljust(max_nome)}  {i[1]}"
                for idx, i in enumerate(rank, start=1)
            ]
                
        
            description = "```\n" + "\n".join(lines) + "\n```"
        embed = discord.Embed(
            title="Server Ranking | Guess The Review",
            description=description,
            color=0x000000
        )
        embed.set_footer(icon_url=f"{ctx.guild.icon.url}", text=f"{ctx.guild.name}")
        if avatar:
            embed.set_thumbnail(url=f'{user.display_avatar.url}')
        await ctx.send(embed=embed)
async def setup(bot):
    await bot.add_cog(GuessTheReviewCog(bot))