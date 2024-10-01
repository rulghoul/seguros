import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from sepomex.models import Estado, Municipio, Asentamiento, TipoAsentamiento  # Importa tus modelos

class Command(BaseCommand):
    help = 'Load initial data using loaddata if not already loaded.'

    def handle(self, *args, **kwargs):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(current_dir, '..', '..', '..', 'sepomex_backup.json')  # Ruta al archivo JSON
        print(json_file_path)

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
            if os.path.exists(json_file_path):
                self.stdout.write(self.style.SUCCESS(f"Existe el archivo {json_file_path}"))
            else:
                self.stdout.write(self.style.ERROR(f"No existe el archivo {json_file_path}"))
            self.stdout.write(self.style.WARNING('Data already loaded. Skipping.'))
