import discord
from discord import app_commands
from discord.ext import commands
from utils.db import DBFute
from utils.formatters import ShortCuts
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
        rodada = list(DBFute().get_next_empty_round())[0]
        jogos = self.db.get_jogo_by_rodada(rodada)
        embed = discord.Embed(title=f"JOGOS DA RODADA {rodada}")
        for jogo in range(10):
            partida = ShortCuts(jogos[jogo])
            embed.add_field(name=f"{partida.mandante()} x {partida.visitante()}", value=f" ", inline=True)
        await ctx.send(embed=embed)


        
    @commands.command(name="rodadares")
    async def resultados(self, ctx):
        rodada = list(DBFute().get_next_round())[0]
        jogos = self.db.get_jogo_by_rodada(rodada)

        embed = discord.Embed(title=f"JOGOS DA RODADA {rodada}")

        for jogo in range(10):
            partida = ShortCuts(jogos[jogo])
            embed.add_field(name=f"{partida.mandante()} x {partida.visitante()}",
                            value=f"{partida.golMandante()} - {partida.golVisitante()}",
                            inline=True)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(TesteComando(bot))
