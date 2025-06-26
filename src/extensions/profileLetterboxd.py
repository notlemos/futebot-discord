import discord
from discord.ext import commands
from scraping.letterboxd import getFavs, getIdMovie, getProfile
from api.tmdbAPI import fetch_data
from utils.pillowImgs import fade, cropImg
import aiohttp
import asyncio
import sqlite3
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
conn = sqlite3.connect("src/data/users.db")
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS users(
            discordId TEXT PRIMARY KEY,
            letterboxdUser TEXT NOT NULL
    )
''')
HTML_HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

class LetterboxdPillow(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(name="profile")
    async def profile(self, ctx, *, user: str = None):
        discordId = str(ctx.author.id)
        
        if user:
            c.execute('REPLACE INTO users (discordId, letterboxdUser) VALUES (?, ?)', (discordId, user))
            conn.commit()
            savedUser = user
        else:
            c.execute('SELECT letterboxdUser FROM users WHERE discordId = ?', (discordId,))
            result = c.fetchone()
            if result:
                savedUser = result[0]
            else:
                await ctx.send("Use o comando uma vez com seu user para salvar.")
                return
        font = ImageFont.truetype('fonts/Poppins-SemiBold.ttf', size=18)
        image = Image.open('imgs/letterboxd.png').convert('RGBA')
        draw = ImageDraw.Draw(image)


        async with aiohttp.ClientSession() as session:
            profilePic, profileName = await getProfile(session, savedUser)
            datas = getFavs(savedUser)
            first_fav = datas[0]
            
            backdrop_img = await handle_movie_backdrop(session, first_fav['target'])
            
            backdrop_cropped = cropImg(backdrop_img)
            fade_backdrop = fade(backdrop_cropped).convert('RGBA')
                
            
            image.paste(fade_backdrop, (0, 0), fade_backdrop)
                
            
            center_x = 130

            bbox = draw.textbbox((0,0), profileName, font=font)
            text_width = bbox[2] - bbox[0]
            x = center_x - text_width // 2
            

            draw.text((x, 50), profileName, fill="#6a7784", font=font)

            
            pp_resp = await session.get(profilePic)
            pp_bytes = await pp_resp.read()
            profPic = Image.open(BytesIO(pp_bytes)).convert('RGBA')
            image.paste(profPic, (30, 77), profPic)

            

            tasks = [handle_movie(session, d['target']) for d in datas]
            posters = await asyncio.gather(*tasks)

            off_set = 30
            for poster_img in posters:
                if poster_img:
                    poster_img = poster_img.resize((290, 433), Image.Resampling.LANCZOS)
                    image.paste(poster_img, (off_set, 391), poster_img)
                    off_set += 308
                    

        temp_path = f"/tmp/profile_card{discordId}"
        image.save(temp_path, format="PNG")
        file = discord.File(temp_path, filename="profile_card.png")
        await ctx.send(file=file)
        os.remove(temp_path)

async def handle_movie(session, letterboxd_link):
    id, media_type = await getIdMovie(session, letterboxd_link)
    if not id:
        return None 
    
    poster_path, _ = await fetch_data(session, id, media_type)
    if not poster_path:
        return None 
    
    url = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2{poster_path}"
    async with session.get(url) as resp:
        if resp.status != 200:
            return None 
        img_data = await resp.read()
        return Image.open(BytesIO(img_data)).convert('RGBA')
async def handle_movie_backdrop(session, letterboxd_link):
    id, media_type = await getIdMovie(session, letterboxd_link)
    if not id:
        return None
    
    _, backdrop_path = await fetch_data(session, id, media_type)
    
    if not backdrop_path:
        return None
    
    url_backdrop = f"https://image.tmdb.org/t/p/w1280{backdrop_path}"
    async with session.get(url_backdrop) as resp:
        if resp.status != 200:
            
            return None
        img_data = await resp.read()
        return Image.open(BytesIO(img_data)).convert('RGBA')


async def setup(bot):
     await bot.add_cog(LetterboxdPillow(bot))