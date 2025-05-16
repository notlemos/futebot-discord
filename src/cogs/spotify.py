import discord
from discord.ext import commands
from discord.activity import Spotify
import logging
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
logger = logging.getLogger(__name__)



class SpotifyPillow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="spotify")
    async def spotify(self, ctx, user: discord.Member = None):
        user = user or ctx.author 
        image = Image.open('backgrounds/spotifybg.png').convert("RGBA")
        

        for activity in user.activities:
            if isinstance(activity, Spotify):

                
                # Função Para Formatar o Tempo
                def format_timedelta(td):
                    total_seconds = int(td.total_seconds())

                    # Garante que não será negativo
                    if total_seconds < 0:
                        total_seconds = 0

                    minutes = total_seconds // 60
                    seconds = total_seconds % 60 
                    return f"{minutes}:{seconds:02d}"

                # Salvando a capa do Album.
                
                url = activity.album_cover_url
                response = requests.get(url)
                capa = Image.open(BytesIO(response.content)).convert("RGBA")
                capa = capa.resize((378,378), Image.LANCZOS)
                # Posições para colar a imagem
                pos_x, pos_y = 72, 28

                # Criar a máscara com bordas arredondadas
                
                    
                # Fontes Escritas do spotify
                font_nome_user = ImageFont.truetype("fonts/BebasNeue-Regular.otf", 42)
                font_main = ImageFont.truetype("fonts/BebasNeue-Regular.otf", 58)
                font_menor = ImageFont.truetype("fonts/Roboto-Regular.ttf", 34)
                font_tempo = ImageFont.truetype("fonts/BebasNeue-Regular.otf", 36)

                def cut_text(text, font, max_size):
                    original = text
                    while font.getlength(text + "...") > max_size and len(text) > 0:
                        text = text[:-1]
                    if text != original:
                        return text + "..."
                    return text

                # Largura maxima do texto

                max_largura_texto = 900 - 94 

                # Campos de escrita.
                
                user_name = ImageDraw.Draw(image)
                music_name = ImageDraw.Draw(image)
                album_name = ImageDraw.Draw(image)
                artists_name = ImageDraw.Draw(image)
                
                
                
                tempo = ImageDraw.Draw(image)
                
                # Campo do nome
                
                user_name.text((492,352), f"{user.name}'s spotify", font=font_nome_user, fill=(250,250,250))
                
                # Campo da musica
                music_name.text((88, 500), "Music", font=font_main, fill=(250,250,250))
                music_title = cut_text(activity.title, font_menor, max_largura_texto)
                music_name.text((94, 580), music_title, font=font_menor, fill=(250,250,250))

                # Campo do album

                album_name.text((88, 650), "Album", font=font_main, fill=(250,250,250))
                album_title = cut_text(activity.album, font_menor, max_largura_texto)
                album_name.text((94, 730), album_title, font=font_menor, fill=(250,250,250))

                # Campo do artista

                artists_name.text((88, 800), "Artists", font=font_main, fill=(250,250,250))
                artist_title = cut_text(activity.artist, font_menor, max_largura_texto)
                artists_name.text((94, 880), artist_title, font=font_menor, fill=(250,250,250))
                                                
                
                

                # Colar a capa sobre o fundo
                duration = activity.duration  # duração total (tipo timedelta)
                start_time = activity.start  # datetime do início
                elapsed_time = discord.utils.utcnow() - start_time 
                
                elapsed_str = format_timedelta(elapsed_time)
                duration_str = format_timedelta(duration)
                
                tempo.text((678, 230), f"  {elapsed_str} / {duration_str}", font=font_tempo, fill=(250,250,250,250))
                
                image.paste(capa, (pos_x, pos_y), capa)

                image.save("/tmp/spotify_card.png", format="PNG")
                file = discord.File("/tmp/spotify_card.png", filename="spotify_card.png")
                await ctx.send(file=file)
                os.remove("/tmp/spotify_card.png")
                return
        await ctx.send(f"{user.display_name} não está ouvindo Spotify no momento.")
async def setup(bot): 
    await bot.add_cog(SpotifyPillow(bot))