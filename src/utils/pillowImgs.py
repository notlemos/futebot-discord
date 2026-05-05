from PIL import Image, ImageDraw, ImageFont
from utils.formatters import ShortCuts





def cropImg(img):
    target_w, target_h = 1279, 418

    
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

  
    grad_height = 1500
   
    
    # --- FADE BASE ---
    for y in range(altura - grad_height, altura):
        alpha = int(255 * ((altura - y) / grad_height))  # 255 → 0
        draw.line([(0, y), (largura+100, y)], fill=alpha)
   
    recorte_com_fade = Image.composite(img, Image.new("RGBA", img.size, (20, 24, 29, 255)), fade_mask)
    resultado_final = Image.composite(img, recorte_com_fade, fade_mask)
    return resultado_final
