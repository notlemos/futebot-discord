import discord
from discord import app_commands
from discord.ext import commands
from utils.db import DBFute, DBTabela
from utils.pillowImgs import pillow, pillowTabela
from utils.formatters import ShortCuts
import os 
from scraping.tabelaData import getRodada, getTabela_user

class Simulate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = DBFute()
        
    @commands.command(name="palpite")
    async def simula(self, ctx, *, resultados: str):
        user = str(ctx.author.id)
        tabela = DBTabela()
        try: 
            rodada = DBTabela().get_rodada(user)
        except:
            tabela._create_table(user)
            for entry in DBTabela().get_tabela('TODOS'):
                tabela.inserir_times(
                    entry["name"],
                    entry["acronym"],
                    entry["pontos"],
                    0,  
                    entry['rodada'],
                    user
                )



        resList = [p.strip() for p in resultados.split(',')]
        rodada_row = DBTabela().get_rodada(user)
        rodada = rodada_row["rodada"]
        jogos = list(self.db.get_jogo_by_rodada(rodada))

        for jogo, res in zip(jogos, resList):
            gm, gv = map(int, res.lower().split("x"))
            home, away = jogo[3], jogo[5]  # Mandante e visitante

            if gm > gv:
                
                tabela.atualizar_pontos(home, 'V', user)
            elif gm == gv:
                
                tabela.atualizar_pontos((home, away), 'E', user)
            elif gv > gm:
                
                tabela.atualizar_pontos(away, 'V', user)

        tabela.reorder_positions(user)
        tabela.incrementar_rodada(user)
        await ctx.send('Simulação aplicada com sucesso!')

    @commands.command(name="delete")
    async def deltabela(self, ctx):
        user = ctx.author.id
        tabela = DBTabela()
        tabela.excluir_table(user)

        await ctx.send("Tabela Excluida.")
    
    @commands.command(name="start")
    async def start(self, ctx):
        user = ctx.author.id
        tabela = DBTabela()
        tabela._create_table(user)

        await ctx.send("Tabela Criada. Você pode começar a simular vendo a rodada com %`%rodada`")

    @commands.command(name="rodada")
    async def rodada(self, ctx):
        user = ctx.author.id
        image = pillow(user)
        file = discord.File(image, filename="rodada.png")
        await ctx.send(file=file)
        os.remove(image)

        
    @commands.command(name="resultados")
    async def resultados(self, ctx, rodada):
        jogos = list(self.db.get_jogo_by_rodada(rodada))

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
        try:
            tabela = pillowTabela(user)
        except:
            await ctx.send("`%start` para iniciar uma tabela.")
        file = discord.File(tabela, filename="tabela.png")
        await ctx.send(file=file)
        os.remove(tabela)


async def setup(bot):
    await bot.add_cog(Simulate(bot))
