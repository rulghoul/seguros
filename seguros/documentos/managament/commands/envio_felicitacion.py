from django.core.management.base import BaseCommand
from seguros.documentos.models import PersonaPrincipal
from datetime import datetime
from seguros.documentos.utils.send_felicitacion import envia_felicitacion as envia

class Command(BaseCommand):
    help = "Envia un correo de Felicitacion a los clientes activos"

    def handle(self, *args, **options):
        hoy = datetime.now().date()
        #Solo que el mes y dia
        festejados = PersonaPrincipal.objects.filter(activo=True, fecha_nacimiento=hoy)
        for festejado in festejados:
            envia(festejado)
