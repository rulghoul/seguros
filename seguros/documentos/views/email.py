from django.shortcuts import render
from documentos.models import Poliza, PersonaPrincipal, AsesorEmpresa
from django.shortcuts import get_object_or_404

def email_preview_recordatorio(request, pk, semana):
    poliza = get_object_or_404(Poliza, pk=pk)
    cliente = poliza.persona_principal
    asesor_empresa = AsesorEmpresa.objects.get(asesor = cliente.asesor_cliente)
    context = {
        'cliente': cliente,
        'semana': semana,
        'poliza': poliza, 
        'asesor': asesor_empresa
    }
    
    return render(request, 'email_templates/recordatorio_pago.html', context)


def email_preview_cumpleaños(request, pk):
    cliente = get_object_or_404(PersonaPrincipal, pk=pk)
    asesor_empresa = AsesorEmpresa.objects.get(asesor = cliente.asesor_cliente)
    telefonos = AsesorEmpresa.objects.filter(asesor__exact = cliente.asesor_cliente).values_list('telefono', flat=True)
    print(telefonos)
    context = {
        'cliente': cliente,
        'asesor': asesor_empresa,
        'telefonos': ' / '.join(telefonos),
    }
    
    return render(request, 'email_templates/felicitacion.html', context)