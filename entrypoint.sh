#!/bin/sh

# Detener la ejecución en caso de error
set -e

# Ejecutar migraciones
#python manage.py makemigrations --noinput
python manage.py migrate --noinput

#python manage.py loaddata sepomex_backup.json
#rm sepomex_backup.json


#python manage.py loaddata documentos.json
#rm documentos.json

# Recopilar archivos estáticos
#python manage.py collectstatic --noinput --clear

python manage.py crear_usuario
#Valores del tema
python manage.py carga_tema_base

# Opción con Gunicorn (asegúrate de tener gunicorn en tu requirements.txt)
gunicorn --workers 4 -t 240 seguros.wsgi:application --bind 0.0.0.0:8000 --log-level debug --log-file - --access-logfile - --error-logfile -

