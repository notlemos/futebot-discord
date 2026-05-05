import discord
from discord import app_commands
from discord.ext import commands
from utils.views import SimulateTable
from utils.db import DBSimulateTable




class Simulate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(name="simular", help="Simulate the brazilian league table `%simular`")
    async def simular(self, ctx, user: discord.Member = None):
        user = user or ctx.author 
        avatar = user.display_avatar.url
        
        simulationId = DBSimulateTable.getOrCreateSimulation(ctx.author.id)
        rows = DBSimulateTable.getPositions(simulationId)
        if len(rows) >= 20:
            await ctx.send(
                "✅ **Sua simulação já foi finalizada.**\n" 
                "Você já escolheu os 20 times da tabela."
            )
            return
        selected = [team for _, team in rows]
        teams = [
            "Atlético-MG",
            "Athletico-PR",
            "Bahia",
            "Botafogo",
            "Bragantino",
            "Chapecoense",
            "Corinthians",
            "Coritiba",
            "Cruzeiro",
            "EC Vitória",
            "Flamengo",
            "Fluminense",
            "Grêmio",
            "Internacional",
            "Mirassol",
            "Palmeiras",
            "Remo",
            "Santos",
            "São Paulo",
            "Vasco da Gama"
        ]
        embed = discord.Embed(
            title="**Tabela do Brasileirão**",
            description="**Temporada 2026**",
            color = discord.Color.blue(),
        )
        embed.add_field(name="Classificação: ", value='')
        view = SimulateTable(teams, user, simulation_id=simulationId)
        view.selected = selected
        embed.set_footer(icon_url=avatar, text=user.display_name)
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(Simulate(bot))
