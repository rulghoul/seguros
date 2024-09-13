import logging
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, CreateView, FormView, DeleteView
from django.contrib import messages #Mensajes
from django.urls import reverse, reverse_lazy

from django.db import transaction
from documentos import models as mod
from documentos import forms as formularios

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

from django.conf import settings
from documentos.utils.encript_files import desencripta_archivo, encripta_archivo

import magic #Obtine el mime type del archivo
from django.http import FileResponse #Devuelve archivos
#filtros y tablas
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from . import filters_tables as tables


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
        context["titulo"] = "Base de datos de Clientes"
        context["add"] = "documentos:poliza_add"
        context["add_label"] = "Nuevo Cliente"
        context["update"] = "documentos:poliza_update"
        context["borra"] = "documentos:poliza_update"
        return context


class polizas_cliente(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = mod.Poliza
    template_name = 'asesor/polizas_cliente.html'
    context_object_name = 'polizas'
    table_class = tables.PolizaTable
    filterset_class = tables.PolizaFilter

    def get_queryset(self):
        cliente_pk =  self.kwargs.get('pk')
        try:       
            return mod.Poliza.objects.filter(persona_principal=cliente_pk).prefetch_related('persona_principal')
        except: 
            return mod.Poliza.objects.none()
            
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

            
    def get_context_data(self, **kwargs):
            #Borra las variables de origen de documentos y siniestros
        if 'origin' in self.request.session:
            del self.request.session['origin']
        if 'siniestros_origen' in self.request.session:
            del self.request.session['siniestros_origen']
        cliente_pk =  self.kwargs.get('pk')
        cliente = mod.PersonaPrincipal.objects.get(pk=cliente_pk)
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Polizas de: "
        context["add"] = "documentos:poliza_cliente_add"
        context["add_label"] = "Nueva Poliza"
        context["update"] = "documentos:poliza_cliente_update"
        context["borra"] = "documentos:poliza_delete"
        context["cliente_pk"] = cliente_pk
        context["cliente"] = cliente

        context['documento_url'] = 'documentos:doc_poliza'
        context['siniestros_url'] = 'documentos:siniestros'
        context['recordatorio_url'] = 'documentos:recordatorio'

        return context
            
    
class borrar_poliza(LoginRequiredMixin, DeleteView):
    model = mod.Poliza
    template_name = "catalogos/borrar.html"

    def get_success_url(self):
        cliente_pk = self.kwargs.get('pk')
        return reverse_lazy('documentos:polizas_cliente', kwargs={'cliente': cliente_pk})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente_pk =  self.kwargs.get('pk')
        context['titulo'] = "Borrar Cliente"
        context['redirige'] = "documentos:polizas_cliente"
        context["cliente"] = cliente_pk
        return context

@login_required
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

        # Valida si el formulario principal y los beneficiarios son correctos
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
                messages.success(request, "Se actualizo la Póliza con beneficiarios.")                
                return redirect('documentos:poliza_update', pk=poliza.pk)  # Redirige a una lista o alguna URL definida
            else:
                messages.error(request, "La suma de los porcentajes de participación de los beneficiarios debe ser exactamente 100%.")  
        
        # Si solo el formulario principal es correcto, pero no el de beneficiarios
        if form_poliza.is_valid() and form_persona_principal.is_valid():

            persona_principal = form_persona_principal.save()  # Guarda la persona principal
            poliza = form_poliza.save(commit=False)  # Prepara la póliza para guardar
            poliza.persona_principal = persona_principal  # Vincula la persona principal a la póliza
            poliza.save()  
            messages.success(request, "Póliza guardada con éxito. Sin beneficiarios")
            return redirect('documentos:poliza_update', pk=poliza.pk)
        # si fallan los dos formularios
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
        'titulo': titulo,
        'documento_url': 'documentos:doc_poliza',
        'siniestros_url': 'documentos:siniestros',
        'poliza_id':poliza.pk,
    })

   
