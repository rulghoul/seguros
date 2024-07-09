from django.core.management.base import BaseCommand
from seguros.documentos.models import Poliza
from datetime import datetime, timedelta
from seguros.documentos.utils.send_recordatorio_pago import envia_recordatorio as envia
import logging

class Command(BaseCommand):
    help = "Envía recordatorios de pago para pólizas próximas a expirar"

    def handle(self, *args, **options):
        logger = logging.getLogger(__name__)
        hoy = datetime.now().date()
        for semana in [3,2,1]:
            fecha_pago = hoy + timedelta(weeks=semana)
            por_expirar = Poliza.objects.filter(activo=True, fecha_vigencia=fecha_pago)
            for poliza in por_expirar:
                envia(poliza, semana)
                logger.info(f'Recordatorio enviado para póliza {poliza} a {semana} semana(s) del vencimiento.')
        
        self.stdout.write(self.style.SUCCESS(f'{hoy.isocalendar}: Recordatorios de pago enviados con éxito'))