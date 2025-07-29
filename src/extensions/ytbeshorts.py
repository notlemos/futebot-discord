import discord
from discord.ext import commands
from discord import app_commands 
import os 
import yt_dlp 
import random
import logging
import string

logger = logging.getLogger(__name__)

class shortsRandom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    
    def get_random_shorts(self,query):

        query = f"shorts {query}"
        
        opts = {
            'format': 'mp4',
            'noplaylist': True,
            'quiet': True,
            'extract_flat': True,
            'dump_single_json': True,
            'no_cache_dir': True
        }

        urls = []

        with yt_dlp.YoutubeDL(opts) as ydl:
            results = ydl.extract_info(f"ytsearch50:{query}", download=False)

        for entry in results['entries']:
            if entry.get("duration") and entry["duration"] <= 120:
                urls.append(entry["url"])
        if urls:
            return random.choice(urls)
        return None
    
    def get_short(self,query):

        query = f"shorts {query}"
        
        opts = {
            'format': 'mp4',
            'noplaylist': True,
            'quiet': True,
            'extract_flat': True,
            'dump_single_json': True,
            'no_cache_dir': True
        }

        urls = []

        with yt_dlp.YoutubeDL(opts) as ydl:
            results = ydl.extract_info(f"ytsearch1:{query}", download=False)

        for entry in results['entries']:
            if entry.get("duration") and entry["duration"] <= 120:
                urls.append(entry["url"])
        if urls:
            return urls
        return None

    def baixar_video(self, url):
        a =  list(string.ascii_lowercase)
        output_path = '/tmp/shor%st.%%(ext)s' % "".join(random.choices(a, k=4))

        opts = {
            'format': 'bestvideo[ext=mp4][height<=720][vcodec^=avc1]+bestaudio[ext=m4a]/best[ext=mp4][height<=720][vcodec^=avc1]',
            'merge_output_format': 'mp4',
            'outtmpl': output_path,
            'quiet': True,
            'noplaylist': True,
            'no_cache_dir': True
        }

        with yt_dlp.YoutubeDL(opts) as ydl:
            try:
                ydl.download([url])
                info_dict = ydl.extract_info(url, download=False)
                # Garante o caminho final correto
                filename = ydl.prepare_filename(info_dict).rsplit('.', 1)[0] + '.mp4'
                return filename
            except Exception as e:
               return e

        
    msg_id = None
    @commands.command(name="shorts")
    async def randomShort(self, ctx, *, tag: str):

        await ctx.message.add_reaction("<:loading:1372046197573025792>")
        video_url = self.get_random_shorts(tag)


        if video_url == None: 
            await ctx.send("Falha ao baixar.")
            await ctx.message.clear_reactions()
            await ctx.message.add_reaction("❌")
            return
        video_path = self.baixar_video(video_url)

        try:
            
            resposta = await ctx.reply(file=discord.File(video_path), mention_author=True)
            await ctx.message.clear_reactions()
            await ctx.message.add_reaction("<:check:1372079293403889704>")
            await resposta.add_reaction("<:youtubeplay:1372638557650292797>")
            
            await self.bot.wait_for(
                "reaction_add",
                timeout=60.0,
                check=lambda r, u: (
                    u != ctx.bot.user and
                    r.message.id == resposta.id and
                    hasattr(r.emoji, 'id') and 
                    r.emoji.id == 1372638557650292797
                )
            )
            await ctx.reply(f"<{video_url}>", mention_author=False)
    
        except Exception as e:
            return e
        finally:
            os.remove(video_path)
      
            return
    
    @app_commands.command(name="short", description="Retorna um shorts do youtube unico, não aleatório.")
    async def short(self, interaction: discord.Interaction, tag: str):
        await interaction.response.defer()
        video_url = self.get_random_shorts(tag)

        if video_url == None:
            await interaction.followup.send("Falha ao baixar.")
        video_path = self.baixar_video(video_url)
        try:
            await interaction.followup.send(file=discord.File(video_path))
        except Exception as e:
            return e
        os.remove(video_path)
        return
async def setup(bot):
    await bot.add_cog(shortsRandom(bot))
    