import xml.etree.ElementTree as ET

def procesar_elemento(elem):
    # Esta función procesa cada elemento. Puedes adaptarla según lo que necesites hacer.
    # Por ejemplo, imprimir el tag y atributos del elemento
    print(elem.tag, elem.attrib)

def recorrer_xml_grande(archivo_xml):
    # Iterar sobre el evento de fin de cada elemento
    for event, elem in ET.iterparse(archivo_xml, events=("end",)):
        procesar_elemento(elem)
        # Es importante limpiar el elemento para no consumir memoria innecesariamente
        elem.clear()


def agregar_estructura(estructuras, ruta):
    # Convierte la ruta (lista de tags) en una cadena única para almacenamiento
    ruta_str = " -> ".join(ruta)
    if ruta_str not in estructuras:
        estructuras.add(ruta_str)
        print(ruta_str)

def recorrer_xml_unico(archivo_xml):
    estructuras = set()
    ruta_actual = []
    for event, elem in ET.iterparse(archivo_xml, events=("start", "end")):
        if event == "start":
            ruta_actual.append(elem.tag)  # Agrega el tag actual a la ruta
        elif event == "end":
            agregar_estructura(estructuras, ruta_actual)
            ruta_actual.pop()  # Remueve el tag al finalizar el elemento
            elem.clear()


def procesar_tabla(elem):
    # Diccionario para almacenar los datos de los campos de interés
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

    # Aquí puedes hacer lo que necesites con los datos, como imprimirlos
    print(datos_tabla)

def recorrer_xml_datos(archivo_xml):
    limite = 50
    contador = 0
    for event, elem in ET.iterparse(archivo_xml, events=("start",)):
        if contador == limite:
            break
        if elem.tag == '{NewDataSet}table':
            procesar_tabla(elem)
            elem.clear()  # Limpiar el elemento para ahorrar memoria
            contador += 1



if __name__ == "__main__":
    archivo_xml = "CPdescarga.xml"  # Asegúrate de cambiar esto por la ruta de tu archivo
    recorrer_xml_datos(archivo_xml)
