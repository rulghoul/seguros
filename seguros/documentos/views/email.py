from django.shortcuts import render
from documentos.models import Poliza, PersonaPrincipal
from django.shortcuts import get_object_or_404

def email_preview_recordatorio(request, pk, semana):
    poliza = get_object_or_404(Poliza, pk=pk)
    cliente = poliza.persona_principal

    context = {
        'cliente': cliente,
        'semana': semana,
        'poliza': poliza
    }
    
    return render(request, 'email_templates/recordatorio_pago.html', context)


def email_preview_cumpleaños(request, pk):
    cliente = get_object_or_404(PersonaPrincipal, pk=pk)

    context = {
        'cliente': cliente,
        'asesor':cliente.asesor_cliente,
    }
    
    return render(request, 'email_templates/felicitacion.html', context)