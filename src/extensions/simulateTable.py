import discord
from discord import app_commands
from discord.ext import commands
from utils.db import DBFute
from scraping.tabelaData import getRodada

class TesteComando(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DBFute()
    @commands.command(name="simula")
    async def simula(self, ctx, *, resultados: str ):
        results = resultados
        resultsStrip = [p.strip() for p in results.split(',')]
        
        gols = []
        for i in resultsStrip:
            gol_mandante, gol_visitante = i.split('x')
            gols.append({
                'mandante': gol_mandante,
                'visitante': gol_visitante
            })
        for idx, y in enumerate(gols):
            self.db.inserir_jogos_at(int(y['mandante']), int(y['visitante']), 10, idx+1)
        
        await ctx.send('sucesso.')
    @commands.command(name="rodada")
    async def rodada(self, ctx):
        ...
async def setup(bot):
    await bot.add_cog(TesteComando(bot))
