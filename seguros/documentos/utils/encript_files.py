from cryptography.fernet import Fernet
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
import io

cipher_suite = Fernet(settings.ENCRYPTION_KEY)

def encripta_archivo(file):
    contenido = file.read()
    encriptado = cipher_suite.encrypt(contenido)    
    return InMemoryUploadedFile(
        file=io.BytesIO(encriptado),
        field_name=None,
        name=file.name + '.enc',
        content_type='application/octet-stream',
        size=len(encriptado),
        charset=None
    )

def desencripta_archivo(file):
    if file.name.endswith("enc"):        
        contenido = file.read()
        desencriptado = cipher_suite.decrypt(contenido)
        return InMemoryUploadedFile(
            file=io.BytesIO(desencriptado),
            field_name=None,
            name=file.name.replace('.enc', ''),
            content_type='application/octet-stream',
            size=len(desencriptado),
            charset=None
        )
    else:
        return file
        
#240627005025 folio 