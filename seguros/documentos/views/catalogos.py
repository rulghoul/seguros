from documentos import models as mod
from documentos import forms as formularios

from .generic_view import BaseListView


######################### Catalogos ###########################

class TipoConductoPagoView(BaseListView):
    form_class = formularios.TipoConductoPagoForm
    model = mod.TipoConductoPago
    template_name = 'catalogos/list.html'
    redirige = 'documentos:lista_tipo_conducto_pago'
    context_object_name = 'lista'
    title = ' Tipo De Conducto Pago'
    encabezados = ['CLAVE', 'DESCRIPCION', 'ACTIVO']
    campos = ['clave', 'descripcion', 'activo']

class TipoPersonaView(BaseListView):
    form_class = formularios.TipoPersonaForm
    model = mod.TipoPersona
    template_name = 'catalogos/list.html'
    redirige = 'documentos:lista_tipo_persona'
    context_object_name = 'lista'
    title = 'Tipo de Persona'
    encabezados = ['CLAVE', 'DESCRIPCION', 'ACTIVO']
    campos = ['clave', 'descripcion', 'activo']


class FormaPagoView(BaseListView):
    form_class = formularios.FormaPagoForm
    model = mod.FormaPago
    template_name = 'catalogos/list.html'
    redirige = 'documentos:lista_forma_pago'
    context_object_name = 'lista'
    title = 'Forma de Pago'
    encabezados = ['CLAVE', 'DESCRIPCION', 'ACTIVO']
    campos = ['clave', 'descripcion', 'activo']

class DocumentosView(BaseListView):
    form_class = formularios.DocumentosForm
    model = mod.TipoDocumentos
    template_name = 'catalogos/list.html'
    redirige = 'documentos:lista_documentos'
    context_object_name = 'lista'
    title = 'Tipo Documentos'
    encabezados = ['CLAVE', 'DESCRIPCION', 'ACTIVO']
    campos = ['tipo', 'descripcion', 'activo']


class TipoMediocontactoView(BaseListView):
    form_class = formularios.TipoMediocontactoForm
    model = mod.TipoMediocontacto
    template_name = 'catalogos/list.html'
    redirige = 'documentos:lista_tipo_medio_conctacto'
    context_object_name = 'lista'
    title = 'Tipo Medio Contacto'
    encabezados = ['DESCRIPCION', 'ACTIVO']
    campos = ['descripcion', 'activo']



class ParentescoView(BaseListView):
    form_class = formularios.ParentescoForm
    model = mod.Parentesco
    template_name = 'catalogos/list.html'
    redirige = 'documentos:lista_parentesco'
    context_object_name = 'lista'
    title = 'Parentesco'
    encabezados = ['DESCRIPCION', 'ACTIVO']
    campos = ['descripcion', 'activo']
