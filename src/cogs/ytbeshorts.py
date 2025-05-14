import discord
from discord.ext import commands
import os 
import yt_dlp 
import random
import logging
import string

logger = logging.getLogger(__name__)

class shortsRandom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
    
    def get_shorts(self,query):

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
            if entry.get("duration") and entry["duration"] <= 60:
                urls.append(entry["url"])
            
        if urls:
            return random.choice(urls)
        return None

    def baixar_video(self, url):
        a =  list(string.ascii_lowercase)
        output_path = '/tmp/shor%st.%%(ext)s' % "".join(random.choices(a, k=4))

        opts = {
            'format': 'bestvideo[ext=mp4][vcodec^=avc1]+bestaudio[ext=m4a]/best[ext=mp4][vcodec^=avc1]',
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
                print(e)

        

    @commands.command(name="shorts")
    async def randomShort(self, ctx, *, tag: str):

        await ctx.message.add_reaction("<:loading:1372046197573025792>")
        

        video_url = self.get_shorts(tag)

        if video_url == None: 
            await ctx.send("Falha ao baixar.")
            await ctx.message.clear_reactions()
            await ctx.message.add_reaction("❌")
            return
        video_path = self.baixar_video(video_url)
        try:
            await ctx.reply(file=discord.File(video_path), mention_author=True)
            await ctx.message.clear_reactions()
            await ctx.message.add_reaction("<:check:1372079293403889704>")
        except Exception as e:
            await ctx.send(e)
        os.remove(video_path)
        return
            
        
            
async def setup(bot):
    await bot.add_cog(shortsRandom(bot))