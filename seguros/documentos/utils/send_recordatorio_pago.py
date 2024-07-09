from django.core.mail import send_mail
from django.template.loader import render_to_string
from documentos.models import Poliza, PersonaPrincipal, Asesor, AsesorEmpresa


def envia_recordatorio(poliza, semana):
    cliente = poliza.persona_principal
    asesor_empresa = AsesorEmpresa.objects.filter(empresa = poliza.empresa, asesor = poliza.asesor_poliza)
    subject = f"Estimado(a) {cliente}, le recordamos que su pago de la {poliza} esta a {semana} semana(s) del vencimiento"
    message_template = "email_templates/recordatorio_pago.html"  
    context = {
        'cliente': poliza.cliente,        
        'poliza': poliza,
        'semana': semana,
        'asesor': asesor_empresa,
    }
    message = render_to_string(message_template, context)
    send_mail(subject, message, None, [cliente.correo, asesor_empresa.email])
