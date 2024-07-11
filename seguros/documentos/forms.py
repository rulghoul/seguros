from django import forms
from django_select2 import forms as s2forms
from django.shortcuts import render, redirect, reverse
from django.forms import inlineformset_factory, BaseFormSet, formset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Div, HTML, Submit, Row, Field, Button
from crispy_bootstrap5.bootstrap5 import BS5Accordion

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from . import models as modelos
from sepomex import models as sepomex
from collections import OrderedDict

from django.utils.safestring import mark_safe

from django.db import transaction
from django.core.validators import RegexValidator

from documentos.utils.encript_files import encripta_archivo, desencripta_archivo
import os

curp_validator = RegexValidator(
    regex='^[A-Z]{4}\\d{6}(H|M)[A-Z]{5}[A-Z0-9]{2}$',
    message='Introduce un CURP válido.'
)


class BootstrapCheckboxInput(forms.CheckboxInput):
    template_name = 'django/forms/widgets/checkbox.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['class'] = 'form-check-input'
        return context


class TipoConductoPagoForm(forms.ModelForm):
    class Meta:
        model = modelos.TipoConductoPago
        fields = ('clave', 'descripcion', 'activo')


class TipoPersonaForm(forms.ModelForm):
    class Meta:
        model = modelos.TipoPersona
        fields = ('clave', 'descripcion', 'activo')


class FormaPagoForm(forms.ModelForm):
    class Meta:
        model = modelos.FormaPago
        fields = ('clave', 'descripcion', 'activo')


class DocumentosForm(forms.ModelForm):
    class Meta:
        model = modelos.TipoDocumentos
        fields = ('tipo','descripcion', 'activo')


class TipoMediocontactoForm(forms.ModelForm):
    class Meta:
        model = modelos.TipoMediocontacto
        fields = ('descripcion', 'activo')


class ParentescoForm(forms.ModelForm):
    class Meta:
        model = modelos.Parentesco
        fields = ('descripcion', 'activo')


class EmpresaContratanteForm(forms.ModelForm):
    class Meta:
        model = modelos.EmpresaContratante
        fields = ('clave', 'nombre', 'link', 'logo_small', 'activo', )


