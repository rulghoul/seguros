import logging
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages #Mensajes
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse

from . import models as mod
from . import forms as formularios
from .utils.send_email_new_asesor import envia_correo_new_asesor as envia 

######################### Vista Base ###########################


class BaseListView(View):
    form_class = None
    model = None
    lista_objetos = None
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
        context = self.get_context_data(post_data=request.POST, files=request.FILES, peticion=request)
        return render(request, self.template_name, context)

    def get_context_data(self, post_data=None, files=None, peticion= None):
        context = {}
        if post_data:
            if 'save' in post_data:
                print(f"Se entro en SAVE")
                pk = post_data.get('save')
                if not pk:
                    form = self.form_class(post_data, files)
                    if form.is_valid():
                        form.save()
                        form = self.form_class()
                        return redirect(self.redirige)
                    #form = self.form_class()
                else:
                    print(f"Se entro el id = {pk}")
                    objeto = self.model.objects.get(id=pk)
                    form = self.form_class(post_data, files, instance=objeto)
                    if form.is_valid():
                        form.save()
                        return redirect(self.redirige)
                    else:
                        messages.warning(peticion, f"Fallo el guardado por: {form.errors}")
                
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

        context['lista'] = self.lista_objetos if self.lista_objetos is not None else self.model.objects.all()
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
    

class Poliza_List(LoginRequiredMixin, ListView):
    model = mod.Poliza
    template_name = 'asesor/polizas.html'
    context_object_name = 'polizas'

    def get_queryset(self):
        user = self.request.user
        try:
            asesor = mod.Asesor.objects.get(usuario=user)        
            return mod.Poliza.objects.filter(asesor_poliza=asesor)
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
        #messages.info(request, f"Se encontró al asesor {asesor_instance.usuario}")
    except mod.Asesor.DoesNotExist:
        if pk is None:
            messages.warning(request, "No encontró al asesor")
            asesor_instance = None

    if pk:
        poliza = get_object_or_404(mod.Poliza, pk=pk)
        titulo = f"Editar Poliza: {poliza.numero_poliza}"
        persona_principal = poliza.persona_principal  # Acceder a la persona principal existente
        asesor_instance = poliza.asesor_poliza
    else:
        poliza = mod.Poliza()
        persona_principal = mod.PersonaPrincipal()
        titulo = f"Nueva Poliza"
        poliza.asesor_poliza = asesor_instance
        persona_principal.asesor_cliente = asesor_instance
        poliza.persona_principal = persona_principal
    

    helper_beneficiario = formularios.BeneficiariosHelper
    formset_beneficiario = formularios.BeneficiariosFormset(request.POST or None, instance=poliza)

    if request.method == 'POST':
        #messages.success(request, "Se entro al post")
        form_poliza = formularios.PolizaForm(request.POST or None, instance=poliza)        
        form_persona_principal = formularios.PersonaPrincipalForm(request.POST or None, instance=poliza.persona_principal)                        

        if form_poliza.is_valid() and form_persona_principal.is_valid() and formset_beneficiario.is_valid():
            
            try:
                total_porcentaje = 0
                for form in formset_beneficiario:
                    total_porcentaje += form.cleaned_data.get('porcentaje_participacion', 0)
                    #messages.info(request, f"Porcentaje {form.cleaned_data['porcentaje_participacion']}  para un total de {total_porcentaje}")
                #total_porcentaje = sum(form.cleaned_data['porcentaje_participacion'] for form in formset_beneficiario)
            except Exception as e:
                messages.error(request, f"Fallo el calculo de porcentaje, favor de revisar las cantidades")
                total_porcentaje = 0
            #messages.success(request, f"Los formularios son validos y el porcentaje es {total_porcentaje}")
            if total_porcentaje == 100:
                persona_principal = form_persona_principal.save()  # Guarda la persona principal
                poliza = form_poliza.save(commit=False)  # Prepara la póliza para guardar
                poliza.persona_principal = persona_principal  # Vincula la persona principal a la póliza
                poliza.save()  # Guarda la póliza
                formset_beneficiario.save()
                messages.success(request, "Póliza guardada con éxito.")
                return redirect('documentos:polizas')  # Redirige a una lista o alguna URL definida
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

# Archivos de la poliza y Siniestros

POLIZA_DESCRIPCIONES = [
    'Documento 1',
    'Documento 2',
    'Documento 3',
]

SINIESTRO_DESCRIPCIONES = [
    'Documento Siniestro 1',
    'Documento Siniestro 2',
    'Documento Siniestro 3',
]



def upload_documentos_poliza(request, pk=None):
    if request.method == 'POST':
        form = formularios.MultiDocumentUploadForm(POLIZA_DESCRIPCIONES, request.POST, request.FILES)
        if form.is_valid():
            for descripcion in POLIZA_DESCRIPCIONES:
                files = request.FILES.getlist(descripcion)
                for file in files:
                    mod.Documentos.objects.create(
                        poliza_id=pk,
                        descripcion=descripcion,
                        activo=True,
                        file=file
                    )
            return redirect(reverse('documentos:update_poliza', args=[form.id])) 
    else:
        form = formularios.MultiDocumentUploadForm(POLIZA_DESCRIPCIONES)
    
    contexto = {'form': form,
                "titulo": "Documentos Poliza", 
                "redirige":"documentos:update_poliza",
                }
    return render(request, 'poliza/archivos_poliza.html', contexto)

def upload_documentos_siniestro(request, pk=None):
    if(pk is None):
        siniestro = get_object_or_404(mod.Siniestros, pk=pk)
    else:
        siniestro = mod.Siniestros()

    if request.method == 'POST':
        form = formularios.MultiDocumentUploadForm(SINIESTRO_DESCRIPCIONES, request.POST, request.FILES)
        if form.is_valid():
            for descripcion in SINIESTRO_DESCRIPCIONES:
                files = request.FILES.getlist(descripcion)
                for file in files:
                    mod.DocumentosSiniestros.objects.create(
                        siniestro=siniestro,
                        descripcion=descripcion,
                        activo=True,
                        file=file
                    )
            return redirect(reverse('documentos:update_siniestro', args=[form.id]))  
    else:
        form = formularios.MultiDocumentUploadForm(SINIESTRO_DESCRIPCIONES)

    contexto = {'form': form,
                "titulo": "Documentos del Siniestro", 
                "redirige":"documentos:update_poliza",
                "lista": mod.Siniestros.objects().filter(poliza=siniestro.poliza)
                }
    return render(request, 'poliza/archivos_siniestro.html', contexto)