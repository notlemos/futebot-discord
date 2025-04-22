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
        image = Image.open('backgrounds/background3.png')

        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype('fonts/Roboto_Condensed-Bold.ttf', size=56)
        time, ponto = get_tabela()

        color = (255,255,255) 
        
        color2 = (0, 22, 190)
        color3 = (0,14,40)

        corG4 = (52,230,83)
        corG6 = (250,123,23)
        corZ4 = (234,67,53)
        corResto = (0,5,100)
        
        
        position = list(range(1, 21))

        y_off_set = 65
        texto_cabecalho = "   Posição                  Times                    Pontos"
        draw.text((200, 280), texto_cabecalho, fill=color, font=font)

        largura_img, altura_img = image.size


        largura_tabela = 1000
        margem_esquerda = (largura_img - largura_tabela) // 2

        pos1 = (margem_esquerda + 220, 370)   # Times
        pos2 = (margem_esquerda + 895, 370)   # Pontos
        pos3 = (margem_esquerda + 70, 370)   # Posição

        linha1_x = margem_esquerda
        linha2_x = margem_esquerda + 820
        linha3_x = margem_esquerda + 1000

        for i, (t, p, pos) in enumerate(zip(time, ponto, position)):
            y = pos1[1] + i * y_off_set
            linha_y = y + 35
            draw.line((margem_esquerda, linha_y, margem_esquerda + largura_tabela, linha_y), fill=color2, width=60)
            
            if pos <= 4:
                draw.line((margem_esquerda, linha_y, margem_esquerda + largura_tabela, linha_y), fill=color2, width=60)
                draw.line((margem_esquerda + 200, linha_y , margem_esquerda, linha_y), fill=corG4, width=60)
                draw.line((margem_esquerda, linha_y + 35, margem_esquerda + largura_tabela, linha_y + 35), fill=color3, width=20)
            
            elif pos >= 5 and pos <= 12:
                draw.line((margem_esquerda, linha_y, margem_esquerda + largura_tabela, linha_y), fill=color2, width=60)
                draw.line((margem_esquerda + 200, linha_y , margem_esquerda, linha_y), fill=corG6, width=60)
                draw.line((margem_esquerda, linha_y + 35, margem_esquerda + largura_tabela, linha_y + 35), fill=color3, width=20)
            
            elif pos > 16:
                draw.line((margem_esquerda, linha_y, margem_esquerda + largura_tabela, linha_y), fill=color2, width=60)
                draw.line((margem_esquerda + 200, linha_y , margem_esquerda, linha_y), fill=corZ4, width=60)
                draw.line((margem_esquerda, linha_y + 35, margem_esquerda + largura_tabela, linha_y + 35), fill=color3, width=20)
            
            else:
                draw.line((margem_esquerda, linha_y, margem_esquerda + largura_tabela, linha_y), fill=color2, width=60)
                draw.line((margem_esquerda + 200, linha_y , margem_esquerda, linha_y), fill=corResto, width=60)
                draw.line((margem_esquerda, linha_y + 35, margem_esquerda + largura_tabela, linha_y + 35), fill=color3, width=20)
            
            draw.text((pos1[0], y), t, fill=color, font=font)
            draw.text((pos2[0]-10, y), f"{p:02d}", fill=color, font=font)
            draw.text((pos3[0], y), f"{pos:02d}", fill=color, font=font)
            
            

        # Linhas verticais centralizadas
        draw.line((linha1_x, 366, linha1_x, 25.90 * y_off_set), fill=color3, width=20)
        draw.line((linha2_x, 366, linha2_x, 25.90* y_off_set), fill=color3, width=20) # Direita Pontos
        draw.line((linha3_x, 366, linha3_x, 25.90 * y_off_set), fill=color3, width=20) 

        # Linha entre "Posição" e "Times" 

        draw.line((linha1_x+190, 366, linha1_x+190, 25.90 * y_off_set), fill=color3, width=20)


        # Linhas horizontais e rodapé

        draw.line((211, linha_y+35, 1230, linha_y+35), fill=color3, width=20)
        draw.line((211, 360, 1230, 360), fill=color3, width=20)

            

        image.save("tabela.png")
            
        
        file = discord.File("tabela.png", filename="tabela.png")
        
        await ctx.send(file=file)
async def setup(bot):
    await bot.add_cog(TabelaView(bot))