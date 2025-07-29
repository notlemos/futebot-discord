import discord
import sqlite3
import os
from api.tmdbAPI import fetch_data
import logging
import random
logger = logging.getLogger(__name__)

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
        jogadores = self.jogadores
        embed = discord.Embed(title=f'Jogador {self.index+1} / {len(self.jogadores)}', description=f'Aqui está as informações do jogador.', color=discord.Color.red())
        embed.add_field(name="Nome", value=jogador['Nome'], inline=False)
        embed.add_field(name='Numero', value=jogador['Número'], inline=False)
        embed.add_field(name='Posição', value=jogador['Posicao'], inline=False)
        embed.add_field(name='Idade', value=jogador['Idade'], inline=False)
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

class ArtilheirosView(discord.ui.View):
    def __init__(self, artilheiros):
        super().__init__(timeout=None)
        self.artilheiros = artilheiros 
        self.index = 0
    def format_embed(self):
        artilheiro = self.artilheiros[self.index]
        artilheiros = self.artilheiros
        embed = discord.Embed(title=f'Jogador {artilheiro['Posicao']} / {len(artilheiros)}')
        embed.add_field(name='Nome', value=artilheiro['Nome'], inline=False)
        embed.add_field(name='Gols', value=artilheiro['Gols'], inline=False)
        return embed 
    @discord.ui.button(label="Anterior", style=discord.ButtonStyle.grey)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.artilheiros) - 1 
        
        embed = self.format_embed()
        
        await interaction.response.edit_message(embed=embed, view=self)
    @discord.ui.button(label="Próximo", style=discord.ButtonStyle.grey)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index += 1
        if self.index >= len(self.artilheiros):
            self.index = 0
            
        embed = self.format_embed()
        await interaction.response.edit_message(embed=embed, view=self)
    @discord.ui.button(label="Fechar", style=discord.ButtonStyle.grey)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Mensagem Fechada! ", embed=None, view=None)

class GuessThereVIEW(discord.ui.View):
    def __init__(self, director, name):
        super().__init__(timeout=30)
        self.director = director
        self.name = name
    @discord.ui.button(label="Add hint", style=discord.ButtonStyle.grey)
    async def giveHint(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0] 

        desc = embed.description
        hint = f"\n- **Directed by: `{self.director}`**"

        embed.description = desc + hint
        button.disabled = True
        await interaction.response.edit_message(embed=embed, view=self)
    @discord.ui.button(label="Jumbled name", style=discord.ButtonStyle.grey)
    async def jumbledName(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0]
        
        text =  self.name
        namesplited = text.split(" ")
        jumbledlist = []
        for word in namesplited:
            words = list(word)
            random.shuffle(words)
            jumbledlist.append(''.join(words).upper())
       
        jumbledname = ' '.join(jumbledlist)
        
        embed.title = f"`{jumbledname}`"
        button.label = "Reshuffle"
        await interaction.response.edit_message(embed=embed, view=self)
    