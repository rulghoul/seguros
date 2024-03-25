from django import forms
from django_select2 import forms as s2forms
from django.forms import inlineformset_factory, BaseFormSet, formset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, HTML, Submit, Row, Field, Button
from crispy_bootstrap5.bootstrap5 import BS5Accordion

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from . import models as modelos
from sepomex import models as sepomex
from collections import OrderedDict

from django.db import transaction


##class PuntoCaracteristicasForm(forms.ModelForm):
##    class Meta:
##        model = modelos.PuntoCaracteristicas
##        fields = ('desccaracteristicas', )

##PuntoCaracteristicasFormSet = inlineformset_factory(
##    modelos.PuntoAcupuntura, modelos.PuntoCaracteristicas, form=PuntoCaracteristicasForm,
##    extra=0, min_num=1, max_num=1, can_delete=True, can_delete_extra=True
##)

class BootstrapCheckboxInput(forms.CheckboxInput):
    template_name = 'django/forms/widgets/checkbox.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['class'] = 'form-check-input'
        return context

class TipoConductoPagoForm(forms.ModelForm):
    class Meta:
        model = modelos.TipoConductoPago
        fields = ('clave', 'descripcion', 'activo' )

class TipoPersonaForm(forms.ModelForm):
    class Meta:
        model = modelos.TipoPersona
        fields = ('clave', 'descripcion', 'activo' )

class FormaPagoForm(forms.ModelForm):
    class Meta:
        model = modelos.FormaPago
        fields = ('clave', 'descripcion', 'activo' )

class DocumentosForm(forms.ModelForm):
    class Meta:
        model = modelos.Documentos
        fields = ('clave', 'descripcion', 'activo' )

class TipoMediocontactoForm(forms.ModelForm):
    class Meta:
        model = modelos.TipoMediocontacto
        fields = ('descripcion', 'activo' )

class ParentescoForm(forms.ModelForm):
    class Meta:
        model = modelos.Parentesco
        fields = ('descripcion', 'activo' )

class EmpresaContratanteForm(forms.ModelForm):
    class Meta:
        model = modelos.EmpresaContratante
        fields = ('clave', 'nombre', 'logo_small', 'pleca', 'activo', )

class PlanesForm(forms.ModelForm):
    class Meta:
        model = modelos.Planes
        fields = ('clave', 'nombre', 'empresa',  'activo',)


class MunicipioWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "username__icontains",
        "email__icontains",
    ]


class AsentamientoWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "username__icontains",
        "email__icontains",
    ]


