from discord.ext import commands
from src.apicalls.servermine import serverOn
import logging
logger = logging.getLogger(__name__)

class ServerStatus(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    @commands.command(name="status")
    async def status(self, ctx):
        status, playerslist, playersnome = serverOn()
        if status == True:
    
            statusMsg = "Online" 
            if playersnome:
                playersFormated = [nome for nome in playersnome]    
            
                playersFormated_str = ", ".join(playersFormated)
                await ctx.send(f"Status: {statusMsg} \n\nPlayers Onlines: {playerslist} \n\nNomes: {playersFormated_str}")
                return
            await ctx.send(f"Status: {statusMsg} \n\nPlayers Onlines: {playerslist}")
        
        else:
            statusMsg = 'Offline'
            await ctx.send(f'Status: {statusMsg}')
async def setup(bot):
    await bot.add_cog(ServerStatus(bot))