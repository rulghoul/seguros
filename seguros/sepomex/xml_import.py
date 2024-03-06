import xml.etree.ElementTree as ET
from django.db import transaction
from . import models 

def procesar_tabla(elem):
    datos_tabla = {
        'd_codigo': elem.find('{NewDataSet}d_codigo').text if elem.find('{NewDataSet}d_codigo') is not None else None,
        'd_asenta': elem.find('{NewDataSet}d_asenta').text if elem.find('{NewDataSet}d_asenta') is not None else None,
        'd_tipo_asenta': elem.find('{NewDataSet}d_tipo_asenta').text if elem.find('{NewDataSet}d_tipo_asenta') is not None else None,
        'D_mnpio': elem.find('{NewDataSet}D_mnpio').text if elem.find('{NewDataSet}D_mnpio') is not None else None,
        'd_estado': elem.find('{NewDataSet}d_estado').text if elem.find('{NewDataSet}d_estado') is not None else None,
        'd_ciudad': elem.find('{NewDataSet}d_ciudad').text if elem.find('{NewDataSet}d_ciudad') is not None else None,
        'd_CP': elem.find('{NewDataSet}d_CP').text if elem.find('{NewDataSet}d_CP') is not None else None,
        'c_estado': elem.find('{NewDataSet}c_estado').text if elem.find('{NewDataSet}c_estado') is not None else None,
        'c_oficina': elem.find('{NewDataSet}c_oficina').text if elem.find('{NewDataSet}c_oficina') is not None else None,
        'c_CP': elem.find('{NewDataSet}c_CP').text if elem.find('{NewDataSet}c_CP') is not None else None,
        'c_tipo_asenta': elem.find('{NewDataSet}c_tipo_asenta').text if elem.find('{NewDataSet}c_tipo_asenta') is not None else None,
        'c_mnpio': elem.find('{NewDataSet}c_mnpio').text if elem.find('{NewDataSet}c_mnpio') is not None else None,
        'id_asenta_cpcons': elem.find('{NewDataSet}id_asenta_cpcons').text if elem.find('{NewDataSet}id_asenta_cpcons') is not None else None,
        'd_zona': elem.find('{NewDataSet}d_zona').text if elem.find('{NewDataSet}d_zona') is not None else None,
        'c_cve_ciudad': elem.find('{NewDataSet}c_cve_ciudad').text if elem.find('{NewDataSet}c_cve_ciudad') is not None else None,
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
        clave=datos_tabla['c_mnpio'],
        estado=estado,
        defaults={'nombre': datos_tabla['D_mnpio']}
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
                try:
                    procesar_tabla(elem)
                except Exception as e:
                    print(f"Fallo el elemento por: {e}")
                elem.clear()  # Limpiar el elemento para ahorrar memoria
    except Exception as e:
        print(f"Fallo el procesamiento de :{archivo_xml} por {e}" )  
            

