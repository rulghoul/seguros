import logging
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages #Mensajes
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView
from django.views import View
from django.db import transaction
from django.contrib.auth.models import User

from . import models as mod
from . import forms as formularios
from .utils.send_email_new_asesor import envia_correo_new_asesor as envia 

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
    redirige = 'documentos:lista_tipo_conducto_pago'
    context_object_name = 'lista'
    title = ' Tipo De Conducto Pago'
    encabezados = ['CLAVE', 'DESCRIPCION', 'ACTIVO']
    campos = ['clave', 'descripcion', 'activo']

class TipoPersonaView(BaseListView):
    form_class = formularios.TipoPersonaForm
    model = mod.TipoPersona
    template_name = 'catalogos/list.html'
    redirige = 'documentos:lista_tipo_persona'
    context_object_name = 'lista'
    title = 'Tipo de Persona'
    encabezados = ['CLAVE', 'DESCRIPCION', 'ACTIVO']
    campos = ['clave', 'descripcion', 'activo']


class FormaPagoView(BaseListView):
    form_class = formularios.FormaPagoForm
    model = mod.FormaPago
    template_name = 'catalogos/list.html'
    redirige = 'documentos:lista_forma_pago'
    context_object_name = 'lista'
    title = 'Forma de Pago'
    encabezados = ['CLAVE', 'DESCRIPCION', 'ACTIVO']
    campos = ['clave', 'descripcion', 'activo']

class DocumentosView(BaseListView):
    form_class = formularios.DocumentosForm
    model = mod.Documentos
    template_name = 'catalogos/list.html'
    redirige = 'documentos:lista_documentos'
    context_object_name = 'lista'
    title = 'Documentos'
    encabezados = ['CLAVE', 'DESCRIPCION', 'ACTIVO']
    campos = ['clave', 'descripcion', 'activo']


class TipoMediocontactoView(BaseListView):
    form_class = formularios.TipoMediocontactoForm
    model = mod.TipoMediocontacto
    template_name = 'catalogos/list.html'
    redirige = 'documentos:lista_tipo_medio_conctacto'
    context_object_name = 'lista'
    title = 'Tipo Medio Contacto'
    encabezados = ['DESCRIPCION', 'ACTIVO']
    campos = ['descripcion', 'activo']



class ParentescoView(BaseListView):
    form_class = formularios.ParentescoForm
    model = mod.Parentesco
    template_name = 'catalogos/list.html'
    redirige = 'documentos:lista_parentesco'
    context_object_name = 'lista'
    title = 'Parentesco'
    encabezados = ['DESCRIPCION', 'ACTIVO']
    campos = ['descripcion', 'activo']


######## Tablas Principales ############

class EmpresaContratanteView(BaseListView):
    form_class = formularios.EmpresaContratanteForm
    model = mod.EmpresaContratante
    template_name = 'catalogos/list.html'
    redirige = 'documentos:lista_empresa'
    context_object_name = 'lista'
    title = 'Empresa Contratante'
    encabezados = ['CLAVE','NOMBRE', 'LOGO', 'PLECA', 'ACTIVO',]
    campos = ['clave', 'nombre', 'logo_small', 'pleca', 'activo',]

class PlanesView(BaseListView):
    form_class = formularios.PlanesForm
    model = mod.Planes
    template_name = 'catalogos/list.html'
    redirige = 'documentos:lista_planes'
    context_object_name = 'lista'
    title = 'Planes'
    encabezados = ['CLAVE','NOMBRE', 'EMPRESA',  'ACTIVO',]
    campos = ['clave', 'nombre', 'empresa',  'activo',]


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
    template_name = "catalogos/add_cliente.html"
    form_class = formularios.PersonaPrincipalForm
    success_url = "home"
    
    def form_valid(self, form):
        if mod.Asesor.objects.filter(usuario = self.request.user).exists():
            form.instance.asesor = mod.Asesor.objects.filter(usuario = self.request.user)  
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["titulo"] = "Actualizar Cliente"
        context["redirige"] = "documentos:principal_update"
        context["informacion"] = "documentos:asentamiento_details"
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        # Asume que tu instancia ya está cargada en self.object gracias a UpdateView
        asentamiento = self.object.asentamiento
        initial['codigo_postal'] = asentamiento.codigo_postal
        initial['municipio'] = asentamiento.municipio.nombre
        initial['estado'] = asentamiento.municipio.estado.nombre
        return initial
    
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
    

