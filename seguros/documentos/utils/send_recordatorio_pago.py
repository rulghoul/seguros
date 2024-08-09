from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from documentos.models import AsesorEmpresa
from django.contrib import messages 
from tema.models import parametros_imagenes



def get_imagen_cdi(nombre, request):
    try:
        imagen_parametro = parametros_imagenes.objects.get(title=nombre)   
        #messages.info(request, f"La imagen es {imagen_parametro.image}")
        return f"https://{request.get_host()}:{request.get_port()}{imagen_parametro.image.url}"
    except parametros_imagenes.DoesNotExist:
        messages.error(request, f"No se encontro la imagen {nombre}")
        return None

def envia_recordatorio(poliza, request):
    cliente = poliza.persona_principal
    asesor_empresa = AsesorEmpresa.objects.get(empresa = poliza.empresa, asesor = poliza.asesor_poliza)
    subject = f"Recordatorio de Pago de su Póliza de Seguro"
    message_template = "email_templates/recordatorio_pago.html"  
    
    imagen_url = get_imagen_cdi('agencia', request)

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


