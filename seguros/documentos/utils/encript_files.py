from cryptography.fernet import Fernet
from django.core.files.base import ContentFile
from django.conf import settings

cipher_suite = Fernet(settings.ENCRYPTION_KEY)

def encripta_archivo(file):
    contenido = file.read()
    encriptado = cipher_suite.encrypt(contenido)
    archivo_encriptado = ContentFile(encriptado, name=file.name  + '.enc')
    return archivo_encriptado

def desencripta_archivo(file):
    contenido = file.read()
    desencriptado = cipher_suite.decrypt(contenido)
    archivo_desencriptado = ContentFile(desencriptado, name=file.name.replace('.enc', ''))
    return archivo_desencriptado