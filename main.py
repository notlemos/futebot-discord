from get_fute import get_standings,get_artilheiros, get_jogos, get_players, get_transfers
from get_movies import get_items

import sqlite3

import discord
from discord.ext import commands
from discord import Spotify

from dotenv import load_dotenv
import os


# Chama a função para carregar o token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all() # Permissões do bot.
bot = commands.Bot(command_prefix='%', intents=intents) # Prefixo do bot


def create_db():
    conn = sqlite3.connect("/app/data/database.sqlite")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS filmes (id INTEGER PRIMARY KEY, name TEXT, filme TEXT, nota1 FLOAT, nota2 FLOAT)''')
    
    conn.commit()
    conn.close()

def save_dates(member, user_filme, user_nota1, user_nota2):
    conn = sqlite3.connect("/app/data/database.sqlite")
    cursor = conn.cursor()
    user_name = member.name
    cursor.execute("INSERT OR IGNORE INTO filmes (name, filme, nota1, nota2) VALUES (?, ?, ?,?)", (user_name, user_filme, user_nota1, user_nota2))
    conn.commit()
    conn.close()


def delete_dates(movie_id: int):
    conn = sqlite3.connect("/app/data/database.sqlite")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM filmes WHERE id = ?", (movie_id,))
    conn.commit()
    
    cursor.execute("""CREATE TEMP TABLE temp_filmes AS SELECT ROW_NUMBER() OVER () AS new_id, filme, name, nota1, nota2 FROM filmes ORDER BY id ASC;""")
    
    cursor.execute("DELETE FROM filmes")
    
    cursor.execute("INSERT INTO filmes (id, filme, name, nota1, nota2) SELECT new_id, filme, name, nota1, nota2 FROM temp_filmes ")
    
    conn.commit()
    conn.close()
    
    
allowed_guild_id = 928519278188167208
# Comando evento para quando o bot starta.

@bot.event 
async def on_ready():
        #await bot.tree.sync()
        print(f'Logged on {bot.user}')
        
        create_db()

async def a():
    for guild in bot.fetch_guilds(limit=150):
        print(guild.name)                  
print(a)
# Comando para sincronizar os slash commands.        

@bot.command()
async def test(ctx):
    await ctx.send('testadooo 23 ')        

@bot.command()
async def davigay(ctx):
    await ctx.send('davi é gay.')        
        
@bot.command()
async def sincronizar(ctx:commands.Context):
    if ctx.author.id == 364874163455787028:
        sincs = await bot.tree.sync()
        await ctx.reply(f"{len(sincs)} comandos sincronizados")
    else:
        await ctx.reply("no.")

@bot.tree.command(description='Responde o usuário com olá')
async def ola(interact:discord.Interaction):
    await interact.response.send_message(f'Olá, {interact.user.name}')


# Comando que retorna a tabela do paulista. (+ command)  
  
  
@bot.command()
async def tabela (ctx, grupo: str = None):
    if not grupo:
        await ctx.send("Por favor informe o grupo, (A, B C ou D)")
        return

    standinng_datas = get_standings(grupo)
    if not standinng_datas:
        await ctx.send(f"O grupo **{grupo}** não foi encontrado.")
        return
    #table = format_table(standinng_datas)
    
    embed = discord.Embed(
        title='🏆 Tabela do Paulistão',
        description=f'Aqui está a tabela do **Grupo {grupo.upper()}**',
        color = discord.Color.blue()
    )
    for idx, row in enumerate(standinng_datas, start=1):
        embed.add_field(
            name=f'{idx}️⃣ {row['Time']}',
            value=f'**Pontos**: {row['Pontos']}',
            inline=False
        )
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/pt/7/71/Federa%C3%A7%C3%A3o_Paulista_de_Futebol_logo.png")
    await ctx.send(embed=embed)



# Comando que retorna info de jogadores (+ command) (apenas do santos)


# Comando que retorna os artilheiros (+ command) (só do santos)

    
@bot.command()
async def artilheiros(ctx):
    artilheiros_data = get_artilheiros()
    embed = discord.Embed(
        title='⚽ARTILHEIROS DO ANO - SANTOS FC⚽',
        description='**TOP 5 ARTILHEIROS TEMPORADA 25**',
        color= discord.Color.red()
    )
    for idx, row in enumerate(artilheiros_data, start=1):
        embed.add_field(
            name=f'{idx}️⃣ {row['Nome']}',
            value=f'',
            inline=False
        )
        embed.add_field(
            name=f'**Jogos: ** {row['Jogos']}',
            value=f'',
            inline=False
        )
        embed.add_field(
            name=f'**Gols:** {row['Gols']}',
            value=f'',
            inline=False
        )
        
        
    await ctx.send(embed=embed)


@bot.command()
async def sp(ctx):
    img = 'https://s2-ge.glbimg.com/PMy9XqvzWBDwZBO1xZRiAEnN9lI=/0x0:744x533/1008x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_bc8228b6673f488aa253bbcb03c80ec5/internal_photos/bs/2020/x/8/THbBLeSWaI3WqeM9DW4A/folha.jpg'
    
    embed = discord.Embed(
        title='A VERDADE SOBRE 1990.',
        description='CHEGA DE MENTIRAS.',
        color= discord.Color.red()
    )
    embed.set_image(url=f'{img}')
    await ctx.send(embed=embed)

# Comando que retorna os ultimos e próximos jogos (+ command) (só do santos)


@bot.command()
async def jogos(ctx, time):
    jogos_data = get_jogos(time)
    jogadores = get_players(time)
    jogadores = jogadores 
    index = 0
    
    jogador = jogadores[index]
    embed = discord.Embed(
        title=f'⚔️ Ultimos jogos do {time.capitalize()} ⚔️',
        description='ultimos resultados e próximos jogos',
        color = discord.Color.dark_embed()
    )
    for row in jogos_data:
        embed.add_field(
            name=f'{row['TeamHome']} {row['Result']} {row['AwayTeam']}',
            value=f'{row['Data']}',
            inline=False
        )
    embed.set_thumbnail(url=f"{jogador['Escudo']}")
    #embed.set_image(url="https://upload.wikimedia.org/wikipedia/commons/1/15/Santos_Logo.png")
    embed.set_footer( text= "", icon_url="")
    await ctx.send(embed=embed)

# COMANDO QUE RETORNA O AVATAR DO USUARIO

@bot.command()
async def avatar(ctx, user: discord.Member = None):
    user = user or ctx.author 
    avatar = user.display_avatar
    if not user.avatar:
        await ctx.send(f'{user.name} não possui avatar.')
        return
    file = await  avatar.with_size(1024).to_file()
    
    await ctx.send(file=file)



# COMANDO SPOTIFY RETORNA OS DADOS DA MUSICA QUE ESTA SENDO OUVIDA PELO USUARIO

@bot.command()
async def spotify(ctx, user: discord.Member = None):
    
    # Tempo da musica vem em deltatime 
    
    def format_timedelta_to_mmss(td):
        total_seconds = int(td.total_seconds())
        minutes = total_seconds // 60 
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"
    user = user or ctx.author
    
    if not user.activities:
        await ctx.send(f'{user.name} não possui atividade.')
    for activity in user.activities:
        if isinstance(activity, Spotify):
                    
            embed = discord.Embed(
                title=f"{user.display_name}'s spotify",
                description=f"",
                color= discord.Color.blue()
                )
            embed.set_thumbnail(url=activity.album_cover_url)
            embed.add_field(
                name=f'Music Name  ',
                value=f'{activity.title}',
                inline=True
            )
            embed.add_field(
                name=f'Artist Name  ',
                value=f'{activity.artist}',
                inline=True
            )
            embed.add_field(
                name=f'Album Name  ',
                value=f'{activity.album}',
                inline=True
            )
            duration = activity.duration  # duração total (tipo timedelta)
            start_time = activity.start  # datetime do início
            elapsed_time = discord.utils.utcnow() - start_time

            # Formata para MM:SS
            elapsed_str = format_timedelta_to_mmss(elapsed_time)
            duration_str = format_timedelta_to_mmss(duration)
            embed.set_footer(text= f"Duration: {elapsed_str} / {duration_str}")
            await ctx.send(embed=embed)


    

    ## COMANDO DE JOGADORES DE TIMES


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

@bot.tree.command(name='jogadores', description='Mostra os jogadores do Santos!')
async def jogadores_command(interaction: discord.Interaction, time:str):
    await interaction.response.defer()
    jogadores = get_players(time.lower())
    
    if not jogadores:
        await interaction.followup.send(f"⚠️ Time **{time}** não encontrado! Verifique o nome e tente novamente.")
        return  
    
    view = JogadoresView(jogadores)
    embed = view.format_embed()
    
    await interaction.followup.send(embed=embed, view=view)
    
    
    ## COMANDO DE ARTILHEIROS
    
    
class ArtilheirosView(discord.ui.View):
    
    def __init__(self, artilheiros):
        super().__init__(timeout=None)
        self.artilheiros = artilheiros
        self.index = 0
        
    def format_embed(self):
        jogador = self.artilheiros[self.index]
        embed = discord.Embed(title=f"Artilheiro {self.index+1} / {len(self.artilheiros)}", description=f'Aqui está as informações do artilheiro {self.index+1} do SANTOS', color=discord.Color.blue())
        embed.add_field(name="Nome", value=jogador['Nome'], inline=False)
        embed.add_field(name="Jogos", value=jogador['Jogos'], inline=False)
        embed.add_field(name='Gols', value=jogador['Gols'], inline=False)
        embed.set_thumbnail(url="https://s4.ezgif.com/tmp/ezgif-46104ee5597194.png")
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
        
@bot.tree.command(name='artilheiros', description='Mostra os artilheiros do campeonato!')
async def artilheiros_command(interaction: discord.Interaction):
    await interaction.response.defer()
    artilheiros = get_artilheiros()
    if not artilheiros:
        await interaction.followup.send("Não foi possivel obter os dados dos artilheiros.")
        return 

    view = ArtilheirosView(artilheiros)
    embed = view.format_embed()
    
    await interaction.followup.send(embed=embed, view=view)

# Command to see the last games and next games 


@bot.tree.command(name='jogos', description='Mostra os ultimos e os próximos resultados do seu time!')
async def jogos_command(interaction: discord.Interaction, time: str):
        await interaction.response.defer()
        
        jogos_data = get_jogos(time)
        jogadores = get_players(time)
        jogadores = jogadores 
        index = 0
        
        jogador = jogadores[index]
        embed =  discord.Embed(title=f'⚔️ Tabela de jogos do {time.capitalize()} ⚔️', description='')
        
        for row in  jogos_data:
            embed.add_field(
                name=f'{row['TeamHome']} {row['Result']} {row['AwayTeam']}',
                value=f'{row['Data']}',
                inline=False
            )
        embed.set_thumbnail(url=f"{jogador['Escudo']}")
        await interaction.followup.send(embed=embed)

# Class made to set the embed and buttons to the Transfers Lists.

class TransfersView(discord.ui.View):
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

    
# Slash command to see your team transfers
    
    
@bot.tree.command(name='transferencias', description='Mostra as ultimas transferências do seu time!')
async def transfers_command(interaction: discord.Interaction, time:str):
    await interaction.response.defer()
    transferencias, escudo = get_transfers(time.lower())
    if transferencias is None:
        await interaction.followup.send(f"⚠️ Time **{time}** não encontrado! Verifique o nome e tente novamente.")
        return 
    if not transferencias:
        await interaction.followup.send("Não foi possível obter os dados das transferências!")
        return  
    view = TransfersView(transferencias, escudo)
    embed = view.format_embed()
    
    await interaction.followup.send(embed=embed, view=view)

# Command to add filme on the list

@bot.tree.command(description='Adicionar filmes a lista!')
async def addmovie(interact:discord.Interaction, filme: str, nota1:float, nota2:float):
    if interact.guild.id != allowed_guild_id:
        await interact.response.send_message("Este comando não está disponível neste servidor.", ephemeral=True)
        return
    
    member = interact.user
    user_filme = filme
    user_nota1 = nota1 
    user_nota2 = nota2
    save_dates(member, user_filme, user_nota1, user_nota2)
    await interact.response.send_message(f'{filme}, adicionado com sucesso!')

# Command to delete movies

@bot.tree.command(description='Delete o filme da lista!')
async def delmovie(interact:discord.Interaction, movie_id: int):
    if interact.guild.id != allowed_guild_id:
        await interact.response.send_message("Este comando não está disponível neste servidor.", ephemeral=True)
        return
    
    delete_dates(movie_id)
    await interact.response.send_message(f'Filme com ID {movie_id} deletado')


# Class made to set the buttons and embed to the movies.


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
        embed.set_image(url=url)
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
        
        
@bot.tree.command(description='Liste os filmes da lista!')
async def listmovies(interaction:discord.Interaction):
    conn = sqlite3.connect("//app/data/database.sqlite")
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
    embed = view.format_embed()
    await interaction.response.send_message(embed=embed, view=view)
    
    



bot.run(TOKEN) 
