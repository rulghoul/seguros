from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.views import View
from . import models as mod
from . import forms as formularios

######################### Vista Base ###########################


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
            if 'save' in post_data:   
                print(f"Se entro en SAVE")
                pk = post_data.get('save')
                if not pk:
                    form = self.form_class(post_data)
                    if form.is_valid():              
                        form.save()
                        form = self.form_class()
                    #form = self.form_class()
                else:
                    print(f"Se entro el id = {pk}")
                    objeto = self.model.objects.get(id=pk)
                    form = self.form_class(post_data, instance=objeto)  
                    if form.is_valid():              
                        form.save()
                
            elif 'delete' in post_data:
                pk = post_data.get('delete')
                objeto = self.model.objects.get(pk=pk)
                objeto.delete()
                form = self.form_class() 
            elif 'edit' in post_data:
                pk = post_data.get('edit')
                objeto = self.model.objects.get(pk=pk)
                form = self.form_class(instance=objeto)
        else:
            form = self.form_class()

        context['lista'] = self.model.objects.all()
        context['form'] = form 
        context['titulo'] = self.title
        context['encabezados'] = self.encabezados
        context['campos'] = self.campos
        context['redirige'] = self.redirige
        return context

######################### Catalogos ###########################

class TipoConductoPagoView(BaseListView):
    form_class = formularios.TipoConductoPagoForm
    model = mod.TipoConductoPago
    template_name = 'catalogos/list.html'
    redirige = 'lista_tipo_conducto_pago'
    context_object_name = 'lista'
    title = ' Tipo De Conducto Pago'
    encabezados = ['CLAVE', 'DESCRIPCION', 'ACTIVO']
    campos = ['clave', 'descripcion', 'activo']

class TipoPersonaView(BaseListView):
    form_class = formularios.TipoPersonaForm
    model = mod.TipoPersona
    template_name = 'catalogos/list.html'
    redirige = 'lista_tipo_persona'
    context_object_name = 'lista'
    title = 'Tipo de Persona'
    encabezados = ['CLAVE', 'DESCRIPCION', 'ACTIVO']
    campos = ['clave', 'descripcion', 'activo']


class FormaPagoView(BaseListView):
    form_class = formularios.FormaPagoForm
    model = mod.FormaPago
    template_name = 'catalogos/list.html'
    redirige = 'lista_forma_pago'
    context_object_name = 'lista'
    title = 'Forma de Pago'
    encabezados = ['CLAVE', 'DESCRIPCION', 'ACTIVO']
    campos = ['clave', 'descripcion', 'activo']

class DocumentosView(BaseListView):
    form_class = formularios.DocumentosForm
    model = mod.Documentos
    template_name = 'catalogos/list.html'
    redirige = 'lista_documentos'
    context_object_name = 'lista'
    title = 'Documentos'
    encabezados = ['CLAVE', 'DESCRIPCION', 'ACTIVO']
    campos = ['clave', 'descripcion', 'activo']


class TipoMediocontactoView(BaseListView):
    form_class = formularios.TipoMediocontactoForm
    model = mod.TipoMediocontacto
    template_name = 'catalogos/list.html'
    redirige = 'lista_tipo_medio_conctacto'
    context_object_name = 'lista'
    title = 'Tipo Medio Contacto'
    encabezados = ['DESCRIPCION', 'ACTIVO']
    campos = ['descripcion', 'activo']



class ParentescoView(BaseListView):
    form_class = formularios.ParentescoForm
    model = mod.Parentesco
    template_name = 'catalogos/list.html'
    redirige = 'lista_parentesco'
    context_object_name = 'lista'
    title = 'Parentesco'
    encabezados = ['DESCRIPCION', 'ACTIVO']
    campos = ['descripcion', 'activo']


######## Tablas Principales ############

class EmpresaContratanteView(BaseListView):
    form_class = formularios.EmpresaContratanteForm
    model = mod.EmpresaContratante
    template_name = 'catalogos/list.html'
    redirige = 'lista_empresa'
    context_object_name = 'lista'
    title = 'Empresa Contratante'
    encabezados = ['CLAVE','NOMBRE', 'LOGO', 'PLECA', 'ACTIVO',]
    campos = ['clave', 'nombre', 'logo_small', 'pleca', 'activo',]

class PlanesView(BaseListView):
    form_class = formularios.PlanesForm
    model = mod.Planes
    template_name = 'catalogos/list.html'
    redirige = 'lista_planes'
    context_object_name = 'lista'
    title = 'Planes'
    encabezados = ['CLAVE','NOMBRE', 'EMPRESA',  'ACTIVO',]
    campos = ['clave', 'nombre', 'empresa',  'activo',]