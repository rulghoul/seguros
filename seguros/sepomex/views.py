from django.core.paginator import Paginator
from django.shortcuts import render, redirect 
from django.views import View
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.http import JsonResponse
import logging

from . import forms as formularios
from . import models as mod
from . import xml_import as xml

@staff_member_required
def upload_xml(request):
    
    if request.method == 'POST':
        logging.info("Se recibio post")
        form = formularios.xml_sepomex_upload_form(request.POST, request.FILES)
        if form.is_valid():
            sepomex_xml = request.FILES['sepomex_xml']
            if sepomex_xml:
                # Usar la función importada para procesar el archivo
                try:
                    message = xml.recorrer_xml_datos(sepomex_xml) 
                    messages.success(request, message)
                    logging.info(message)
                    return redirect('sepomex:carga_sepomex') 
                except Exception as e:
                    messages.error(request, f"Fallo la carga del archivo por: {e}" )
            else: 
                logging.error("No se pudo leer el archivo")
                messages.error(request, "No se pudo leer el archivo" )
        else:
            logging.info("No es valido el formulario")
            messages.error(request, "No es valido el formulario" )
    else:
        logging.info("Se recibio get")
        form = formularios.xml_sepomex_upload_form()

    return render(request, 'upload_xml.html', {'form': form})

@method_decorator(login_required, name="dispatch")
class BaseListView(View):
    form_class = None
    model = None
    template_name = ''
    redirige = ''
    context_object_name = 'lista'
    title = ''
    encabezados = []
    campos = []

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(request.POST)
        return render(request, self.template_name, context)

    def get_context_data(self, post_data=None):
        context = {}
        if post_data:
            #print(post_data)
            paginas = Paginator(self.model.objects.all().order_by('nombre'), 10)
            if 'move' in post_data:
                #print(f"El valor de move es {post_data.get('move',1)}")
                form = self.form_class()
                page = paginas.get_page(post_data.get('move',1))
            else:
                form = self.form_class()
                page = paginas.get_page(1)

            if 'save' in post_data:   
                #print(f"Se entro en SAVE")
                pk = post_data.get('save')
                if not pk:
                    form = self.form_class(post_data)
                    if form.is_valid():              
                        form.save()
                        form = self.form_class()
                    #form = self.form_class()
                else:
                    #print(f"Se entro el id = {pk}")
                    objeto = self.model.objects.get(id=pk)
                    form = self.form_class(post_data, instance=objeto)  
                    if form.is_valid():              
                        form.save()
                        form = self.form_class()
                
            elif 'delete' in post_data:
                pk = post_data.get('delete')
                objeto = self.model.objects.get(pk=pk)
                objeto.delete()
                form = self.form_class() 

            elif 'edit' in post_data:
                print(f"El pk a editar es {post_data.get('edit')}")
                pk = post_data.get('edit')
                objeto = self.model.objects.get(pk=pk)
                form = self.form_class(instance=objeto)  


        else:            
            form = self.form_class()
            paginas = Paginator(self.model.objects.all().order_by('nombre'), 10)
            page = paginas.get_page(1)
            print(f"Se recupero la pagina 1 {page}")

        context['lista'] = page
        context['form'] = form 
        context['titulo'] = self.title
        context['encabezados'] = self.encabezados
        context['campos'] = self.campos
        context['redirige'] = self.redirige
        return context
    

class EstadoView(BaseListView):
    form_class = formularios.EstadoForm
    model = mod.Estado
    template_name = 'list.html'
    redirige = 'sepomex:estado'
    context_object_name = 'lista'
    title = 'Estado'
    encabezados = ['CLAVE', 'NOMBRE']
    campos = ['clave', 'nombre',]


class MunicipioView(BaseListView):
    form_class = formularios.MunicipioForm
    model = mod.Municipio
    template_name = 'list.html'
    redirige = 'sepomex:municipio'
    context_object_name = 'lista'
    title = 'Municipio'
    encabezados = ['ESTADO', 'CLAVE',  'NOMBRE']
    campos = ['estado','clave', 'nombre',]

class TipoAsentamientoView(BaseListView):
    form_class = formularios.TipoAsentamientoForm
    model = mod.TipoAsentamiento
    template_name = 'list.html'
    redirige = 'sepomex:tipo_asentamiento'
    context_object_name = 'lista'
    title = 'Tipo Asentamiento'
    encabezados = ['CLAVE', 'NOMBRE']
    campos = ['clave', 'nombre',]

class AsentamientoView(BaseListView):
    form_class = formularios.AsentamientoForm
    model = mod.Asentamiento
    template_name = 'list.html'
    redirige = 'sepomex:asentamiento'
    context_object_name = 'lista'
    title = 'Asentamiento'
    encabezados = ['MUNUCIPIO', 'TIPO ASENTAMIENTO', 'CODIGO POSTAL', 'NOMBRE']
    campos = ['municipio','tipo_asentamiento','codigo_postal', 'nombre',]

def obtener_municipios(request):
    estado_id = request.GET.get('estado_id')
    municipios = mod.Municipio.objects.filter(estado_id=estado_id).values('id', 'nombre')
    return JsonResponse({'municipios': list(municipios)})

def obtener_asentamientos(request):
    municipio_id = request.GET.get('municipio_id')
    asentamientos = mod.Asentamiento.objects.filter(municipio_id=municipio_id).values('id', 'nombre')
    return JsonResponse({'asentamientos': list(asentamientos)})