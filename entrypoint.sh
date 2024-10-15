#!/bin/sh

# Detener la ejecución en caso de error
set -e

# Tareas programadas
crontab cronseguros.cfg
#crontab -r 
#crontab -l | { cat; echo "0 6 * * * /usr/local/bin/python /seguros/seguros/manage.py envio_recordatorio"; } | crontab -
#crontab -l | { cat; echo "30 6 * * * /usr/local/bin/python /seguros/seguros/manage.py envio_felicitacion"; } | crontab -


# Ejecutar migraciones
#python manage.py makemigrations --noinput
python manage.py migrate --noinput

if [ ! -f /seguros/documentos.json ]; then
python manage.py loaddata documentos.json
rm documentos.json

# Recopilar archivos estáticos
python manage.py collectstatic --noinput --link

#Crea el usuario para la administracion del sistema
python manage.py crear_usuario
#Carga los valores de sepomex si aun no se ha realizado
echo "Cargando valores de sepomex"
if [ ! -f /seguros/sepomex_backup.json ]; then
    python manage.py sepomex_inicial
    rm sepomex_backup.json
fi
#Valores del tema
python manage.py carga_tema_base

# Opción con Gunicorn (asegúrate de tener gunicorn en tu requirements.txt)
gunicorn --workers ${DJANGO_WORKERS:-2} -t 240 seguros.wsgi:application --bind 0.0.0.0:8000 --log-level debug --log-file - --access-logfile - --error-logfile -

