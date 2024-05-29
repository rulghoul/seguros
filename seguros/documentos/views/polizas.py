import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views.generic import ListView, UpdateView, CreateView, FormView
from django.contrib import messages #Mensajes
from django.urls import reverse, reverse_lazy

from django.db import transaction
from documentos import models as mod
from documentos import forms as formularios
from django.core.files.base import ContentFile

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
        'titulo': titulo,
        'documento_url': 'documentos:doc_poliza',
        'siniestros_url': 'documentos:siniestros',
        'poliza_id':poliza.pk,
    })

# Archivos de la poliza y Siniestros


POLIZA_DESCRIPCIONES = [
    'Identificacion Oficial',
    'Estado de Cuenta Bancario',
    'Comprobante de Domicilio',
    'Caratula de Póliza',
]

SINIESTRO_DESCRIPCIONES = [
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        self.pk = self.kwargs.get('pk')
        archivos_existentes = {}
        documentos = mod.Documentos.objects.filter(poliza_id=self.pk)
        for documento in documentos:
            archivos_existentes[documento.descripcion] = documento.archivo
        kwargs.update({
            'lista_archivos': POLIZA_DESCRIPCIONES,
            'archivos_existentes': archivos_existentes,
            'retorno': 'documentos:poliza_update',
            'indice': self.pk,
        })
        return kwargs

    def form_valid(self, form):
        for descripcion in POLIZA_DESCRIPCIONES:
            files = self.request.FILES.getlist(descripcion)
            for file in files:
                obj, created = mod.Documentos.objects.update_or_create(
                    poliza_id=self.pk,
                    descripcion=descripcion,                            
                    defaults={'activo': True, 'archivo': file}
                )
                if created:
                    messages.info(self.request, f"Se cargó {descripcion} para la póliza.")
        return redirect(reverse_lazy('documentos:doc_poliza', args=[self.pk]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "titulo": "Documentos Póliza", 
            "redirige": "documentos:update_poliza",
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
        siniestro = mod.Siniestros.objects.get(pk=self.pk)
        self.poliza_pk = siniestro.poliza.pk
        documentos = mod.DocumentosSiniestros.objects.filter(siniestro_id=self.pk)
        for documento in documentos:
            archivos_existentes[documento.descripcion] = documento.archivo
        kwargs.update({
            'lista_archivos': SINIESTRO_DESCRIPCIONES,
            'archivos_existentes': archivos_existentes,
            'retorno': 'documentos:siniestros',
            'indice': self.poliza_pk,
        })
        return kwargs

    def form_valid(self, form):
        for descripcion in SINIESTRO_DESCRIPCIONES:
            files = self.request.FILES.getlist(descripcion)
            for file in files:
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
        context.update({
            "titulo": "Documentos Siniestro", 
            "redirige": f"'documentos:siniestros' { self.poliza_pk }",
        })
        return context


class Siniestro_Add(LoginRequiredMixin, FormView):
    form_class = formularios.SiniestroForm
    template_name = "catalogos/add.html"
    pk = None

    def get_initial(self):
        initial = super().get_initial()
        self.pk = self.kwargs.get('pk')
        initial['poliza'] = self.pk 
        return initial

    def get_success_url(self):
        return reverse_lazy('documentos:list_siniestros', kwargs={"pk": self.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.info(self.request, f"Se intenta recuperar la poliza con el pk {self.pk}")
        context["titulo"] = "Nuevo Siniestro"
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
        messages.info(self.request, f"Form valid: se intenta recuperar la poliza con el pk {self.poliza}")

        return initial 
    
    def get_object(self):
        siniestro_id = self.kwargs.get('pk')
        return get_object_or_404(mod.Siniestros, pk=siniestro_id)

    def get_success_url(self):
        return reverse_lazy('documentos:siniestros', kwargs={"pk": 3})
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Actualiza Siniestro"
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
        poliza = get_object_or_404(mod.Poliza, pk=self.pk)
        context["titulo"] = "Siniestros"
        context["poliza"] = poliza
        context["cliente"] = poliza.persona_principal
        context["add"] = 'documentos:siniestro_add'
        context["add_label"] = "Nuevo Siniestro"
        context["update"] = "documentos:siniestro_update"
        context["upload"] = "documentos:doc_siniestros"
        context["poliza_id"] = self.pk
        return context