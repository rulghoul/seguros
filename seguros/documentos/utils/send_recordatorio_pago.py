from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from documentos.models import AsesorEmpresa


def envia_recordatorio(poliza):
    cliente = poliza.persona_principal
    asesor_empresa = AsesorEmpresa.objects.get(empresa = poliza.empresa, asesor = poliza.asesor_poliza)
    subject = f"Recordatorio de Pago de su Póliza de Seguro"
    message_template = "email_templates/recordatorio_pago.html"  
    plain_message = strip_tags(message_template)
    context = {
        'cliente': cliente,        
        'poliza': poliza,
        'asesor': asesor_empresa,
    }
    message = render_to_string(message_template, context)
    msg = EmailMultiAlternatives(
        subject, 
        plain_message, 
        "ghoulrul@gmail.com",
        [cliente.correo, asesor_empresa.correo_empleado]
    )
    msg.attach_alternative(message, "text/html")
    msg.send()
