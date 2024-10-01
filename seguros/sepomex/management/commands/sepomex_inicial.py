import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from sepomex.models import Estado, Municipio, Asentamiento, TipoAsentamiento  # Importa tus modelos

class Command(BaseCommand):
    help = 'Load initial data using loaddata if not already loaded.'

    def handle(self, *args, **kwargs):
        json_file_path = os.path.join('/seguros', 'sepomex_backup.json')  # Ruta al archivo JSON

        # Verificar si los datos ya se han cargado
        if not (Estado.objects.exists() or Municipio.objects.exists() or 
                Asentamiento.objects.exists() or TipoAsentamiento.objects.exists()):
            try:
                # Cargar los datos utilizando el comando loaddata
                call_command('loaddata', json_file_path)
                self.stdout.write(self.style.SUCCESS('Data loaded successfully using loaddata.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'An error occurred while loading data: {e}'))
        else:
            self.stdout.write(self.style.WARNING('Data already loaded. Skipping.'))
