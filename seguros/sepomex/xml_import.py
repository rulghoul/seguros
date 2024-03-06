import xml.etree.ElementTree as ET
from django.db import transaction
from . import models 

def procesar_tabla(elem):
    datos_tabla = {
        # Aquí mantienes la extracción como ya la tienes
    }

    # Intenta obtener o crear el Estado
    estado, created = models.Estado.objects.get_or_create(
        clave=datos_tabla['c_estado'],
        defaults={'nombre': datos_tabla['d_estado']}
    )
    
    # Obtener o crear TipoAsentamiento
    tipo_asentamiento, created = models.TipoAsentamiento.objects.get_or_create(
        clave=datos_tabla['c_tipo_asenta'], # Asumiendo que esta es la clave correcta
        defaults={'nombre': datos_tabla['d_tipo_asenta']}
    )

    # Obtener o crear Municipio (depende del Estado)
    municipio, created = models.Municipio.objects.get_or_create(
        clave=datos_tabla['D_mnpio'],
        estado=estado,
        defaults={'nombre': datos_tabla['c_mnpio']}
    )
    
    # Finalmente, crear el Asentamiento
    asentamiento, created = models.Asentamiento.objects.get_or_create(
        codigo_postal=datos_tabla['d_CP'],
        municipio=municipio,
        tipo_asentamiento=tipo_asentamiento,
        defaults={'nombre': datos_tabla['d_asenta']}
    )

@transaction.atomic
def recorrer_xml_datos(archivo_xml):
    try:
        sepomex = ET.iterparse(archivo_xml, events=("start",))
        models.Estado.objects.all().delete()
        models.Asentamiento.objects.all().delete()
        for event, elem in sepomex:
            if elem.tag == '{NewDataSet}table':
                procesar_tabla(elem)
                elem.clear()  # Limpiar el elemento para ahorrar memoria
    except Exception as e:
        print(f"Fallo el procesamiento de :{archivo_xml} por {e}" )  
            

