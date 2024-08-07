from django.shortcuts import render
from documentos.models import Poliza, PersonaPrincipal, AsesorEmpresa
from django.shortcuts import get_object_or_404, render
from documentos.utils.send_recordatorio_pago import envia_recordatorio
from django.contrib import messages 
import logging
logger = logging.getLogger(__name__)

def email_preview_recordatorio(request, pk):
    poliza = get_object_or_404(Poliza, pk=pk)
    cliente = poliza.persona_principal
    asesor_empresa = AsesorEmpresa.objects.get(empresa = poliza.empresa, asesor = poliza.asesor_poliza)
    context = {
        'cliente': cliente,
        'poliza': poliza, 
        'asesor': asesor_empresa
    }
    
    return render(request, 'email_templates/recordatorio_pago.html', context)

def email_recordatorio(request, pk):
    poliza = get_object_or_404(Poliza, pk=pk) 
    context = {
        "poliza":poliza,
        "tilulo": f"Enviar recordatorio para la poliza {poliza}",
    }
    if request.method == "POST":
        try:
            envia_recordatorio(poliza=poliza)
            messages.info(request, "Se envio el correo de recordatorio")
            logger.info(f"Correo de recordatorio enviado para la póliza {poliza.pk}")
        except Exception as e:
            messages.warning(request, f"No se pudo enviar el correo por: {e}")
            logger.error(f"Error inesperado enviando correo de recordatorio para la póliza {poliza.pk}: {e}")
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