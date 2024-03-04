from django import forms
from django.forms import inlineformset_factory, BaseFormSet, formset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, HTML, Submit

from . import models as modelos

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
