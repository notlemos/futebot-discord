import discord
from api.tmdbAPI import fetch_data
from scraping.letterboxd import getDiary
import re
import asyncio
import aiohttp
import discord
import datetime
from scraping.letterboxd import getRatings, getPfp, getDiary, getYears
import logging
import random
from io import BytesIO
from PIL import Image
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
class GuessTheMovie(discord.ui.View):
    def __init__(self, img, diretor, name):
        super().__init__(timeout=30)
        self.img = img
        self.diretor = diretor
        self.name = name
        self.p = 128
        self.flag = True
    @discord.ui.button(label="Add hint", style=discord.ButtonStyle.grey)
    async def giveHint(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = interaction.message.embeds[0] 
        
        if self.flag == True:
            hint = f"\n- **Directed by: `{self.diretor}`**"
            desc = embed.description
            embed.description = desc + hint
        if self.p <= 16:
            button.disabled = True
            return 
        
        self.p -= 16
        w, h = self.img.size
        small = self.img.resize((max(1, w//self.p), max(1, h//self.p)), Image.NEAREST)
        pixelated = small.resize((w, h), Image.NEAREST)

        buffer = BytesIO()
        pixelated.save(buffer, format="PNG")
        buffer.seek(0)
        
        file = discord.File(buffer, filename="pixel.png")
        self.flag = False
        await interaction.response.edit_message(
            embed = embed,
            attachments=[file],
            view=self
        )
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
    
    
class DiaryView(discord.ui.View):
    def __init__(self, bot, letterboxdUser, ano, mes, avatar, yearsPossible, ctx):
        super().__init__(timeout=60)
        self.bot = bot
        self.letterboxdUser = letterboxdUser
        self.ano = ano
        self.mes = mes
        self.avatar = avatar
        self.yearsPossible = yearsPossible
        self.ctx = ctx

    async def update_embed(self, interaction):
        async with aiohttp.ClientSession() as session:
            
            names, days, stars = await getDiary(session, self.letterboxdUser, self.ano, self.mes)
            def pad_stars(star_str, length=5):
                base = star_str.replace(' ', '')
                return base + '☆' * (length - len(base))

            def pad_name(names, length=29):
                if len(names) > 29:
                    s = names[:28] 
                    return s.ljust(length - len(".")) + "."
                else:
                    return names

            max_days = max(len(x) for x in days) if days else 2
            lines = []
            for day, name, star in zip(days, names, stars):
                star_padded = pad_stars(star, 5)
                name_padded = pad_name(name, 29)
                line = f"{str(day).rjust(max_days)} | {str(name_padded).ljust(29)} | {star_padded.ljust(5)}"
                lines.append(line)
            description = "```\n" + "\n".join(lines) + "\n```"

            embed = discord.Embed(
                title=f"{self.letterboxdUser}'s diary",
                description=description,
                color=0x000000
            )
            embed.set_thumbnail(url=self.avatar)
            embed.set_footer(
                icon_url="https://a.ltrbxd.com/logos/letterboxd-mac-icon.png",
                text=f"{self.letterboxdUser}'s diary for {self.ano}-{self.mes}"
            )
            await interaction.response.edit_message(embed=embed, view=self)
    @discord.ui.button(label="⬅ Month", style=discord.ButtonStyle.blurple)
    async def prevMonth(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.mes -= 1
        if self.mes < 1:
            self.mes = 12
            self.ano -= 1
        await self.update_embed(interaction)
    @discord.ui.button(label="➡ Month", style=discord.ButtonStyle.blurple)
    async def nextMonth(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.mes += 1
        if self.mes > 12:
            self.mes = 1
            self.ano += 1
        await self.update_embed(interaction)
    @discord.ui.button(label="⬅ Year", style=discord.ButtonStyle.grey)
    async def prevYear(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.ano -= 1
        if self.ano not in self.yearsPossible:
            self.ano = self.yearsPossible[0]
        await self.update_embed(interaction)
    @discord.ui.button(label="➡ Year", style=discord.ButtonStyle.grey)
    async def nextYear(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.ano += 1
        if self.ano not in self.yearsPossible:
            self.ano = self.yearsPossible[0]
        await self.update_embed(interaction)