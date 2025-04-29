import discord
from discord.ext import commands
from discord.activity import Spotify
import logging
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from io import BytesIO
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
                mask = Image.new("L", capa.size, 0)
                draw = ImageDraw.Draw(mask)

                # Criar uma borda arredondada com transição suave
                radius = 15
                draw.rounded_rectangle((0, 0, 378,378), radius=radius, fill=255)

                
                capa_arredondada = Image.new("RGBA", capa.size)
                capa_arredondada.paste(capa, (0, 0), mask)

                # Agora, aplique uma suavização à própria imagem para suavizar as bordas mais visíveis (caso necessário)
                capa_arredondada = capa_arredondada.filter(ImageFilter.SMOOTH_MORE)

                # Colocar a máscara na imagem arredondada
                capa_arredondada.putalpha(mask)

                # Colar a imagem arredondada na imagem final
                
                
                    
                # Fontes Escritas do spotify
                font_nome_user = ImageFont.truetype("fonts/BebasNeue-Regular.otf", 42)
                font_main = ImageFont.truetype("fonts/BebasNeue-Regular.otf", 48)
                font_menor = ImageFont.truetype("fonts/Roboto-Regular.ttf", 28)
                font_tempo = ImageFont.truetype("fonts/BebasNeue-Regular.otf", 36)
                # Campos de escrita.
                
                user_name = ImageDraw.Draw(image)
                music_name = ImageDraw.Draw(image)
                album_name = ImageDraw.Draw(image)
                artists_name = ImageDraw.Draw(image)
                
                
                
                tempo = ImageDraw.Draw(image)
                # Campo do nome
                
                user_name.text((492,352), f"{user.name}'s spotify", font=font_nome_user, fill=(250,250,250))
                
               
                music_name.text((88, 520), "Music", font=font_main, fill=(250,250,250))
                music_name.text((94, 590), activity.title, font=font_menor, fill=(250,250,250))

                album_name.text((88, 660), "Album", font=font_main, fill=(250,250,250))
                album_name.text((94, 730), activity.album, font=font_menor, fill=(250,250,250))

                artists_name.text((88, 800), "Artists", font=font_main, fill=(250,250,250))
                artists_name.text((94, 870), activity.artist, font=font_menor, fill=(250,250,250))
                                                
                
                

                # Colar a capa sobre o fundo
                duration = activity.duration  # duração total (tipo timedelta)
                start_time = activity.start  # datetime do início
                
                elapsed_time = discord.utils.utcnow() - start_time
                
                elapsed_str = format_timedelta(elapsed_time)
                duration_str = format_timedelta(duration)
                
                tempo.text((678, 230), f"  {elapsed_str} / {duration_str}", font=font_tempo, fill=(250,250,250,250))
                
                image.paste(capa_arredondada, (pos_x, pos_y), capa_arredondada)

                image.save("spotify_card.png", format="png", optimize=True)
                file = discord.File("spotify_card.png", filename="spotify_card.png")
                await ctx.send(file=file)
                return
        await ctx.send(f"{user.display_name} não está ouvindo Spotify no momento.")
async def setup(bot): 
    await bot.add_cog(SpotifyPillow(bot))