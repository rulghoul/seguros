import os
import shutil
from django.core.management.base import BaseCommand
from tema.models import parametros_colores, parametros_imagenes
from django.conf import settings

class Command(BaseCommand):
    help = 'Carga valores iniciales y mueve archivos a la carpeta media'

    def handle(self, *args, **kwargs):
        if not parametros_colores.objects.exists():
            # Cargar valores iniciales
            colores_iniciales = [
                {'elemento': 'pleca', 'color': '#79AEC8'},
                {'elemento': 'menu', 'color': '#417690'},
                {'elemento': 'fondo', 'color': '#F8F8F8'},
            ]

            imagenes_iniciales = [
                {'title': 'logo', 'image': 'images_parameter/logo.png'},
                {'title': 'bigLogo', 'image': 'images_parameter/big_logo.png'},
                {'title': 'fondo', 'image': 'images_parameter/background.png'},
            ]

            for data in colores_iniciales:
                parametros_colores.objects.update_or_create(
                    elemento=data['elemento'], defaults={'color': data['color']}
                )
                self.stdout.write(self.style.SUCCESS('Successfully loaded data: {}'.format(data)))

            for data in imagenes_iniciales:
                parametros_imagenes.objects.update_or_create(
                    title=data['title'], defaults={'image': data['image']}
                )
                self.stdout.write(self.style.SUCCESS('Successfully loaded data: {}'.format(data)))

            # Mover archivos a la carpeta media
            script_dir = os.path.dirname(os.path.abspath(__file__))
            source_dir = os.path.join(script_dir, 'imagenes')
            target_dir = os.path.join(settings.MEDIA_ROOT, 'images_parameter')

            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            for filename in os.listdir(source_dir):
                source_file = os.path.join(source_dir, filename)
                target_file = os.path.join(target_dir, filename)
                shutil.move(source_file, target_file)
                self.stdout.write(self.style.SUCCESS('Successfully moved file: {}'.format(filename)))
            print("Se cargaron los valores iniciales de imagenes y colores")
        else:
            print("Ya se habian cargado los valores por iniciales de imagenes y colores")