from PIL import Image, ImageDraw

def draw_rounded_field_with_alpha(base_image, position, size, radius, fill_color):
    """
    Desenha um campo arredondado com cor RGBA (transparente), colando por cima da imagem principal.
    """
    x, y = position
    width, height = size

    # Criar camada transparente
    layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_layer = ImageDraw.Draw(layer)

    # Desenhar o campo com cor RGBA (suporta transparência)
    draw_layer.rounded_rectangle(
        [(0, 0), (width, height)],
        radius=radius,
        fill=fill_color,
        
    )

    # Colar essa camada na imagem principal
    base_image.paste(layer, (x, y), layer)