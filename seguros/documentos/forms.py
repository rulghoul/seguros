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
    codigo_postal = forms.CharField(max_length=5, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    municipio = forms.CharField(label="Munuicipio/Alcaldia",max_length=250, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    estado = forms.CharField(max_length=250, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    asentamiento =  forms.ModelChoiceField(
        label="Colonia",
        queryset=sepomex.Asentamiento.objects.all(),                                    
            widget=s2forms.ModelSelect2Widget(
                model=sepomex.Asentamiento,
                search_fields=['codigo_postal__icontains','nombre__icontains'],
                max_results=50,
                attrs={
                    "data-minimum-input-length": 3,
                    "data-placeholder": "Buscar por nombre o codigo postal",
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
                Div('estado', css_class='col-md-3'),
                Div('municipio', css_class='col-md-3'),
                Div('asentamiento', css_class='col-md-4'),
                Div('codigo_postal', css_class='col-md-2'),
                css_class='row'
            ),
            Div(
                Div('calle', css_class='col-md-6'),
                Div('numero', css_class='col-md-3'),
                Div('numero_interior', css_class='col-md-3'),
                css_class='row'
            ),
            Div(
                Submit('submit', 'Guardar', css_class='btn btn-info'),
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
                  'asentamiento', 
                  'calle', 'numero', 'numero_interior',
                  ]  

    

#Asesores
        
class EmpresaWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "nombre__icontains",
        "clave__icontains",
    ]
    model=modelos.EmpresaContratante
    queryset=modelos.EmpresaContratante.objects.all()
    attrs={
        "data-minimum-input-length": 3,
    }

class UserForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
            Div(
                Div('first_name', css_class='col-md-6'),
                Div('last_name', css_class='col-md-6'),
                css_class='row'
            ),
            Div(
                Div('username', css_class='col-md-4'),
                Div('email', css_class='col-md-8'),
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
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class AsesorEmpresaForm(forms.ModelForm):
    class Meta:
        model = modelos.AsesorEmpresa
        fields = ['empresa', 'correo_empleado', 'codigo_empleado', 'telefono']

class AsesorEmpresaFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.layout = Layout(
                Div(
                    Div('empresa', css_class='col-md-6'),
                    Div('codigo_empleado', css_class='col-md-3'),
                    Div('telefono', css_class='col-md-3'),
                    css_class='row'
                ),
                Div(
                    Div('correo_empleado', css_class='col-md-12'),
                    css_class='row'
                ),
        )
        self.render_required_fields = True

AsesorEmpresaFormset = inlineformset_factory(
    parent_model=modelos.Asesor,
    model=modelos.AsesorEmpresa,
    form=AsesorEmpresaForm,
    min_num=1,
    extra=2,  
    max_num=5,
    can_delete=True 
)

class FormBeneficiario(forms.ModelForm):
    class Meta:
        model = modelos.Beneficiarios
        fields = ['tipo_persona', 'nombre_completo', 'porcentaje_participacion',]

class BeneficiariosHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
                Div(
                    Div('tipo_persona', css_class='col-md-3'),
                    Div('nombre_completo', css_class='col-md-6'),
                    Div('porcentaje_participacion', css_class='col-md-3'),
                    css_class='row'
                ),
        )

BeneficiariosFormset = inlineformset_factory(
    parent_model=modelos.Poliza,
    model=modelos.Beneficiarios,
    form=FormBeneficiario,
    min_num=1,
    extra=2,  
    max_num=5,
    can_delete=True 
)