@login_required
@transaction.atomic
def edit_poliza_cliente(request, cliente = None, pk=None):
    cliente_object = get_object_or_404(mod.PersonaPrincipal, pk=cliente)

    #Borra las variables de origen de documentos y siniestros
    if 'origin' in request.session:
        del request.session['origin']
    if 'siniestros_origen' in request.session:
        del request.session['siniestros_origen']

    if pk:
        poliza = get_object_or_404(mod.Poliza, pk=pk)
        titulo = f"Editar Poliza "
        persona_principal = poliza.persona_principal        
    else:
        poliza = mod.Poliza()
        persona_principal = mod.PersonaPrincipal.objects.get(pk=cliente)
        titulo = f"Nueva Poliza"
        poliza.asesor_poliza = persona_principal.asesor_cliente        
        poliza.persona_principal = persona_principal

    helper_beneficiario = formularios.BeneficiariosHelper
    formset_beneficiario = formularios.BeneficiariosFormset(request.POST or None, instance=poliza)

    if request.method == 'POST':
        #messages.success(request, "Se entro al post")
        form_poliza = formularios.PolizaForm(request.POST or None, instance=poliza)

        if form_poliza.is_valid() and formset_beneficiario.is_valid():
            
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
                poliza = form_poliza.save(commit=False)  # Prepara la póliza para guardar
                poliza.persona_principal = persona_principal  # Vincula la persona principal a la póliza
                poliza.save()  # Guarda la póliza
                formset_beneficiario.save()
                messages.success(request, "Póliza guardada con éxito.")                
                return redirect('documentos:poliza_cliente_update', pk=poliza.pk, cliente=cliente)
            else:           
                poliza = form_poliza.save(commit=False)  
                poliza.save()  
                messages.error(request, "La suma de los porcentajes de participación de los beneficiarios debe ser exactamente 100%.")  
        
        if form_poliza.is_valid():            
            poliza = form_poliza.save(commit=False)  
            poliza.save()  
            messages.success(request, "Póliza guardada con éxito. Sin Beneficiario")
            #return redirect('documentos:poliza_cliente_update', pk=poliza.pk, cliente=cliente)

        
        else:
            if not form_poliza.is_valid():
                messages.error(request, "Hubo un problema con el formulario de la póliza: " + ", ".join([f"{field}: {error}" for field, error in form_poliza.errors.items()]))            
            if not formset_beneficiario.is_valid():
                messages.error(request, "Hubo un problema con el formset de beneficiarios.")
                for form in formset_beneficiario:
                    if not form.is_valid():
                        messages.error(request, "Detalles: " + ", ".join([f"{field}: {error}" for field, error in form.errors.items()]))
    else:        
        form_poliza = formularios.PolizaForm(instance=poliza)        

    return render(request, 'asesor/edit_poliza.html', {
        'form_poliza': form_poliza,
        'persona_principal': persona_principal,
        'formset_beneficiario': formset_beneficiario,
        'helper_beneficiario': helper_beneficiario,
        "informacion": "sepomex:asentamiento_details",
        'titulo': titulo,
        'documento_url': 'documentos:doc_poliza',
        'siniestros_url': 'documentos:siniestros',
        'poliza_id':poliza.pk,
        'cliente':cliente_object,
        'poliza': poliza,
    })

# Archivos de la poliza y Siniestros


POLIZA_DESCRIPCIONES = [
    'Identificacion Oficial',
    'Estado de Cuenta Bancario',
    'Comprobante de Domicilio',
    'Caratula de Póliza',
]

SINIESTRO_DESCRIPCIONES = [
    'Identificacion del cliente',
    'Informe Médico',
    'Interpretación de Estudios',
    'Cotización de Material Extra a la Cirugía',
    'Aviso de Accidente',
    'Carta de Autorización de Pago Directo',
    'Carta de Autorización de Honorarios',
    'Carta de Invalidez Total y Permanente',
    'Carta de Aseguradora por Fallecimiento',
]


