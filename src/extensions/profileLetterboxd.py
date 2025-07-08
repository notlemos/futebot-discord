import discord
from discord.ext import commands
from scraping.letterboxd import getFavs, getIdMovie, getProfile, getLastFourWatched
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
        font = ImageFont.truetype('fonts/Poppins-SemiBold.ttf', size=26)
        image = Image.open('imgs/profile_card_letterboxd.png').convert('RGBA')
        draw = ImageDraw.Draw(image)


        async with aiohttp.ClientSession() as session:
            profilePic, profileName, statusAccount = await getProfile(session, savedUser)
            datas = getFavs(savedUser)
            first_fav = datas[0]
            
            backdrop_img = await handle_movie_backdrop(session, first_fav['target'])
            
            backdrop_cropped = cropImg(backdrop_img)
            fade_backdrop = fade(backdrop_cropped).convert('RGBA')
                
            
            image.paste(fade_backdrop, (0, 0), fade_backdrop)
                

            draw.text((220, 270), profileName, fill="#ffffff", font=font)
            text_bbox = font.getbbox(profileName)
            text_width = text_bbox[2] - text_bbox[0]
            text_end_x = 220 + text_width
            
            pp_resp = await session.get(profilePic)
            pp_bytes = await pp_resp.read()
            profPic = Image.open(BytesIO(pp_bytes)).convert('RGBA')
            
            if statusAccount == 'Patron':
                patron = Image.open('imgs/patron_letterboxd.png')
                patron = patron.resize((67, 23), Image.Resampling.LANCZOS)
                image.paste(patron, (int(text_end_x + 5), 281), patron)
                
            
            mask = Image.new("L", profPic.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, profPic.size[0], profPic.size[1]), fill=255)
            profPic = profPic.convert("RGBA")
            circular_img = Image.composite(profPic, Image.new("RGBA", profPic.size, (0, 0, 0, 0)), mask)
            
                    
            image.paste(circular_img, (30, 77),circular_img)

            

            tasks = [handle_movie(session, d['target']) for d in datas]
            posters = await asyncio.gather(*tasks)

            off_set = 30
            for poster_img in posters:
                if poster_img:
                    poster_img = poster_img.resize((290, 433), Image.Resampling.LANCZOS)
                    image.paste(poster_img, (off_set, 408), poster_img)
                    off_set += 308
                    

        temp_path = f"/tmp/profile_card{discordId}"
        image.save(temp_path, format="PNG")
        file = discord.File(temp_path, filename="profile_card.png")
        await ctx.send(file=file)
        os.remove(temp_path)

        
    @commands.command(name='last4')
    async def last4watched(self, ctx, *, user: str = None):
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
        font = ImageFont.truetype('fonts/Poppins-SemiBold.ttf', size=26)
        image = Image.open('imgs/last_four_watched_letterboxd.png').convert('RGBA')
        draw = ImageDraw.Draw(image)


        

        async with aiohttp.ClientSession() as session:
            profilePic, profileName, statusAccount = await getProfile(session, savedUser)
            datas = getLastFourWatched(savedUser)
            first_fav = datas[0]
            
            backdrop_img = await handle_movie_backdrop(session, first_fav['target'])
            
            backdrop_cropped = cropImg(backdrop_img)
            fade_backdrop = fade(backdrop_cropped).convert('RGBA')
                
            
            image.paste(fade_backdrop, (0, 0), fade_backdrop)
                
            
            draw.text((220, 270), profileName, fill="#ffffff", font=font)
            text_bbox = font.getbbox(profileName)
            text_width = text_bbox[2] - text_bbox[0]
            text_end_x = 220 + text_width
            
            pp_resp = await session.get(profilePic)
            pp_bytes = await pp_resp.read()
            profPic = Image.open(BytesIO(pp_bytes)).convert('RGBA')
            
            if statusAccount != None:
                patron = Image.open('imgs/patron_letterboxd.png')
                patron = patron.resize((67, 23), Image.Resampling.LANCZOS)
                image.paste(patron, (int(text_end_x + 5), 281), patron)
            
            
            mask = Image.new("L", profPic.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0, profPic.size[0], profPic.size[1]), fill=255)
            profPic = profPic.convert("RGBA")
            circular_img = Image.composite(profPic, Image.new("RGBA", profPic.size, (0, 0, 0, 0)), mask)
            
                    
            image.paste(circular_img, (30, 77),circular_img)

            

            tasks = [handle_movie(session, d['target']) for d in datas]
            posters = await asyncio.gather(*tasks)

            off_set = 30
            for poster_img in posters:
                if poster_img:
                    poster_img = poster_img.resize((290, 433), Image.Resampling.LANCZOS)
                    image.paste(poster_img, (off_set, 408), poster_img)
                    off_set += 308
                    

        temp_path = f"/tmp/last_four_watched{discordId}"
        image.save(temp_path, format="PNG")
        file = discord.File(temp_path, filename="last_four_watched.png")
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