import discord
from discord.ext import commands
from discord import app_commands 
from src.api.aiAPI import geminiResume, groqMovie
import datetime 
import re
import google.genai as genai


class ResumeSubs(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.user_subtitles = {}
    def filterSubtitle(self, subtitle, startTime, minutes):
    
        now = datetime.datetime.now() 
        elapsedSeconds = (now - startTime).total_seconds() 
        
        if elapsedSeconds < 0: 
            return 
        
        start = elapsedSeconds - (minutes * 60) 
        end = elapsedSeconds 
        
        pattern = re.compile(r'(\d{2}):(\d{2}):(\d{2}),\d{3}') 
        lines = subtitle.split('\n') 
       
        subtitleClean = [] 
        currentTimeSec = 0 
        
        for line in lines: 
            timestamp = pattern.search(line) 
            if timestamp: 
                h, m, s = map(int, timestamp.groups()) 
                currentTimeSec = h * 3600 + m * 60 + s 
                
            elif start <= currentTimeSec <= end: 
                if not line.strip().isdigit() and "-->" not in line and line.strip(): 
                    subtitleClean.append(line.strip()) 
                    
        return " ".join(subtitleClean)
    
    
    @commands.command(name="sub", description="Upload a subtitle")
    async def upload(self, ctx, arquivo: discord.Attachment):
        if not arquivo:
            await ctx.response.send_message("Please upload a .srt file", ephemeral=True)
            return
        if not arquivo.filename.endswith('.srt'):
            await ctx.response.send_message("Please upload a .srt file", ephemeral=True)
        await arquivo.save(f"subs/sub.srt")
        await ctx.send('salvei filho da puta')
        
        
    @app_commands.command(name="resume", description="Upload a subtitle to resume")
    @app_commands.describe(inicio="time the movie started (20:30)", minutos="minutes to summarize the movie")
    async def resume(self, interaction: discord.Interaction, inicio: str, minutos: int):
        await interaction.response.defer()
        
        start = datetime.datetime.strptime(inicio, "%H:%M").replace(
            year=datetime.datetime.now().year,
            month=datetime.datetime.now().month,
            day=datetime.datetime.now().day
        )
        arquivo = "subs/sub.srt"
        try:
            with open(arquivo, "r", encoding="utf-8", errors="ignore") as f:
                rawText = f.read()
            
            subtitleClean = self.filterSubtitle(rawText, start, minutos)
            print(subtitleClean)
            
            summary =  groqMovie(subtitleClean)
            await interaction.followup.send(summary)
        except Exception as e:
            await interaction.followup.send(f"An error occurred: {e}")
        
        
        
    
async def setup(bot):
    await bot.add_cog(ResumeSubs(bot))