from django.conf import settings
from tema.models import parametros_imagenes

def get_imagen_url(nombre):
    try:
        host = settings.CSRF_TRUSTED_ORIGINS[0]
        imagen_parametro = parametros_imagenes.objects.get(title=nombre)  
        return f"{host}{imagen_parametro.image.url}"
    except parametros_imagenes.DoesNotExist:
        return None