class PlanesForm(forms.ModelForm):
    class Meta:
        model = modelos.Planes
        fields = ('nombre', 'empresa', 'gastosMedicos','activo', )


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
    codigo_postal = forms.CharField(
        max_length=5, required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    municipio = forms.CharField(label="Munuicipio/Alcaldia", max_length=250,
                                required=False, widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    estado = forms.CharField(max_length=250, required=False,
                             widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    curp = forms.CharField(validators=[curp_validator], max_length=18)
    asentamiento = forms.ModelChoiceField(
        label="Colonia",
        queryset=sepomex.Asentamiento.objects.all(),
        widget=s2forms.ModelSelect2Widget(
            model=sepomex.Asentamiento,
            search_fields=['codigo_postal__icontains', 'nombre__icontains'],
            max_results=50,
            attrs={
                "data-minimum-input-length": 3,
                "data-placeholder": "No se encontro la la colonia o Codigo Postal",
            }
        ))
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(
        format='%Y-%m-%d', attrs={'type': 'date'}))
    helper = FormHelper()
    helper.form_tag = False

    class Meta:
        model = modelos.PersonaPrincipal
        fields = ['nombre', 'primer_apellido', 'curp',
                  'segundo_apellido', 'genero', 'estatus_persona',
                  'asesor_cliente', 'lugar_nacimiento', 'fecha_nacimiento',
                  'asentamiento',
                  'calle', 'numero', 'numero_interior',
                  'correo', 'telefono',
                  ]

        widgets = {
            'asesor_cliente': forms.HiddenInput(),
        }

    def __init__(self,*args, **kwargs):
        super(PersonaPrincipalForm, self).__init__(*args, **kwargs)      
        if self.instance and self.instance.pk:
            self.fields['estado'].initial = self.instance.asentamiento.municipio.estado
            self.fields['municipio'].initial = self.instance.asentamiento.municipio.estado
            self.fields['codigo_postal'].initial = self.instance.asentamiento.codigo_postal
        
        self.fields['asesor_cliente'].required = False
        self.helper.layout = Layout(
            Div(
                Div('nombre', css_class='col-md-4'),
                Div('primer_apellido', css_class='col-md-4'),
                Div('segundo_apellido', css_class='col-md-4'),
                css_class='row'
            ),
            Div(
                Div('curp', css_class='col-md-6'),
                Div('genero', css_class='col-md-3'),
                Div('estatus_persona', css_class='col-md-3'),
                css_class='row'
            ),
            Div(
                Div('lugar_nacimiento', css_class='col-md-8'),
                Div('fecha_nacimiento', css_class='col-md-4'),
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
                Div('correo', css_class='col-md-9'),
                Div('telefono', css_class='col-md-3'),
                css_class='row'
            ),
            Div(
                Submit('submit', 'Guardar', css_class='btn btn-info'),
                HTML("""
                        <a class="btn btn-primary" href="{% url '""" +
                        "documentos:clientes' "
                        """ %}">Regresar</a>
                    """),
                css_class='col text-center'
            ),
            Field('asesor_cliente', type="hidden"),
        )


# Asesores

class EmpresaWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "nombre__icontains",
        "clave__icontains",
    ]
    model = modelos.EmpresaContratante
    queryset = modelos.EmpresaContratante.objects.all()
    attrs = {
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
    max_num=6,
    can_delete=True
)


class FormBeneficiario(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Div(
            Div('tipo_persona', css_class='col-md-3'),
            Div('nombre_completo', css_class='col-md-6'),
            Div('porcentaje_participacion', css_class='col-md-3'),
            css_class='row'
        ),
    )

    class Meta:
        model = modelos.Beneficiarios
        fields = ['parentesco', 'nombre_completo', 'porcentaje_participacion',]


class BeneficiariosHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_method = 'post'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.layout = Layout(
            Div(
                Div('parentesco', css_class='col-md-3'),
                Div('nombre_completo', css_class='col-md-6'),
                Div('porcentaje_participacion', css_class='col-md-3'),
                css_class='row'
            ),
        )
        self.render_required_fields = True


BeneficiariosFormset = inlineformset_factory(
    parent_model=modelos.Poliza,
    model=modelos.Beneficiarios,
    form=FormBeneficiario,
    min_num=1,
    extra=2,
    max_num=5,
    can_delete=True
)


class PolizaForm(forms.ModelForm):
    plan = forms.ModelChoiceField(
        queryset=modelos.Planes.objects.all(),
        label="Plan",
        required=True,
        widget=s2forms.ModelSelect2Widget(
            model=modelos.Planes,
            search_fields=['nombre__icontains'],
            dependent_fields={'empresa': 'empresa'},
            max_results=50,
            attrs={
                "data-minimum-input-length": 0,
                "data-placeholder": "No hay planes Disponibles",
                "data-allow-clear": True,
            },
        )
    )
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Div(
            Div('empresa', css_class='col-md-4'),
            Div('numero_poliza', css_class='col-md-4'),
            Div('forma_pago', css_class='col-md-4'),
            css_class='row'
        ),
        Div(
            Div('tipo_conducto_pago', css_class='col-md-4'),
            Div('plan', css_class='col-md-8'),
            css_class='row'
        ),
        Div(
            Div('fecha_emision', css_class='col-md-6'),
            Div('fecha_vigencia', css_class='col-md-6'),
            css_class='row'
        ),
        Div(
            Div('fecha_pago', css_class='col-md-4'),
            Div('monto', css_class='col-md-4'),
            Div('estatus', css_class='col-md-4'),
            css_class='row'
        ),
        Div(
            Submit('submit', 'Guardar', css_class='btn btn-info'),
            HTML("""
                    <a class="btn btn-primary" href="{{request.META.HTTP_REFERER|escape}}">Regresar</a>
                """),
            css_class='col text-center'
        ),
        Field('asesor_poliza', type="hidden"),
    )

    class Meta:
        model = modelos.Poliza
        fields = ['empresa', 'numero_poliza', 'forma_pago', 'asesor_poliza',
                  'tipo_conducto_pago', 'plan', 'fecha_vigencia', 'fecha_emision',
                  'fecha_pago', 'monto', 'estatus']

        widgets = {
            'fecha_vigencia': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fecha_emision': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fecha_pago': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'asesor_poliza': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(PolizaForm, self).__init__(*args, **kwargs)
        asesor = self.instance.asesor_poliza
        if asesor and asesor.pk:
            self.fields['empresa'].queryset = modelos.EmpresaContratante.objects.filter(
                asesorempresa__asesor_id=asesor
            )
        else:
            self.fields['empresa'].queryset = modelos.EmpresaContratante.objects.none()


from .widgets import CustomFileInput

class MultiDocumentUploadForm(forms.Form):
    def __init__(self, lista_archivos, archivos_existentes=None, retorno=None, indice=None, modelo=None, *args, **kwargs):
        super(MultiDocumentUploadForm, self).__init__(*args, **kwargs)
        
        for archivo in lista_archivos:
            self.fields[archivo] = forms.FileField(
                required=False,
                label=archivo
            )

            if archivos_existentes and archivo in archivos_existentes:
                #self.fields[archivo].initial = archivos_existentes[archivo]
                documento = archivos_existentes[archivo]
                self.fields[archivo] = forms.FileField(
                    required=False,
                    label=mark_safe(f'''{archivo}<div class="input-group"><span class="input-group-text"></span>
                                    {documento.name.replace(".enc","").replace("documento_poliza/","")}
                                    <a class="form-control d-flex h-auto" target="_blank" href="/documentos/documento/{documento.instance.pk}/descargar/{modelo}/0"><span class="fa fa-eye"></span></a>
                                    <a class="form-control d-flex h-auto" target="_blank" href="/documentos/documento/{documento.instance.pk}/descargar/{modelo}/1"><span class="fa fa-download"></span></a>
                                    </div>'''),
                    widget=CustomFileInput()
                )
            else:
                self.fields[archivo] = forms.FileField(
                    required=False,
                    label=archivo, 
                )

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.layout = Layout(
            *[Field(archivo) for archivo in lista_archivos],
            Submit('submit', 'Cargar'),
            HTML("""
                    <a class="btn btn-primary" href="{{request.META.HTTP_REFERER|escape}}">Regresar</a>
                """),
        )


class SiniestroForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_tag = False
    helper.layout = Layout(
        Div(
            Div('numero_siniestro', css_class='col-md-4'),
            Div('fecha_evento', css_class='col-md-4'),
            Div('estatus', css_class='col-md-4'),
            css_class='row'
        ),
        Div(
            Div('descripcion_siniestro', css_class='col-md-12'),
            css_class='row'
        ),
        Div(
            Submit('submit', 'Guardar'),
            HTML('<a class="btn btn-primary" href="' +
                 "{{request.META.HTTP_REFERER|escape}}" + '">Regresar</a>'),
            css_class='col text-center'
        ),
        Field('poliza', type="hidden"),
    )

    class Meta:
        model = modelos.Siniestros
        fields = ['poliza', 'numero_siniestro',
                  'descripcion_siniestro', 'fecha_evento', 'estatus']
        
        widgets = {
            'fecha_evento': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),}
