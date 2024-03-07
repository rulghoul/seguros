

from django import forms
from . import models as modelos

class xml_sepomex_upload_form(forms.Form):
    sepomex_xml = forms.FileField()

class EstadoForm(forms.ModelForm):
    class Meta:
        model = modelos.Estado
        fields = ('clave', 'nombre')

class TipoAsentamientoForm(forms.ModelForm):
    class Meta:
        model = modelos.TipoAsentamiento
        fields = ('clave', 'nombre')

class MunicipioForm(forms.ModelForm):
    class Meta:
        model = modelos.Municipio
        fields = ('estado','clave', 'nombre')

class AsentamientoForm(forms.ModelForm):
    class Meta:
        model = modelos.Asentamiento
        fields = ('municipio', 'tipo_asentamiento', 'codigo_postal', 'nombre')