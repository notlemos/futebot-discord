import discord 
from discord.ext import commands
import random
import logging
logger = logging.getLogger(__name__)



class ChooseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 

    @commands.command(name="choose")
    async def choose(self, ctx, *, parameter: str):
        if 'ou' in parameter:
            items = [item.strip() for item in parameter.split('ou')]
            
        if ',' in parameter:
            items = [item.strip() for item in parameter.split(',')]
            
        await ctx.send(random.choice(items))



async def setup(bot):
    await bot.add_cog(ChooseCog(bot))