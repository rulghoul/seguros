import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views.generic import ListView
from django.contrib import messages #Mensajes
from django.urls import reverse

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
        'titulo': titulo
    })

# Archivos de la poliza y Siniestros

POLIZA_DESCRIPCIONES = [
    'Documento Poliza 1',
    'Documento Poliza 2',
    'Documento Poliza 3',
    'Documento Poliza 4',
    'Documento Poliza 5',
    'Documento Poliza 6',
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
                    obj, created = mod.Documentos.objects.update_or_create(
                            poliza_id=pk,
                            descripcion=descripcion,                            
                            defaults={'activo': True, 'archivo': file}
                    )
                    if created:
                        messages.info(request, f"Se cargo {descripcion} para la poliza ")
            return redirect(reverse('documentos:doc_poliza', args=[pk])) 
    else:
        archivos_existentes = {}
        documentos = mod.Documentos.objects.filter(poliza_id=pk)
        for documento in documentos:
            archivos_existentes[documento.descripcion] = documento.archivo
        form = formularios.MultiDocumentUploadForm(POLIZA_DESCRIPCIONES, archivos_existentes=archivos_existentes)
    
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
                        archivo=ContentFile(file)
                    )
            return redirect(reverse('documentos:update_siniestro', args=[pk]))  
    else:
        form = formularios.MultiDocumentUploadForm(SINIESTRO_DESCRIPCIONES)

    contexto = {'form': form,
                "titulo": "Documentos del Siniestro", 
                "redirige":"documentos:update_poliza",
                "lista": mod.Siniestros.objects().filter(poliza=siniestro.poliza)
                }
    return render(request, 'poliza/archivos_siniestro.html', contexto)