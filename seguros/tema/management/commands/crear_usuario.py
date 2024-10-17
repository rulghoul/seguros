#__author__ = 'dkarchmer@gmail.com'
#https://github.com/dkarchmer/aws-eb-docker-django/blob/master/.ebextensions/01-main.config
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from tema.models import Subscription


class Command(BaseCommand):
    help = "Crea un usuario inicial"

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write('Solo se crea un usuario si no existe alguno previamente')
        else:
            username = os.getenv('SEGUROS_SUPERUSER_USERNAME', 'organizame.admin')
            email = os.getenv('SEGUROS_SUPERUSER_EMAIL', 'admin@example.com')
            password = os.getenv('SEGUROS_SUPERUSER_PASSWORD', 'admin')
            self.stdout.write(f'Creando la cuenta para {username} ({email})')
            try:
                usuario = User.objects.create_superuser(username=username, email=email, password=password)
                suscrip = Subscription(user=usuario,subscription_type='A')
                suscrip.save()
                self.stdout.write(f"Se creo el usuario administrador {username}")
            except Exception as e:
                self.stderr.write(f'Fallo la creacion del usuario por: {e}')