class Poliza_List(LoginRequiredMixin, ListView):
    model = mod.Poliza
    template_name = 'asesor/polizas.html'
    context_object_name = 'polizas'

    def get_queryset(self):
        user = self.request.user
        try:
            asesor = mod.Asesor.objects.get(usuario=user)        
            return mod.Poliza.objects.filter(asesor=asesor)
        except mod.Asesor.DoesNotExist:
            if user.is_staff or user.is_superuser:
                return mod.Poliza.objects.all()
            else: 
                return mod.Poliza.objects.none()
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Polizas"
        context["add"] = "documentos:poliza_add"
        context["add_label"] = "Nueva Poliza"
        context["update"] = "documentos:poliza_update"
        context["borra"] = "documentos:poliza_update"
        return context
            
    
@transaction.atomic
def edit_poliza(request, pk=None):
    try:
        asesor_instance = mod.Asesor.objects.get(usuario=request.user)
        #messages.info(request, "Se encontró al asesor")
    except mod.Asesor.DoesNotExist:
        messages.warning(request, "No encontró al asesor")

    if pk:
        poliza = get_object_or_404(mod.Poliza, pk=pk)
        titulo = f"Editar Poliza: {poliza.numero_poliza}"
        persona_principal = poliza.persona_principal  # Acceder a la persona principal existente
    else:
        poliza = mod.Poliza()
        persona_principal = mod.PersonaPrincipal()
        poliza.asesor = asesor_instance
        persona_principal.asesor = asesor_instance
        titulo = f"Nueva Poliza"

    helper_beneficiario = formularios.BeneficiariosHelper
    formset_beneficiario = formularios.BeneficiariosFormset(request.POST or None, instance=poliza)

    if request.method == 'POST':
        messages.success(request, "Se entro al post")
        form_poliza = formularios.PolizaForm(request.POST, instance=poliza, initial={'asesor': asesor_instance})
        form_persona_principal = formularios.PersonaPrincipalForm(request.POST, instance=persona_principal, initial={'asesor': asesor_instance})                
        form_persona_principal.instance.asesor = asesor_instance

        if form_poliza.is_valid()  and formset_beneficiario.is_valid():
            messages.success(request, "Los formularios son validos")
            total_porcentaje = sum(form.cleaned_data['porcentaje_participacion'] for form in formset_beneficiario)
            messages.success(request, f"Los formularios son validos y el porcentaje es {total_porcentaje}")
            if total_porcentaje == 100:
                persona_principal = form_persona_principal.save()  # Guarda la persona principal
                poliza = form_poliza.save(commit=False)  # Prepara la póliza para guardar
                poliza.persona_principal = persona_principal  # Vincula la persona principal a la póliza
                poliza.save()  # Guarda la póliza
                formset_beneficiario.save()
                messages.success(request, "Póliza guardada con éxito.")
                return redirect('poliza_list')  # Redirige a una lista o alguna URL definida
            else:
                messages.error(request, "La suma de los porcentajes de participación de los beneficiarios debe ser exactamente 100%.")  
        else:
            if not form_poliza.is_valid():
                messages.error(request, "Hubo un problema con el formulario de la póliza: " + ", ".join([f"{field}: {error}" for field, error in form_poliza.errors.items()]))
            if not form_persona_principal.is_valid():
                messages.error(request, "Hubo un problema con el formulario de persona principal: " + ", ".join([f"{field}: {error}" for field, error in form_persona_principal.errors.items()]))
            if not formset_beneficiario.is_valid():
                messages.error(request, "Hubo un problema con el formset de beneficiarios.")
                for form in formset_beneficiario:
                    if not form.is_valid():
                        messages.error(request, "Detalles: " + ", ".join([f"{field}: {error}" for field, error in form.errors.items()]))
    else:        
        form_poliza = formularios.PolizaForm(instance=poliza)
        form_persona_principal = formularios.PersonaPrincipalForm(instance=persona_principal)

    return render(request, 'asesor/add_poliza.html', {
        'form_poliza': form_poliza,
        'form_persona_principal': form_persona_principal,
        'formset_beneficiario': formset_beneficiario,
        'helper_beneficiario': helper_beneficiario,
        "informacion": "sepomex:asentamiento_details",
        'titulo': titulo
    })