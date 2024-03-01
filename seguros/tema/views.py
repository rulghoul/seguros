from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView

from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required


from tema.models import parametros_colores, parametros_imagenes
# Create your views here.

####### Parametros de colores #########


class add_color(CreateView):
    model = parametros_colores
    success_url = reverse_lazy('list_color')
    fields = ['elemento', 'color']
    template_name = 'catalogos/add.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Nuevo Color"
        context['regresa'] = 'list_color'
        return context

class update_color(UpdateView):
    model = parametros_colores
    fields = ['elemento', 'color']
    success_url = reverse_lazy('list_color')
    template_name = 'catalogos/update.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Actualiza Color"
        context['regresa'] = 'list_color'
        return context


class list_color(ListView):
    model = parametros_colores
    template_name = ('parametros/listColor.html')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        datos = {
            'titulo': "Colores",
            'add':"add_color",
            'add_label':'Nuevo color',
            'update':'update_color',    
            'encabezados': {"elemento":'Elemento',"color":"Color"},
        }
        context.update(datos)
        return context
    


####### Parametros de imagenes #########


class add_imagen(CreateView):
    model = parametros_imagenes
    success_url = reverse_lazy('list_imagen')
    fields = ['title', 'image',]
    template_name = 'parametros/add.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Nueva Imagen"
        context['regresa'] = 'list_imagen'
        return context

class update_imagen(UpdateView):
    model = parametros_imagenes
    fields = ['title', 'image',]
    success_url = reverse_lazy('list_imagen')
    template_name = 'parametros/update.html'
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Actualiza Imagen"
        context['regresa'] = 'list_imagen'
        return context


class list_imagen(ListView):
    model = parametros_imagenes
    template_name = ('parametros/listImagenes.html')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        datos = {
            'titulo': "Parametros Imagenes",
            'add':"add_imagen",
            'add_label':'Nueva imagen',
            'update':'update_imagen',    
            'encabezados': {"title":'Nombre',"image":"Imagen"},
        }
        context.update(datos)
        return context
    


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        super().form_valid(form)
        return redirect('home')


class CustomLogoutView(LogoutView):
    next_page = 'home'

def home_view(request):   
    template = loader.get_template('home.html')
    colores = parametros_colores.objects.all().order_by('elemento').values()
    #graficos = parametros_imagenes.objects.all().order_by('descripcion').values()
    context = {'titulo': "Nueva Actividad", 
               'colores': colores, 
               'imagenes': [], 
               'regresa':'lista_actividad'}
    return HttpResponse(template.render(context, request))

def base_view(request):
    colores = parametros_colores.objects.all().order_by('elemento').values()
    return render(request, 'base.html', {'site_colors': colores})
