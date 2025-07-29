from PIL import Image, ImageDraw, ImageFont
from utils.db import DBFute, DBTabela
from utils.formatters import ShortCuts


def pillow(user):
            db = DBFute()
            db_tabela = DBTabela()
            try:
                jogos = db.get_jogo_by_rodada(db_tabela.get_rodada(user)[0])
            except:
                jogos = db.get_jogo_by_rodada(db_tabela.get_rodada('TODOS')[0])

            image = Image.open('imgs/rodada.png').convert("RGBA")
            draw = ImageDraw.Draw(image)
            font = ImageFont.truetype('fonts/BebasNeue-Regular.otf', size=40)

            x1, y1, off1 = 150, 205, 0
            x2, y2, off2 = 260, 205, 0
            x3, y3, off3 = 550, 205, 0
            x4, y4, off4 = 660, 205, 0

            # coluna 1 
            pos_x, pos_y = 60, 180
            pos_xx, pos_yy = 320, 180

            # coluna 2: desloca +400px em X
            offset_col = 400
            pos_x2, pos_y2   = pos_x  + offset_col, pos_y
            pos_xx2, pos_yy2 = pos_xx + offset_col, pos_yy

            for jogo in range(10):
                partida = ShortCuts(jogos[jogo])
                mandante_path = f"imgs/shields/{partida.mandante()}"
                visitante_path = f"imgs/shields/{partida.visitante()}"

                
                if jogo <= 4:
                    draw.text((x1, y1 + off1), partida.siglaMandante(), fill="white", font=font)
                    draw.text((x2, y2 + off2), partida.siglaVisitante(), fill="white", font=font)

                    
                    mandante_img = Image.open(mandante_path).convert("RGBA")
                    mandante_img = mandante_img.resize((80, 80), Image.LANCZOS)
                    visitante_img = Image.open(visitante_path).convert("RGBA")
                    visitante_img = visitante_img.resize((80, 80), Image.LANCZOS)

                    image.paste(mandante_img, (pos_x,   pos_y),   mandante_img)
                    image.paste(visitante_img, (pos_xx, pos_yy), visitante_img)

                    off1 += 120; off2 += 120

                    
                    if jogo == 1:
                        pos_y   += 115; pos_yy   += 115
                    else:
                        pos_y   += 125; pos_yy   += 125

                else:
                    draw.text((x3, y3 + off3), partida.siglaMandante(), fill="white", font=font)
                    draw.text((x4, y4 + off4), partida.siglaVisitante(), fill="white", font=font)

                    # coluna 2: redimensiona e cola do mesmo jeito
                    mandante_img = Image.open(mandante_path).convert("RGBA")
                    mandante_img = mandante_img.resize((80, 80), Image.LANCZOS)
                    visitante_img = Image.open(visitante_path).convert("RGBA")
                    visitante_img = visitante_img.resize((80, 80), Image.LANCZOS)

                    image.paste(mandante_img, (pos_x2,   pos_y2),   mandante_img)
                    image.paste(visitante_img, (pos_xx2, pos_yy2), visitante_img)

                    off3 += 120; off4 += 120

                    # avança verticalmente igual à primeira coluna
                    if jogo == 6:   # espelha o “jogo==1” da primeira coluna
                        pos_y2   += 115; pos_yy2   += 115
                    else:
                        pos_y2   += 125; pos_yy2   += 125

            image.save("/tmp/tabela.png")
            return "/tmp/tabela.png"

def pillowTabela(user):
    image = Image.open('imgs/tabelabg.png')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('fonts/BebasNeue-Regular.otf', size=32)
    fontPts = ImageFont.truetype('fonts/BebasNeue-Regular.otf', size=48)
    all_data = DBTabela().get_tabela(user)
    times = []
    pontos = []
    for i in all_data:
          times.append(i['name'])
          pontos.append(i['pontos'])   
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

    image.save("/tmp/tabela.png")
    return "/tmp/tabela.png"
def cropImg(img):
    target_w, target_h = 1279, 325

    
    target_ratio = target_w / target_h

    
    original_w, original_h = img.size
    original_ratio = original_w / original_h

    
    if original_ratio > target_ratio:
        # Imagem é mais larga → redimensiona pela altura
        new_h = target_h
        new_w = int(new_h * original_ratio)
    else:
        # Imagem é mais alta → redimensiona pela largura
        new_w = target_w
        new_h = int(new_w / original_ratio)

    
    resized = img.resize((new_w, new_h), Image.LANCZOS)

    # Cálculo para crop central
    left = (new_w - target_w) // 2

    vertical_offset = -80
    top = ((new_h - target_h) // 2) + vertical_offset

    top = max(0, top)
    
    
    bottom = top + target_h 

    # Faz o recorte central
    final = resized.crop((left, top, left+target_w, bottom))

    
    
    return final

def fade(img):
    
    
    largura, altura = img.size
    fade_mask = Image.new("L", (largura, altura), color=0)  # centro totalmente visível
    draw = ImageDraw.Draw(fade_mask)

  
    grad_height = 900
   
    
    # --- FADE BASE ---
    for y in range(altura - grad_height, altura):
        alpha = int(255 * ((altura - y) / grad_height))  # 255 → 0
        draw.line([(0, y), (largura+100, y)], fill=alpha)
   
    recorte_com_fade = Image.composite(img, Image.new("RGBA", img.size, (32, 40, 48, 255)), fade_mask)
    resultado_final = Image.composite(img, recorte_com_fade, fade_mask)
    return resultado_final
