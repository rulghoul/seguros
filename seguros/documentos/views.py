from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.views import View
from . import models as mod
from . import forms as formularios

######################### Catalogos ###########################


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
                    #form = self.form_class(post_data)
                    form = self.form_class()
                else:
                    print(f"Se entro el id = {pk}")
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

class TipoConductoPagoView(BaseListView):
    form_class = formularios.TipoConductoPagoForm
    model = mod.TipoConductoPago
    template_name = 'catalogos/list.html'
    redirige = 'lista_tipo_conducto_pago'
    context_object_name = 'lista'
    title = ' Tipo De Conducto Pago'
    encabezados = ['CLAVE', 'DESCRIPCION', 'ACTIVO']
    campos = ['clave', 'descripcion', 'activo']






class lista_tipo_conducto_pago(ListView):
    model = mod.TipoConductoPago
    template_name  = 'catalogos/list.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        datos = {
            'titulo': "Tipo Conducto Pago",
            'add':"add_tipo_conducto",
            'add_label':'Nuevo Tipo Conducto',
            'update':'update_tipo_conducto',  
            'detalle':'detalle_tipo_conducto',
            'borra':'borra_tipo_conducto',
            'encabezados': {"clave":"CLAVE","descripcion":"DESCRIPCION", "activo":"ACTIVO"},
        }
        context.update(datos)
        return context    
    

class add_tipo_conducto_pago(CreateView):
    model = mod.TipoConductoPago
    success_url = reverse_lazy('lista_tipo_conducto_pago')
    fields = ['clave', 'descripcion', 'activo']
    template_name = 'catalogos/add.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Nuevo Tipo Conducto Pago"
        context['regresa'] = 'lista_tipo_conducto_pago'
        return context

class update_canal(UpdateView):
    model = mod.TipoConductoPago
    fields = ['clave', 'descripcion', 'activo']
    success_url = reverse_lazy('lista_tipo_conducto_pagos')
    template_name = 'catalogos/update.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Actualiza Tipo Conducto Pago"
        context['regresa'] = 'lista_tipo_conducto_pago'
        return context
    
class detalle_canal(DetailView):
    model = mod.TipoConductoPago
    template_name = 'catalogos/detalle.html'
    success_url = reverse_lazy('lista_tipo_conducto_pago')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Detalle Tipo Conducto Pago"
        context['regresa'] = 'lista_tipo_conducto_pago'
        return context   


class borra_canal(DeleteView):
    model = mod.TipoConductoPago
    template_name = 'catalogos/borrar.html'
    success_url = reverse_lazy('lista_tipo_conducto_pago')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Borrar Tipo Conducto Pago"
        context['regresa'] = 'lista_tipo_conducto_pago'
        return context   