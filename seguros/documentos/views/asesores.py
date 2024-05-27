import logging
from django.views.generic.edit import  UpdateView, FormView
from django.views.generic import ListView

from documentos import models as mod
from documentos import forms as formularios
from django.shortcuts import render, redirect
from django.contrib import messages 

from django.db import transaction
from django.contrib.auth.models import User

from .catalogos import BaseListView


from documentos.utils.send_email_new_asesor import envia_correo_new_asesor as envia 

class EmpresaContratanteView(BaseListView):
    form_class = formularios.EmpresaContratanteForm
    model = mod.EmpresaContratante
    lista_objetos = mod.EmpresaContratante.objects.all().order_by('clave')
    template_name = 'catalogos/list.html'
    redirige = 'documentos:lista_empresa'
    context_object_name = 'lista'
    title = 'Empresa Contratante'
    encabezados = ['CLAVE','NOMBRE', 'LINK','LOGO', 'ACTIVO',]
    campos = ['clave', 'nombre', 'link', 'logo_small', 'activo',]

class PlanesView(BaseListView):
    form_class = formularios.PlanesForm
    model = mod.Planes
    template_name = 'catalogos/list.html'
    redirige = 'documentos:lista_planes'
    context_object_name = 'lista'
    title = 'Planes'
    encabezados = ['NOMBRE', 'EMPRESA',  'ACTIVO',]
    campos = ['nombre', 'empresa',  'activo',]


class PersonaPrincipalAdd(FormView):
    template_name = "catalogos/add_cliente.html"
    form_class = formularios.PersonaPrincipalForm
    success_url = "sepomex:asentamiento_details"
    
    def form_valid(self, form):
        logging.info("Entra en validacion")
        try:
            asesor_instance = mod.Asesor.objects.get(usuario=self.request.user)
            form.instance.asesor = asesor_instance
            logging.info("Encontró al asesor")
        except mod.Asesor.DoesNotExist:
            logging.info("No encontró al asesor")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        logging.info("Entra en Contexto")
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Agregar Cliente"
        context["redirige"] = "documentos:principal_add"
        context["informacion"] = "sepomex:asentamiento_details"
        return context
    
class PersonaPrincipalUpdate(UpdateView):
    model = mod.PersonaPrincipal
    template_name = "catalogos/add_cliente.html"
    form_class = formularios.PersonaPrincipalForm
    success_url = "documentos:principal_update"
    
    def form_valid(self, form):
        if mod.Asesor.objects.filter(usuario = self.request.user).exists():
            form.instance.asesor = mod.Asesor.objects.filter(usuario = self.request.user)  
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["titulo"] = "Actualizar Cliente"
        context["redirige"] = "documentos:principal_update"
        context["informacion"] = "sepomex:asentamiento_details"
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        # Asume que tu instancia ya está cargada en self.object gracias a UpdateView
        asentamiento = self.object.asentamiento
        initial['codigo_postal'] = asentamiento.codigo_postal
        initial['municipio'] = asentamiento.municipio.nombre
        initial['estado'] = asentamiento.municipio.estado.nombre
        return initial

class ListCliente(ListView):
    template_name = "catalogos/list_cliente.html"
    model = mod.PersonaPrincipal
    paginate_by = 100
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Clientes"
        context["encabezados"] = ('Nombre', 'Correo', 'Telefono', "Asesor")
        context["add"] = "documentos:principal_add"
        context["add_label"] = "Nuevo Cliente"
        context["update"] = "documentos:principal_update"
        context["borra"] = "documentos:principal_update"
        return context
    
#Asesores

    
@transaction.atomic
def crear_o_editar_asesor(request, pk=None):
    if pk:
        asesor = mod.Asesor.objects.get(pk=pk)
        user = asesor.usuario
    else:
        asesor = mod.Asesor()
        user = User()

    helper = formularios.AsesorEmpresaFormSetHelper
    formset = formularios.AsesorEmpresaFormset(request.POST or None, instance=asesor)
    
    if request.method == 'POST':
        user_form = formularios.UserForm(request.POST, instance=user)
        if user_form.is_valid():
            created_user = user_form.save()
            asesor.usuario = created_user
            asesor.save()                        
            if formset.is_valid():
                formset.save()
                envia(request, created_user)
                return redirect('home') 
                
    else:
        user_form = formularios.UserForm(instance=user)
        formset = formularios.AsesorEmpresaFormset(instance=asesor)
    
    return render(request, 'catalogos/add_asesor.html', {
        'user_form': user_form,
        'formset': formset,
        'helper': helper,
        'titulo': 'Nuevo Asesor'
    })

class ListAseror(ListView):
    template_name = "catalogos/list_asesor.html"
    model = mod.Asesor
    paginate_by = 100
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Asesores"
        context["encabezados"] = ('Nombre', 'Usuario', 'Empresas')
        context["add"] = "documentos:asesor_add"
        context["add_label"] = "Nuevo Asesor"
        context["update"] = "documentos:asesor_update"
        context["borra"] = "documentos:asesor_update"
        return context
    