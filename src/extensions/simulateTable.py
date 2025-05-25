import discord
from discord import app_commands
from discord.ext import commands
from utils.db import DBFute, DBTabela
from utils.pillowImgs import pillow, pillowTabela
from utils.formatters import ShortCuts
import os 
from scraping.tabelaData import getRodada, getTabela_user

class TesteComando(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DBFute()
        
    @commands.command(name="simula")
    async def simula(self, ctx, *, resultados: str):
        user = str(ctx.author.id)
        tabela = DBTabela()
        
        # Criar tabela personalizada do usuário
        tabela._create_table(user)

        # Preencher com dados iniciais
        for entry in getTabela_user():
            tabela.inserir_times(
                entry["Time"],
                entry["Sigla"],
                entry["Pontos"],
                0,  # 👈 posição inicial zerada
                user
            )


        # Processar resultados
        resList = [p.strip() for p in resultados.split(',')]
        
        rodada = self.db.get_next_empty_round()[0]
        jogos = list(self.db.get_jogo_by_rodada(rodada))

        for jogo, res in zip(jogos, resList):
            gm, gv = map(int, res.lower().split("x"))
            home, away = jogo[3], jogo[5]  # Mandante e visitante

            if gm > gv:
                print(f"[V] {home} venceu {away}")
                tabela.atualizar_pontos(home, 'V', user)
            elif gm == gv:
                print(f"[E] {home} empatou com {away}")
                tabela.atualizar_pontos((home, away), 'E', user)
            elif gv > gm:
                print(f"[V] {away} venceu {home}")
                tabela.atualizar_pontos(away, 'V', user)

            
        # Reordenar posições
        tabela.reorder_positions(user)

        await ctx.send('Simulação aplicada com sucesso!')


    @commands.command(name="rodada")
    async def rodada(self, ctx):
        image = pillow()
        file = discord.File(image, filename="rodada.png")
        await ctx.send(file=file)
        os.remove(image)

        
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
    @commands.command(name="mytabela")
    async def mytabela(self, ctx):
        user = ctx.author.id
        tabela = pillowTabela(user)
        if not tabela:
            await ctx.send("NÃO POSSUI SIMULAÇÃO DE TABELA AINDA.")
        file = discord.File(tabela, filename="tabela.png")
        await ctx.send(file=file)
        os.remove(tabela)
async def setup(bot):
    await bot.add_cog(TesteComando(bot))
