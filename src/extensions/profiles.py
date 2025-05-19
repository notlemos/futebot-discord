import discord 
from discord.ext import commands
from discord import app_commands
import logging
logger = logging.getLogger(__name__)


class ProfileView(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.command(name="avatar")
    async def avatar(self, ctx, user: discord.Member = None):
        user = user or ctx.author 
        avatar = user.display_avatar
        if not user.avatar:
            await ctx.send(f"{user.name} não possui avatar.")
            return 
        file = await avatar.with_size(1024).to_file()
        await ctx.send(file=file)

    
    @commands.command(name="banner")
    async def banner(self, ctx, user: discord.Member = None):
        user = user or ctx.author 
        user = await self.bot.fetch_user(user.id)
        
        if not user.banner:
            await ctx.send(f"{user.name} não possui banner.")
            return 
        banner = user.banner 
        file = await banner.with_size(1024).to_file()
        
        await ctx.send(file=file)
async def setup(bot):
    await bot.add_cog(ProfileView(bot))
    