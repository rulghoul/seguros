from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string


def envia_correo_new_asesor(request, new_user):
    current_site = get_current_site(request)
    subject = "Configura tu contraseña de asesor"
    message_template = "email_templates/new_asesor.html"  
    context = {
        'protocol': 'https' if request.is_secure() else 'http',
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
        'token': default_token_generator.make_token(new_user),
        'user': new_user,
    }
    message = render_to_string(message_template, context)
    send_mail(subject, message, None, [new_user.email])
