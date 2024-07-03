import logging


from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views.generic.edit import  UpdateView, FormView, DeleteView, CreateView
from django.views.generic import ListView

from documentos import models as mod
from documentos import forms as formularios
from django.shortcuts import render, redirect
from django.contrib import messages 
from django.urls import reverse_lazy

from django.db import transaction
from django.contrib.auth.models import User
from django.http import JsonResponse

from .generic_view import BaseListView


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


class PersonaPrincipalAdd(LoginRequiredMixin,CreateView):
    model = mod.PersonaPrincipal
    template_name = "catalogos/add_cliente.html"
    form_class = formularios.PersonaPrincipalForm

    def get_success_url(self):
        return reverse_lazy("documentos:cliente_update", kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.info(self.request,"Entra en validacion")
        try:
            asesor_instance = mod.Asesor.objects.get(usuario=self.request.user)
            form.instance.asesor = asesor_instance
            messages.info(self.request,"Encontró al asesor")
        except mod.Asesor.DoesNotExist:
            messages.info(self.request,"No encontró al asesor")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Agregar Cliente"
        context["redirige"] = "documentos:clientes"
        context["informacion"] = "sepomex:asentamiento_details"
        return context
    
class PersonaPrincipalUpdate(LoginRequiredMixin,UpdateView):
    model = mod.PersonaPrincipal
    template_name = "catalogos/add_cliente.html"
    form_class = formularios.PersonaPrincipalForm

    def get_success_url(self):
        return reverse_lazy("documentos:cliente_update", kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        if mod.Asesor.objects.filter(usuario = self.request.user).exists():
            form.instance.asesor = mod.Asesor.objects.filter(usuario = self.request.user)  
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Actualizar Cliente"
        context["redirige"] = "documentos:clientes"
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

class borrar_cliente(LoginRequiredMixin, DeleteView):
    model = mod.PersonaPrincipal
    template_name = "catalogos/borrar.html"
    success_url = reverse_lazy('documentos:clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Borrar Cliente"
        context['redirige'] = "documentos:clientes"
        return context


class ListCliente(LoginRequiredMixin,ListView):
    template_name = "catalogos/list_cliente.html"
    model = mod.PersonaPrincipal
    paginate_by = 100

    def get_queryset(self):
        user = self.request.user
        if mod.Asesor.objects.filter(usuario=user).exists():
            return mod.PersonaPrincipal.objects.filter(asesor_cliente=mod.Asesor.objects.get(usuario=user))
        
        elif user.is_staff:
            return mod.PersonaPrincipal.objects.all()
        
        return mod.PersonaPrincipal.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Clientes"
        context["encabezados"] = ('Nombre', 'Correo', 'Telefono', "Asesor")
        context["add"] = "documentos:cliente_add"
        context["add_label"] = "Nuevo Cliente"
        context["update"] = "documentos:cliente_update"
        context["borra"] = "documentos:borra_cliente"
        return context
    

@login_required
def buscar_cliente_por_curp(request):
    curp = request.GET.get('curp', None)
    if curp:
        try:
            asesor = mod.Asesor.objects.get(usuario = request.user)
            messages.info(request, f"Asesor encontrado {asesor}")
            persona = mod.PersonaPrincipal.objects.get(curp=curp, asesor_cliente=asesor.pk)
            messages.info(request, f"Persona encontrada: {persona}")
            data = {
                'nombre': persona.nombre,
                'primer_apellido': persona.primer_apellido,
                'segundo_apellido': persona.segundo_apellido,
                'genero': persona.genero,
                'estatus_persona': persona.estatus_persona,
                'lugar_nacimiento': persona.lugar_nacimiento,
                'fecha_nacimiento': persona.fecha_nacimiento,
                # Direccion
                'asentamiento': persona.asentamiento.nombre,
                'municipio': persona.asentamiento.municipio.nombre,
                'estado': persona.asentamiento.municipio.estado.nombre,
                'codigo_postal': persona.asentamiento.codigo_postal,

                'calle': persona.calle,
                'numero': persona.numero,
                'numero_interior': persona.numero_interior,
                # Contacto
                'correo': persona.correo,
                'telefono': persona.telefono,
            }
            return JsonResponse({'status': 'ok', 'data': data})
        except mod.PersonaPrincipal.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'No se encontró una persona con ese CURP'})
        except mod.Asesor.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'No se encontro el Asesor'})
        except Exception as inst:
            return JsonResponse({'status': 'error', 'message': f'Fallo no identificado: {inst}'})
        
    return JsonResponse({'status': 'error', 'message': 'CURP no proporcionado'})

#Asesores

@staff_member_required 
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

class borrar_asesor(LoginRequiredMixin, DeleteView):
    model = mod.Asesor
    template_name = "catalogos/borrar.html"
    success_url = reverse_lazy('documentos:asesor_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Borrar Asesor"
        context['redirige'] = "documentos:asesor_list"
        return context


@method_decorator(staff_member_required, name="dispatch")
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
        context["borra"] = "documentos:asesor_delete"
        return context
    