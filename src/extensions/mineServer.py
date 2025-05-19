from discord.ext import commands
from api.servermine import serverOn
import logging
logger = logging.getLogger(__name__)

class ServerStatus(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    @commands.command(name="status", aliases=["server"])
    async def status(self, ctx):
        status, playerslist, playersnome = serverOn()
        
        if status == False: 
            statusMsg = 'Offline'
            await ctx.send(f'Status: {statusMsg}')
            return 
    
        statusMsg = "Online" 
        if playersnome:
            playersFormated = [nome for nome in playersnome]    
            
            playersFormated_str = ", ".join(playersFormated)
            await ctx.send(f"Status: {statusMsg} \n\nPlayers Onlines: {playerslist} \n\nNomes: {playersFormated_str}")
            return
        
        await ctx.send(f"Status: {statusMsg} \n\nPlayers Onlines: {playerslist}")
        return 
        
            
async def setup(bot):
    await bot.add_cog(ServerStatus(bot))