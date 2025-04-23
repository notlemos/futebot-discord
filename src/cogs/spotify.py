import discord
from discord.ext import commands
from discord.activity import Spotify
import logging

logger = logging.getLogger(__name__)

class SpotifyView(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        
    @commands.command(name="spotify")
    async def spotify(self, ctx, user: discord.Member = None):
        
        
        def format_timedelta(td):
            total_seconds = int(td.total_seconds())
            minutes = total_seconds // 60
            seconds = total_seconds % 60 
            return f"{minutes}:{seconds:02d}"
        user = user or ctx.author 
        
        
        for activity in user.activities:
            logger.info(f"Name: {getattr(activity, 'name', None)}, Title: {getattr(activity, 'title', None)}")
            if isinstance(activity, Spotify):
                embed = discord.Embed(
                title=f"{user.display_name}'s spotify",
                description=f"",
                color= discord.Color.blue()
                    )
                embed.set_thumbnail(url=activity.album_cover_url)
                embed.add_field(
                    name=f'Music   ',
                    value=f'{activity.title}',
                    inline=True
                )
                embed.add_field(
                    name=f'Artist   ',
                    value=f'{activity.artist}',
                    inline=True
                )
                embed.add_field(
                    name=f'Album   ',
                    value=f'{activity.album}',
                    inline=True
                )
                duration = activity.duration  # duração total (tipo timedelta)
                start_time = activity.start  # datetime do início
                elapsed_time = discord.utils.utcnow() - start_time

                # Formata para MM:SS
                elapsed_str = format_timedelta(elapsed_time)
                duration_str = format_timedelta(duration)
                embed.set_footer(text= f"Duration: {elapsed_str} / {duration_str}")
                await ctx.send(embed=embed)
                return
        await ctx.send(f"{user.display_name} não está ouvindo Spotify no momento.")
        
async def setup(bot):
    await bot.add_cog(SpotifyView(bot))