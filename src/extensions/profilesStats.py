import re
import asyncio
import aiohttp
import discord
from discord import app_commands
import datetime
from discord.ext import commands 
from utils.views import DiaryView
from scraping.letterboxd import getratings2, getRatings, getPfp, getDiary, getYears, getHowMuchMovies
from utils.db import DBUsers
stars = [
                    "½☆☆☆☆",
                    "★☆☆☆☆",
                    "★½☆☆☆",
                    "★★☆☆☆",
                    "★★½☆☆",
                    "★★★☆☆",
                    "★★★½☆",
                    "★★★★☆",
                    "★★★★½",
                    "★★★★★"
                ]
class GetRatingsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    @commands.command(name='ratings')
    async def ratings(self, ctx, *, user: str = None):
        guildId = ctx.guild.id
        DBUsers.create(guildId)
        discordId = str(ctx.author.id)
        if user:
            DBUsers.replace(guildId, discordId, user)
            letterboxdUser = user
        else:
            result = DBUsers.select(guildId, discordId)
            if result:
                letterboxdUser = result
            else:
                await ctx.send("Use o comando uma vez com seu user para salvar.")
                return
        async with aiohttp.ClientSession() as session:
            ratings = await getratings2(session, letterboxdUser)
            stars = [
                    "½☆☆☆☆",
                    "★☆☆☆☆",
                    "★½☆☆☆",
                    "★★☆☆☆",
                    "★★½☆☆",
                    "★★★☆☆",
                    "★★★½☆",
                    "★★★★☆",
                    "★★★★½",
                    "★★★★★"
                ]
            desc_lines = [f"- {star} → {num} {perc} " for (num, perc), star in zip(ratings, stars)]
            description = "\n".join(desc_lines)
        

            avatar = await getPfp(session, letterboxdUser)
            

            

            
            embed = discord.Embed(
                title=f"{letterboxdUser}'s ratings",
                description=f"**{description}**",
                color=0x000000
            )
            embed.set_thumbnail(url=f'{avatar}')
            embed.set_footer(icon_url="https://a.ltrbxd.com/logos/letterboxd-mac-icon.png")
            await ctx.send(embed=embed)
    @commands.hybrid_command(name='diary')
    async def diary(self, ctx, user: str = None, year: int = None, month: int = None):
        DBUsers.create(ctx.guild.id)
        discordId = str(ctx.author.id)
        if user:
            DBUsers.replace(ctx.guild.id, discordId, user)
            letterboxdUser = user
        else:
            result = DBUsers.select(ctx.guild.id, discordId)
            if result:
                letterboxdUser = result
            else:
                await ctx.send("Use o comando uma vez com seu user para salvar.")
                return
        ano = year 
        mes = month
        
        if year is None:
            ano = datetime.datetime.now().year
        if month is None:
            mes = datetime.datetime.now().month 
        
        def pad_stars(star_str, length=5):
            base = star_str.replace(' ', '')
            return base + '☆' * (length - len(base))
        def pad_name(names, length=29):
            if len(names) > 29:
                s = names[:28] 
                return s.ljust(length - len(".")) + "."
            else:
                return names
        async with aiohttp.ClientSession() as session:
            yearsPossible = await getYears(session, letterboxdUser)
            if ano not in yearsPossible:
                await ctx.send(f"O usuário não tem filmes logados no ano {ano} !")
            
            names, days, stars = await getDiary(session, letterboxdUser, ano, mes)

            
            max_days = max(len(x) for x in days)

            lines = []
            avatar = await getPfp(session, letterboxdUser)

            for day, name, star in zip(days, names, stars):
                star_padded = pad_stars(star, 5)
                name_padded = pad_name(name, 29)
                line = f"{str(day).rjust(max_days)} | {str(name_padded).ljust(29)} | {star_padded.ljust(5)}"
                lines.append(line)
            description = "```\n" + "\n".join(lines) + "\n```"
            embed = discord.Embed(
                title=f"{letterboxdUser}'s diary",
                description=description,
                color=0x000000
            )
            
            embed.set_thumbnail(url=f'{avatar}')
            embed.set_footer(icon_url="https://a.ltrbxd.com/logos/letterboxd-mac-icon.png", text = f"{letterboxdUser}'s diary for {ano}-{mes}")
            view = DiaryView(self.bot, letterboxdUser, ano, mes, avatar, yearsPossible, ctx)
            await ctx.send(embed=embed, view=view)
    @commands.command(name="stats")
    async def stats(self, ctx, *, user: str = None):
        guildId = ctx.guild.id
        DBUsers.create(guildId)
        discordId = str(ctx.author.id)
        if user:
            DBUsers.replace(guildId, discordId, user)
            letterboxdUser = user
        else:
            result = DBUsers.select(guildId, discordId)
            if result:
                letterboxdUser = result
            else:
                await ctx.send("Use o comando uma vez com seu user para salvar.")
                return
        async with aiohttp.ClientSession() as session:
            years = await getYears(session, letterboxdUser)
            print(years)
            howmuch = await getHowMuchMovies(session, letterboxdUser)
            print(howmuch)
            avatar = await getPfp(session, letterboxdUser)

           
            
            desc_lines = [f"- {year} → {qty} filmes" for year, qty in zip(years, howmuch)]
            description = "\n".join(desc_lines)
            
            embed = discord.Embed(
                title=f"{letterboxdUser}'s diary",
                description=description,
                color=0x000000
            )
            embed.set_thumbnail(url=avatar)
            embed.set_footer(icon_url="https://a.ltrbxd.com/logos/letterboxd-mac-icon.png", text = f"{letterboxdUser}'s total movies: {sum(howmuch)}")
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(GetRatingsCog(bot))