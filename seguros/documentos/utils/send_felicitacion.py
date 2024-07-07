from django.core.mail import send_mail
from django.template.loader import render_to_string


def envia_felicitacion(poliza):
    cliente = poliza.persona_principal
    subject = f"Estimado(a) {cliente}. Feliz cumpleaños"
    message_template = "email_templates/felicitacion.html"  
    context = {
        'cliente': poliza.cliente,
        'poliza': poliza,
    }
    message = render_to_string(message_template, context)
    send_mail(subject, message, None, [cliente.correo])
