from django.core.management.base import BaseCommand
from seguros.documentos.models import Poliza
from datetime import datetime, timedelta
from seguros.documentos.utils.send_recordatorio_pago import envia_recordatorio as envia

class Command(BaseCommand):
    help = "Crea un usuario inicial"

    def handle(self, *args, **options):
        fecha_pago = datetime.now().date() + timedelta(days=3)
        por_expirar = Poliza.objects.filter(activo=True, fecha_pago=fecha_pago)
        for expirado in por_expirar:
            envia(expirado)
