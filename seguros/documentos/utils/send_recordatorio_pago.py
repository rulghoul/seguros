from django.core.mail import send_mail
from django.template.loader import render_to_string


def envia_recordatorio(poliza):
    cliente = poliza.persona_principal
    subject = f"Estimado(a) {cliente}, le recordamos que su pago de la {poliza} esta por vencerse"
    message_template = "email_templates/recordatorio_pago.html"  
    context = {
        'cliente': poliza.cliente,
        'poliza': poliza,
    }
    message = render_to_string(message_template, context)
    send_mail(subject, message, None, [cliente.correo, cliente.asesor_cliente.email])
