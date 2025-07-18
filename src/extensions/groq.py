import discord 
from discord.ext import commands 
from api.groqAPI import groqFut, groqPop, groqResenhemetro, groqVar


class GroqCommandsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="explique", help="Explain something in football terms.")
    async def explique(self, ctx, *, msg: str):
        resposta = groqFut(msg)
        await ctx.send(resposta)
    
    @commands.command(name="expliquepop", help="Explain something in pop terms")
    async def expliquepop(self, ctx, *, msg: str):
        resposta = groqPop(msg)
        await ctx.send(resposta)
        
    @commands.command(name="var", help="See the Video Assistant Referee to see who's right in the discussion.")
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.user)
    async def var(self, ctx):
        messages = [message async for message in ctx.channel.history(limit=20)]
        contents = [
            f"**{message.author.display_name}**: {message.content}"
            for message in reversed(messages)
            if message.author.display_name != 'futebot' and not message.content.startswith('%')
        ]
        varCheck = groqVar(contents)
        
        await ctx.send(varCheck)
    @commands.command(name="resenhometro")
    @commands.cooldown(rate=1, per=300, type=commands.BucketType.guild)
    async def resenhometro(self,ctx):
        messages = [message async for message in ctx.channel.history(limit=50)]
    
        contents = [f"**{message.author.display_name.upper()}**: {message.content}" for message in reversed(messages)]
        
        resenhometro = groqResenhemetro(contents)
        
        await ctx.send(resenhometro)
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"⏳ Esse comando está em cooldown! Tente novamente em {error.retry_after:.1f} segundos.")
        else:
            raise error
async def setup(bot):
    await bot.add_cog(GroqCommandsCog(bot))