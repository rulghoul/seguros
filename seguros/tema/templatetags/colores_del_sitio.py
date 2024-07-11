from django import template
from tema.models import parametros_colores, parametros_imagenes
import base64
import magic

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
        return "#AABBBCC"
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
    try:
        momo = parametros_imagenes.objects.filter(title=nombre).first()    
        return momo.image.url
    except parametros_imagenes.DoesNotExist:    
        return f"No se encontro la imagen con el titulo {nombre}"

@register.simple_tag
def get_imagen_base64(nombre):
    try:
        momo = parametros_imagenes.objects.get(title=nombre)
        contenido = momo.image.file.read()
        
        # Obtener el tipo MIME del contenido
        mime = magic.Magic(mime=True)
        content_type = mime.from_buffer(contenido)
        
        # Codificar el contenido a base64
        encoded_string = base64.b64encode(contenido).decode('utf-8')
        return f"data:{content_type};base64,{encoded_string}"
    except parametros_imagenes.DoesNotExist:
        return f"No se encontró la imagen con el título {nombre}"
    except Exception as e:
        return f"Error al convertir la imagen: {e}"
    
@register.simple_tag
def get_full_name(user):
    if user.is_authenticated:
        return f"{user.first_name} {user.last_name}"
    return ""