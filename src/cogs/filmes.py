import discord 
from discord.ext import commands
from discord import app_commands
import sqlite3
from src.utils.views import FilmesView
from src.utils.db import DBManager
import logging
logger = logging.getLogger(__name__)
allowed_guild_id = 928519278188167208


class Filmes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        self.db = DBManager
        
        
    @app_commands.command(name="addfilme", description="Adiciona um Filme")
    async def saveMovie(self, interaction: discord.Interaction, filme: str, nota1: float, nota2: float):
        member = interaction.user 
        self.db.save_movie(member, filme, nota1, nota2)
        await interaction.response.send_message("Filme adicionado com sucesso!")
        
    @app_commands.command(name="delfilme", description="Remove um filme")
    async def delFilme(self, interaction: discord.Interaction, movie_id: int):
        self.db.delete_movie(movie_id)
        await interaction.response.send_message(f"Filme deletado")
        
    @app_commands.command(name="listmovies", description="Lista de filmes!")
    async def listMovie(self, interaction: discord.Interaction):
        conn = sqlite3.connect("/app/data/database.sqlite")
        cursor = conn.cursor()
        cursor.execute("SELECT id, filme, name, nota1, nota2 FROM filmes")
        filmes = cursor.fetchall()
        conn.close()
        
        if interaction.guild.id != allowed_guild_id:
            await interaction.response.send_message("Este comando não está disponível neste servidor.", ephemeral=True)
            return
        if not filmes:
            await interaction.response.send_message(content="A LISTA ESTÁ VAZIA!!!")
            return

        view = FilmesView()
        await interaction.response.send_message(embed=view.format_embed(), view=view)
async def setup(bot):
    await bot.add_cog(Filmes(bot))