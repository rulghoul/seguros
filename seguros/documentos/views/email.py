from django.shortcuts import render
from documentos.models import Poliza, PersonaPrincipal, AsesorEmpresa
from django.shortcuts import get_object_or_404, render
from documentos.utils.send_recordatorio_pago import envia_recordatorio
from django.contrib import messages 
from tema.models import parametros_imagenes

def get_imagen_cdi(nombre, request):
    try:
        imagen_parametro = parametros_imagenes.objects.get(title=nombre)   
        messages.info(request, f"La imagen es {imagen_parametro.image}")
        return f"https://{request.get_host()}:{request.get_port()}{imagen_parametro.image.url}"
    except parametros_imagenes.DoesNotExist:
        messages.error(request, f"No se encontro la imagen {nombre}")
        return None

def email_preview_recordatorio(request, pk):
    poliza = get_object_or_404(Poliza, pk=pk)
    cliente = poliza.persona_principal
    asesor_empresa = AsesorEmpresa.objects.get(empresa = poliza.empresa, asesor = poliza.asesor_poliza)
    imagen_url = get_imagen_cdi("agencia", request)
    context = {
        'cliente': cliente,
        'poliza': poliza, 
        'asesor': asesor_empresa,
        'imagen_url': imagen_url,
    }
    
    return render(request, 'email_templates/recordatorio_pago.html', context)

def email_recordatorio(request, pk):
    poliza = get_object_or_404(Poliza, pk=pk) 
    context = {
        "poliza":poliza,
        "cliente": poliza.persona_principal.pk,
        "tilulo": f"Enviar recordatorio para la poliza {poliza}",
    }
    messages.info(request, "No fue el contexto")
    if request.method == "POST":
        try:
            messages.info(request, "Se esta por enviar el correo")
            envia_recordatorio(poliza=poliza, request=request)
            messages.info(request, "Se envio el correo de recordatorio")
            #logger.info(f"Correo de recordatorio enviado para la póliza {poliza.pk}")
        except Exception as e:
            messages.warning(request, f"No se pudo enviar el correo por: {e}")
            #messages.error(request,f"Error inesperado enviando correo de recordatorio para la póliza {poliza.pk}: {e}")
    return render(request, 'asesor/recordatorio.html', context)


def email_preview_cumpleaños(request, pk):
    cliente = get_object_or_404(PersonaPrincipal, pk=pk)
    telefonos = AsesorEmpresa.objects.filter(asesor__exact = cliente.asesor_cliente).values_list('telefono', flat=True)
    print(telefonos)
    context = {
        'cliente': cliente,
        'asesor': cliente.asesor_cliente,
        'telefonos': ' / '.join(telefonos),
    }
    
    return render(request, 'email_templates/felicitacion.html', context)