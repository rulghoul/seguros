from django.core.mail import send_mail
from django.template.loader import render_to_string
from documentos.models import AsesorEmpresa


def envia_felicitacion(cliente):
    subject = f"¡Feliz Cumpleaños, [Nombre del Cliente]!"
    message_template = "email_templates/felicitacion.html"  
    telefonos = AsesorEmpresa.objects.filter(asesor = cliente.asesor_cliente).values_list('telefono', flat=True)
    context = {
        'cliente': cliente,
        'asesor':cliente.asesor_cliente,
        'telefonos': ' / '.join(telefonos),
    }
    message = render_to_string(message_template, context)
    send_mail(subject, message, None, [cliente.correo, cliente.asesor_cliente.usuario.email])
