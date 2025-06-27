from discord.ext import commands
import discord

class Geral(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        
        texto = "📜 **Comandos de texto:**\n"
        for cmd in self.bot.commands:
            if not cmd.hidden:
                texto += f"`%{cmd.name}` - {cmd.help or 'Sem descrição.'}\n"

       
        texto += "\n🤖 **Comandos slash:**\n"
        for slash in self.bot.tree.get_commands():
            texto += f"/{slash.name} - {slash.description}\n"

        await ctx.send(texto)
        


async def setup(bot):
    await bot.add_cog(Geral(bot))
