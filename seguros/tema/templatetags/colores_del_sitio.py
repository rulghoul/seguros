from django import template
from tema.models import parametros_colores, parametros_imagenes

register = template.Library()

def hex_to_rgb(hex_color):
    """Convierte un color hexadecimal en una tupla RGB."""
    hex_color = hex_color.lstrip('#')
    hlen = len(hex_color)
    return tuple(int(hex_color[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))

@register.simple_tag
def get_color(nombre):
    color_resultado = parametros_colores.objects.filter(elemento=nombre).first()
    if not color_resultado:
        return "#AABVBCC"
    else:
        return color_resultado.color

@register.simple_tag
def get_rgba(nombre, alpha=1):
    """Convierte un color hexadecimal recuperado a su equivalente RGBA."""
    hex_color = get_color(nombre)
    rgb_color = hex_to_rgb(hex_color)
    return "rgba({}, {}, {}, {})".format(*rgb_color, alpha)

@register.simple_tag
def get_imagen(nombre):
    momo = parametros_imagenes.objects.filter(title=nombre).first()
    if not momo:
        return f"No se encontro la imagen con el titulo {nombre}"
    else:
        return momo.image.url