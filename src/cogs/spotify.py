import discord
from discord.ext import commands
from discord.activity import Spotify
import logging
import requests
from PIL import Image, ImageDraw, ImageFont
from src.utils.rounded_field import draw_rounded_field_with_alpha
from io import BytesIO
logger = logging.getLogger(__name__)



class SpotifyPillow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="spotify")
    async def spotify(self, ctx, user: discord.Member = None):
        user = user or ctx.author 
        image = Image.open('backgrounds/spotifybg3.png').convert("RGBA")
        

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
                capa = Image.open(BytesIO(response.content)).resize((180,180)).convert("RGBA")
                radius = 20
                pos_x, pos_y = 600, 20


            

                # Arredondar a capa
                mask = Image.new("L", capa.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.rounded_rectangle((0, 0, 180, 180), radius=radius, fill=255)
                capa_arredondada = Image.new("RGBA", capa.size)
                capa_arredondada.paste(capa, (0, 0), mask)
                
                
                    
                # Fontes Escritas do spotify
                font_nome_user = ImageFont.truetype("fonts/Roboto-Regular.ttf", 30)
                font_main = ImageFont.truetype("fonts/Roboto-Regular.ttf", 23)
                font_menor = ImageFont.truetype("fonts/Roboto-Regular.ttf", 18)
                font_tempo = ImageFont.truetype("fonts/Roboto-Regular.ttf", 14)
                # Campos de escrita.
                
                user_name = ImageDraw.Draw(image)
                music_name = ImageDraw.Draw(image)
                album_name = ImageDraw.Draw(image)
                artists_name = ImageDraw.Draw(image)
                
                rights = ImageDraw.Draw(image)
                
                tempo = ImageDraw.Draw(image)
                # Campo do nome
                draw_rounded_field_with_alpha(image,position=(50, 20),size=(500, 50),radius=10,fill_color=(255, 255, 255, 20) ) # Transparente! 
                user_name.text((80,25), f"{user.name}'s spotify", font=font_nome_user, fill=(250,250,250,250))
                
                draw_rounded_field_with_alpha(image,position=(30, 90),size=(520, 190),radius=10,fill_color=(255, 255, 255,20) ) # Transparente! 
                music_name.text((60, 100), f"Music", font=font_main, fill=(250,250,250,250))
                music_name.text((63, 130), f"{activity.title}", font=font_menor, fill=(250,250,250,250))
                
                album_name.text((60,160), "Album", font=font_main, fill=(250,250,250,250))
                album_name.text((63, 190), f"{activity.album}", font=font_menor, fill=(250,250,250,250))
                
                artists_name.text((60,220), "Artists", font=font_main, fill=(250,250,250,250))
                artists_name.text((63, 250), f"{activity.artist}", font=font_menor, fill=(250,250,250,250))
                
                rights.text((490, 73), f"notlemos", font=font_tempo, fill=(255, 255, 255, 100))
                
                

                # Colar a capa sobre o fundo
                duration = activity.duration  # duração total (tipo timedelta)
                start_time = activity.start  # datetime do início
                
                elapsed_time = discord.utils.utcnow() - start_time
                
                elapsed_str = format_timedelta(elapsed_time)
                duration_str = format_timedelta(duration)
                icon = Image.open("backgrounds/spotify.png").resize((60,60))
                image.paste(icon, (660, 230), icon)
                tempo.text((650, 210), f"  {elapsed_str} / {duration_str}", font=font_tempo, fill=(250,250,250,250))
                
                image.paste(capa_arredondada, (pos_x, pos_y), capa_arredondada)

                image.save("spotify_card.png")
                file = discord.File("spotify_card.png", filename="spotify_card.png")
                await ctx.send(file=file)
                return
        await ctx.send(f"{user.display_name} não está ouvindo Spotify no momento.")
async def setup(bot): 
    await bot.add_cog(SpotifyPillow(bot))