from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from documentos.models import AsesorEmpresa

from .imagen_mail import get_imagen_url

def envia_recordatorio(poliza):
    cliente = poliza.persona_principal
    asesor_empresa = AsesorEmpresa.objects.get(empresa = poliza.empresa, asesor = poliza.asesor_poliza)
    subject = f"Recordatorio de Pago de su Póliza de Seguro"
    message_template = "email_templates/recordatorio_pago.html"  
    
    imagen_url = get_imagen_url('agencia')

    context = {
        'cliente': cliente,        
        'poliza': poliza,
        'asesor': asesor_empresa,
        'imagen_url': imagen_url,
    }

    message_html = render_to_string(message_template, context)
    
    plain_message = strip_tags(message_html)

    msg = EmailMultiAlternatives(
        subject, 
        plain_message, 
        "ghoulrul@gmail.com",
        [cliente.correo, asesor_empresa.correo_empleado],
    )
    msg.attach_alternative(message_html, "text/html")
    

    msg.send()


