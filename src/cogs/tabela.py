import discord 
from discord.ext import commands 
from src.scraping.get_fute import get_tabela
from PIL import Image, ImageDraw, ImageFont
import logging
logger = logging.getLogger(__name__)

class TabelaView(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot 
    
    @commands.command(name="tabela")
    async def tabela(self, ctx):
        image = Image.open('backgrounds/tabelabg.png')

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('fonts/BebasNeue-Regular.otf', size=32)
        fontPts = ImageFont.truetype('fonts/BebasNeue-Regular.otf', size=48)

        times, pontos = get_tabela()

        
        # Coordenadas e offsets
        # Parte 1 da tabela
        x1, y1, off1 = 115, 261, 0
        x2, y2, off2 = 350, 251, 0

        # Parte 2 da tabela

        x3, y3, off3 = 530, 261, 0
        x4, y4, off4 = 765, 251, 0


        for i, (time, pontos) in enumerate(zip(times, pontos), 1):
            if i <= 10:
                draw.text((x1, y1 + off1), f"{time}", fill="white", font=font)
                draw.text((x2, y2 + off2), f"{pontos:02d}", fill="white", font=fontPts)
                off1 += 50
                off2 += 50
            else:
                draw.text((x3, y3 + off3), f"{time}", fill="white", font=font)
                draw.text((x4, y4 + off4), f"{pontos:02d}", fill="white", font=fontPts)
                off3 += 50
                off4 += 50
            
        image.save("tabela.png")

                    

                
                    
                
        file = discord.File("tabela.png", filename="tabela.png")
                
        await ctx.send(file=file)
async def setup(bot):
    await bot.add_cog(TabelaView(bot))