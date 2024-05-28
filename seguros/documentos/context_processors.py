from .models import Asesor

def asesor_status(request):
    if request.user.is_authenticated:
        return {'es_asesor': Asesor.objects.filter(usuario=request.user).exists()}
    return {'es_asesor': False}

