import discord
from discord.ext import commands
from discord import app_commands 
import datetime
from scraping.horoscope import horoscope_data
import logging
logger = logging.getLogger(__name__)

class Horoscope(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    @commands.command(name="horoscopo", description="Horoscopo do seu signo!")
    async def horoscope(self, ctx, *, signo: str):
        title, horoscopo, img, footer  = await horoscope_data(signo)

        if title and horoscopo and img:

            embed = discord.Embed(
                title=title,
                description=horoscopo,
                color=0x000000
            )
            embed.set_thumbnail(url=img)
            embed.set_footer(icon_url=img, text=footer.split(" ")[4])
            await ctx.reply(embed=embed)
        else:
            await ctx.reply("erro")
        
        
async def setup(bot):
    await bot.add_cog(Horoscope(bot))