from django import forms
from django_select2 import forms as s2forms
from django.forms import inlineformset_factory, BaseFormSet, formset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, HTML, Submit, Row, Field
from crispy_bootstrap5.bootstrap5 import BS5Accordion

from . import models as modelos
from sepomex import models as sepomex
from collections import OrderedDict



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
    ))
    municipio = forms.ModelChoiceField(queryset=sepomex.Municipio.objects.all(),                                    
            widget=s2forms.ModelSelect2Widget(
                model=sepomex.Municipio,
                search_fields=['nombre__icontains'],
                dependent_fields={'estado': 'estado'},
                max_results=500,
    ))
    asentamiento =  forms.ModelChoiceField(queryset=sepomex.Asentamiento.objects.all(),                                    
            widget=s2forms.ModelSelect2Widget(
                model=sepomex.Asentamiento,
                search_fields=['nombre__icontains'],
                dependent_fields={'municipio': 'municipio'},
                max_results=500,
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
                Div('piso', css_class='col-md-3'),
                css_class='row'
            ),
    )

    class Meta:
        model = modelos.PersonaPrincipal
        fields = ['tipo_persona', 'nombre', 'primer_apellido',
                  'segundo_apellido', 'genero', 'estatus',
                  'asesor', 'lugar_nacimiento', 'fecha_nacimiento',
                  'estado', 'municipio', 'asentamiento', 
                  'calle', 'numero', 'piso',
                  ]  

    

