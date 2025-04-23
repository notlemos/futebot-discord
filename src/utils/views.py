import discord
import sqlite3
import os
from src.apicalls.get_movies import get_items




class FilmesView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.conn = sqlite3.connect("//app/data/database.sqlite")
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT id, filme, name, nota1, nota2 FROM filmes")
        self.filmes = self.cursor.fetchall()
        self.conn.close()
        self.index = 0
    
    def format_embed(self):
        dados = self.filmes[self.index]
        
        movie_id, filme, name, nota1, nota2 = dados
        
        def stars(nota):
            nota = nota
            
            estrelas = ["<:intero:1355770128310075543> ", "<:meia:1355770368899551345>  "] # Stars emote // Full star and half star
            
            inteiro = int(nota) # Only the integer part 
            
            meia = int((inteiro - nota) * 2) # Getting de float part, if 0 == None, else += half star
            
            resultado = estrelas[0] * inteiro 
            
            if meia:
                resultado += estrelas[1]
            return resultado
        
        embed = discord.Embed(
            title='🎥  LISTA DE FILMES ',
            description='',
            color= 534759
        )
        embed.add_field(name=f'{movie_id}️⃣   {filme.title()}', value=f'Escolhido por: {name}', inline=False)
        embed.add_field(name=f"**Nota do {os.getenv("NAME1")}:**", value=f"{stars(nota1)}", inline=False)
        embed.add_field(name=f"**Nota da {os.getenv("NAME2")}:**", value=f"{stars(nota2)}", inline=False)
        
        url = f'https://image.tmdb.org/t/p/w600_and_h900_bestv2{get_items(filme)}'
        embed.set_thumbnail(url=url)
        return embed
    
    @discord.ui.button(label="Anterior", style=discord.ButtonStyle.grey)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.filmes) - 1
        embed = self.format_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    @discord.ui.button(label="Próximo", style=discord.ButtonStyle.grey)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index += 1
        if self.index >= len(self.filmes):
            self.index = 0
        embed = self.format_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    @discord.ui.button(label="Fechar", style=discord.ButtonStyle.grey)
    
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Mensagem Fechada!", embed=None, view=None)


class TransfersViews(discord.ui.View):
    def __init__(self, transferencias,escudo):
        super().__init__(timeout=None)
        self.index = 0
        self.transferencias = transferencias
        self.escudo = escudo
    def format_embed(self):
        transfer = self.transferencias[self.index]
        esc = self.escudo
        embed = discord.Embed(title=f'Mercado da Bola   {self.index+1} / {len(self.transferencias)}', description='Informações sobre o mercado do seu time!', color = discord.Color.red())
        embed.add_field(name='Nome do jogador:', value=transfer['Nome'], inline=True)
        embed.add_field(name='Posição do jogador:', value=transfer['Posicao'], inline=True)
        embed.add_field(name='Data da transferência:', value=transfer['Data'], inline=True)
        embed.add_field(name='Ultimo time:', value=transfer['LastTeam'], inline=True)
        embed.add_field(name='Atual time:', value=transfer['CurrentTeam'], inline=True)
        embed.add_field(name='Preço/Tipo', value=transfer['Preco'], inline=True)
        embed.set_thumbnail(url=f'{esc}')
        return embed
        
    @discord.ui.button(label="Anterior", style=discord.ButtonStyle.grey)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.transferencias) - 1 
        
        embed = self.format_embed()
        
        await interaction.response.edit_message(embed=embed, view=self)
    @discord.ui.button(label="Próximo", style=discord.ButtonStyle.grey)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index += 1
        if self.index >= len(self.transferencias):
            self.index = 0
            
        embed = self.format_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    @discord.ui.button(label="Fechar", style=discord.ButtonStyle.grey)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Mensagem Fechada! ", embed=None, view=None)


class JogadoresView(discord.ui.View):
    def __init__(self, jogadores):
        super().__init__(timeout=None)
        self.jogadores = jogadores 
        self.index = 0
    def format_embed(self):
        jogador = self.jogadores[self.index]
        embed = discord.Embed(title=f'Jogador {self.index+1} / {len(self.jogadores)}', description=f'Aqui está as informações do jogador.', color=discord.Color.red())
        embed.add_field(name="Nome", value=jogador['Nome'], inline=False)
        embed.add_field(name='Numero', value=jogador['Número'], inline=False)
        embed.add_field(name='Posição', value=jogador['Posicao'], inline=False)
        embed.add_field(name='Idade', value=jogador['Idade'], inline=False)
        embed.set_thumbnail(url=f'{jogador['Escudo']}')
        return embed 
    @discord.ui.button(label="Anterior", style=discord.ButtonStyle.grey)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.jogadores) - 1 
        
        embed = self.format_embed()
        
        await interaction.response.edit_message(embed=embed, view=self)
    @discord.ui.button(label="Próximo", style=discord.ButtonStyle.grey)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index += 1
        if self.index >= len(self.jogadores):
            self.index = 0
            
        embed = self.format_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    @discord.ui.button(label="Fechar", style=discord.ButtonStyle.grey)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Mensagem Fechada! ", embed=None, view=None)