class upload_documentos_poliza(LoginRequiredMixin, FormView):
    template_name = 'poliza/archivos_poliza.html'
    form_class = formularios.MultiDocumentUploadForm
    pk = None
    poliza = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.pk = self.kwargs.get('pk')
        self.poliza = mod.Poliza.objects.get(pk= self.pk)
        archivos_existentes = {}
        archivos_adicionales = {}
        documentos = mod.Documentos.objects.filter(poliza_id=self.pk)
        for documento in documentos:
            if documento.descripcion in POLIZA_DESCRIPCIONES:
                archivos_existentes[documento.descripcion] = documento.archivo                
            else:
                archivos_adicionales[documento.descripcion] = documento.archivo
        
        kwargs.update({
            'lista_archivos': POLIZA_DESCRIPCIONES,
            'archivos_existentes': archivos_existentes,
            'archivos_adicionales': archivos_adicionales,
            'modelo': "Documentos",
        })
        return kwargs

    def form_valid(self, form):
        messages.info(self.request, self.request.FILES.getlist)
        #files = self.request.FILES.getlist('file_field_name') 
        for descripcion, file in self.request.FILES.items():

            # Validar tipo de archivo
            if file.content_type not in settings.ALLOWED_FILE_TYPES:
                messages.error(self.request, f"El archivo {file.name} no es de un tipo permitido.")                
                continue
                
            # Validar tamaño de archivo
            if file.size > int(settings.MAX_FILE_SIZE_MB) * 1024 * 1024:
                messages.error(self.request, f"El archivo {file.name} supera el tamaño máximo permitido de {settings.MAX_FILE_SIZE_MB} MB.")                
                continue

            obj, created = mod.Documentos.objects.update_or_create(
                    poliza_id=self.pk,
                    descripcion=descripcion,                            
                    defaults={'activo': True, 'archivo': file}
                )
            
            if created:
                    messages.info(self.request, f"Se cargó {descripcion} para la póliza.")

        return redirect(reverse_lazy('documentos:doc_poliza', args=[self.pk]))

    def get_context_data(self, **kwargs):
        # Comprueba si hay un 'origin' en la sesión, si no, obtén de GET
        if 'origin' not in self.request.session:
            origin = self.request.GET.get('origin')
            if origin:
                self.request.session['origin'] = origin
            else:
                self.request.session['origin'] = reverse('documentos:clientes')
        elif self.request.session['origin'] == reverse('documentos:clientes'):
            origin = self.request.GET.get('origin')
            if origin:
                self.request.session['origin'] = origin
            else:
                self.request.session['origin'] = reverse('documentos:clientes')


        context = super().get_context_data(**kwargs)
        context.update({
            "titulo": f"Documentos:",
            "poliza":  self.poliza , 
            "redirige": "documentos:poliza_cliente_update",
            "origin": self.request.session['origin'],
        })
        return context