class PersonaPrincipalForm(forms.ModelForm):  
    estado = forms.ModelChoiceField(queryset=sepomex.Estado.objects.all(),                                    
        widget=s2forms.ModelSelect2Widget(
            model=sepomex.Estado,
            search_fields=['nombre__icontains'],
            attrs={
                "data-minimum-input-length": 4,
            }
    ))
    municipio = forms.ModelChoiceField(queryset=sepomex.Municipio.objects.all(),                                    
            widget=s2forms.ModelSelect2Widget(
                model=sepomex.Municipio,
                search_fields=['nombre__icontains'],
                dependent_fields={'estado': 'estado'},
                max_results=50,
                attrs={
                    "data-minimum-input-length": 4,
                }
    ))
    asentamiento =  forms.ModelChoiceField(queryset=sepomex.Asentamiento.objects.all(),                                    
            widget=s2forms.ModelSelect2Widget(
                model=sepomex.Asentamiento,
                search_fields=['nombre__icontains'],
                dependent_fields={'municipio': 'municipio'},
                max_results=50,
                attrs={
                    "data-minimum-input-length": 4,
                }
    ))

    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    helper = FormHelper()
    helper.layout = Layout(
            Div(
                Div('nombre', css_class='col-md-4'),
                Div('primer_apellido', css_class='col-md-4'),
                Div('segundo_apellido', css_class='col-md-4'),
                css_class='row'
            ),
            Div(
                Div('tipo_persona', css_class='col-md-4'),
                Div('genero', css_class='col-md-4'),
                Div('estatus', css_class='col-md-4'),
                css_class='row'
            ),
            Div(
                Div('lugar_nacimiento',css_class='col-md-8'),            
                Div('fecha_nacimiento',css_class='col-md-4'),
                css_class='row'
            ),
            Div(
                Div('estado', css_class='col-md-4'),
                Div('municipio', css_class='col-md-4'),
                Div('asentamiento', css_class='col-md-4'),
                css_class='row'
            ),
            Div(
                Div('calle', css_class='col-md-6'),
                Div('numero', css_class='col-md-3'),
                Div('numero_interior', css_class='col-md-3'),
                css_class='row'
            ),
            Div(
                Submit('submit', 'Agregar', css_class='btn btn-info'),
                 HTML("""
                    <a class="btn btn-primary" href="{{request.META.HTTP_REFERER|escape}}">Regresar</a>
                """),
                css_class='col text-center'
            ),
            
    )

    class Meta:
        model = modelos.PersonaPrincipal
        fields = ['tipo_persona', 'nombre', 'primer_apellido',
                  'segundo_apellido', 'genero', 'estatus',
                  'asesor', 'lugar_nacimiento', 'fecha_nacimiento',
                  'estado', 'municipio', 'asentamiento', 
                  'calle', 'numero', 'numero_interior',
                  ]  

    

#Asesores
        
class EmpresaWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "nombre__icontains",
        "clave__icontains",
    ]


        
class AsesorCustomForm(forms.Form):
    usuario = forms.CharField(label='Nombre de usuario')
    correo = forms.EmailField(label='Correo electrónico')
    nombre = forms.CharField(label='Nombre')
    apellidos = forms.CharField(label='Apellidos')
    empresa = forms.ModelMultipleChoiceField(label='Empresas',
        queryset=modelos.EmpresaContratante.objects.all(),                                    
        widget=s2forms.ModelSelect2MultipleWidget(
            model=modelos.EmpresaContratante,
            search_fields=['nombre__icontains'],
            attrs={
                "data-minimum-input-length": 3,
            }
    ))
    telefono2 = forms.CharField(label='Telefono 1')
    telefono1 = forms.CharField(label='Telefono 2')
    helper = FormHelper()
    helper.layout = Layout(
            Div(
                Div('nombre', css_class='col-md-5'),
                Div('apellidos', css_class='col-md-5'),
                Div('usuario', css_class='col-md-2'),
                css_class='row'
            ),
            Div(
                Div('correo', css_class='col-md-8'),
                Div('empresa', css_class='col-md-4'),
                css_class='row'
            ),
            Div(
                Div('telefono1',css_class='col-md-2'),            
                Div('telefono2',css_class='col-md-4'),
                css_class='row'
            ),
            Div(
                Submit('submit', 'Agregar', css_class='btn btn-info'),
                 HTML("""
                    <a class="btn btn-primary" href="{{request.META.HTTP_REFERER|escape}}">Regresar</a>
                """),
                css_class='col text-center'
            ),
    )

    @transaction.atomic
    def crea_asesor(self):
        username = self.cleaned_data.get('usuario')
        email = self.cleaned_data.get('correo')
        first_name = self.cleaned_data.get('nombre')
        last_name = self.cleaned_data.get('apellidos')
        empresa = self.cleaned_data.get('empresa')
        telefono1 = self.cleaned_data.get('telefono1')
        telefono2 = self.cleaned_data.get('telefono2')

        # Crear el usuario
        user, created = User.objects.get_or_create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        # Crear el perfil del asesor
        asesor = modelos.Asesor.objects.create(
            usuario=user,
            telefono1=telefono1,
            telefono2=telefono2
        )
        #Modificar para agregar telefono, clave y correo por empresa

        asesor.empresa.set(empresa)     