class upload_documentos_siniestro(LoginRequiredMixin, FormView):
    template_name = 'poliza/archivos_siniestros.html'
    form_class = formularios.MultiDocumentUploadForm
    pk = None
    poliza_pk = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.pk = self.kwargs.get('pk')
        archivos_existentes = {}
        archivos_adicionales = {}
        siniestro = mod.Siniestros.objects.get(pk=self.pk)
        self.poliza_pk = siniestro.poliza.pk
        documentos = mod.DocumentosSiniestros.objects.filter(siniestro_id=self.pk)

        for documento in documentos:
            if documento.descripcion in SINIESTRO_DESCRIPCIONES:
                archivos_existentes[documento.descripcion] = documento.archivo                
            else:
                archivos_adicionales[documento.descripcion] = documento.archivo
                
        kwargs.update({
            'lista_archivos': SINIESTRO_DESCRIPCIONES,
            'archivos_existentes': archivos_existentes,
            'archivos_adicionales': archivos_adicionales,
            'modelo': "DocumentosSiniestros",
        })
        return kwargs

    def form_valid(self, form):
        #messages.info(self.request, self.request.FILES.getlist)
        #archivos_invalidos = False
        for descripcion, file in self.request.FILES.items():
            # Validar tipo de archivo
            if file.content_type not in settings.ALLOWED_FILE_TYPES:
                messages.error(self.request, f"El archivo {file.name} no es de un tipo permitido.")
                archivos_invalidos = True
                continue
                
            # Validar tamaño de archivo
            if file.size > int(settings.MAX_FILE_SIZE_MB) * 1024 * 1024:
                messages.error(self.request, f"El archivo {file.name} supera el tamaño máximo permitido de {settings.MAX_FILE_SIZE_MB} MB.")
                archivos_invalidos = True
                continue

            obj, created = mod.DocumentosSiniestros.objects.update_or_create(
                siniestro_id=self.pk,
                descripcion=descripcion,                            
                defaults={'activo': True, 'archivo': file}
                )
            if created:
                messages.info(self.request, f"Se cargó {descripcion} para la póliza.")
        

        return redirect(reverse_lazy('documentos:doc_siniestros', args=[self.pk]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'origin' not in self.request.session:
            origin = self.request.GET.get('origin')
            if origin:
                self.request.session['origin'] = origin
            else:
                self.request.session['origin'] = reverse('documentos:clientes')
        elif self.request.session['origin'] == reverse('documentos:clientes'):
            origin = self.request.GET.get('origin')
            if origin:
                self.request.session['origin'] = origin
            else:
                self.request.session['origin'] = reverse('documentos:clientes')

        poliza = mod.Poliza.objects.get(pk=self.poliza_pk)
        context.update({
            "titulo": f"Documentos Siniestro:", 
            "poliza": poliza,
            "origin": self.request.session['origin'],
            "redirige": f"'documentos:siniestros' { self.poliza_pk }",
        })
        return context


class Siniestro_Add(LoginRequiredMixin, FormView):
    form_class = formularios.SiniestroForm
    template_name = "poliza/add_siniestro.html"
    pk = None

    def get_initial(self):
        initial = super().get_initial()
        self.pk = self.kwargs.get('pk')
        initial['poliza'] = self.pk 
        return initial

    def get_success_url(self):
        return reverse_lazy('documentos:siniestros', kwargs={"pk": self.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #messages.info(self.request, f"Se intenta recuperar la poliza con el pk {self.pk}")

        if 'origin' not in self.request.session:
            origin = self.request.GET.get('origin')
            if origin:
                self.request.session['origin'] = origin
            else:
                self.request.session['origin'] = reverse('documentos:clientes')
        elif self.request.session['origin'] == reverse('documentos:clientes'):
            origin = self.request.GET.get('origin')
            if origin:
                self.request.session['origin'] = origin
            else:
                self.request.session['origin'] = reverse('documentos:clientes')

        poliza = get_object_or_404(mod.Poliza, pk=self.pk)
        context["titulo"] = f"Nuevo Siniestro para la poliza:"
        context["poliza"] = poliza
        context["origin"] = self.request.session['origin']
        context["redirige"] = reverse_lazy('documentos:list_siniestros', kwargs={"pk": self.pk})
        return context

    def form_valid(self, form):
        messages.info(self.request, f"Form valid: se intenta recuperar la poliza con el pk {self.pk}")
        poliza = get_object_or_404(mod.Poliza, pk=self.pk)
        form.instance.poliza = poliza
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "El formulario es inválido. Revisa los datos ingresados.")
        return self.render_to_response(self.get_context_data(form=form))

class Siniestro_Update(LoginRequiredMixin, UpdateView):
    form_class = formularios.SiniestroForm
    template_name = "catalogos/add.html"
    poliza = None   

    def get_initial(self):
        initial = super().get_initial()     
        siniestro = self.get_object()
        self.poliza = siniestro.poliza
        self.pk = siniestro.poliza.pk 
        #messages.info(self.request, f"Form valid: se intenta recuperar la poliza con el pk {self.poliza}")

        return initial 
    
    def get_object(self):
        siniestro_id = self.kwargs.get('pk')
        return get_object_or_404(mod.Siniestros, pk=siniestro_id)

    def get_success_url(self):
        return reverse_lazy('documentos:siniestros', kwargs={"pk": self.pk})
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'origin' not in self.request.session:
            origin = self.request.GET.get('origin')
            if origin:
                self.request.session['origin'] = origin
            else:
                self.request.session['origin'] = reverse('documentos:clientes')
        elif self.request.session['origin'] == reverse('documentos:clientes'):
            origin = self.request.GET.get('origin')
            if origin:
                self.request.session['origin'] = origin
            else:
                self.request.session['origin'] = reverse('documentos:clientes')

        context["titulo"] = "Actualiza Siniestro"
        context["origin"] = self.request.session['origin']
        context["redirige"] = "documentos:siniestros"
        return context

class Siniestro_List(LoginRequiredMixin, ListView):
    model = mod.Siniestros
    template_name = 'asesor/siniestros.html'
    context_object_name = 'siniestros'
    pk = None

    def get_queryset(self):        
        self.pk = self.kwargs.get('pk')
        try:
            poliza = mod.Poliza.objects.get(pk=self.pk)        
            return mod.Siniestros.objects.filter(poliza=poliza)
        except mod.Poliza.DoesNotExist:
            return mod.Poliza.objects.none()
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #Borra las variables de origen de documentos y siniestros
        if 'origin' in self.request.session:
            del self.request.session['origin']

        if 'siniestros_origen' not in self.request.session:
            origin = self.request.GET.get('origin')
            if origin:
                self.request.session['siniestros_origen'] = origin
            else:
                self.request.session['siniestros_origen'] = reverse('documentos:clientes')
        elif self.request.session['siniestros_origen'] == reverse('documentos:clientes'):
            origin = self.request.GET.get('siniestros_origen')
            if origin:
                self.request.session['siniestros_origen'] = origin
            else:
                self.request.session['siniestros_origen'] = reverse('documentos:clientes')

        poliza = get_object_or_404(mod.Poliza, pk=self.pk)
        context["titulo"] = "Siniestros"
        context["poliza"] = poliza
        context["cliente"] = poliza.persona_principal.pk
        context["origin"] = self.request.session['siniestros_origen']
        context["add"] = 'documentos:siniestro_add'
        context["add_label"] = "Nuevo Siniestro"
        context["update"] = "documentos:siniestro_update"
        context["upload"] = "documentos:doc_siniestros"
        context["poliza_id"] = self.pk
        return context

@login_required
def servir_archivo_encriptado(request, pk, modelo, modo):
    if modelo == 'Documentos':
        documento = get_object_or_404(mod.Documentos, pk=pk)
    elif modelo == 'DocumentosSiniestros':
        documento = get_object_or_404(mod.DocumentosSiniestros, pk=pk)
    else:
        raise Http404("Modelo no soportado.")   
    
    try:
        print(type(documento.archivo))
        desencriptado = desencripta_archivo(documento.archivo)
        # Usar python-magic para detectar el tipo de contenido
        mime = magic.Magic(mime=True)
        content_type = mime.from_buffer(desencriptado.read(1024))

        response = FileResponse(desencriptado.open(), content_type=content_type, filename=desencriptado.name, as_attachment=bool(modo))
        #response = HttpResponse(desencriptado.read(), content_type='application/octet-stream')
        #response['Content-Disposition'] = f'inline; filename="{desencriptado.name}"'
        return response
    except Exception as e:
        raise Http404(f"No se puede desencriptar el archivo o el archivo no existe.<br> {e}")
    
@login_required
def borrar_archivo(request, pk, modelo):
    if modelo == 'Documentos':
        documento = get_object_or_404(mod.Documentos, pk=pk)
    elif modelo == 'DocumentosSiniestros':
        documento = get_object_or_404(mod.DocumentosSiniestros, pk=pk)
    else:
        raise Http404("Modelo no soportado.")   
    
    if request.method == "POST":
        try:
            documento.archivo.delete()  # Elimina el archivo del sistema de archivos
            documento.delete()  # Elimina el registro de la base de datos
            next = request.POST.get('next', '/')
            return redirect(next)
        except Exception as e:
            raise Http404(f"No se pudo borrar el archivo.<br> {e}")
            #return render(request, 'poliza/borrar_archivo.html', {'error': f"No se pudo eliminar el archivo: {e}"})
    

    return render(request, 'poliza/borrar_archivo.html', {'documento': documento, 'modelo': modelo, 'request': request })
    
