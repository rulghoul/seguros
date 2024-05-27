from django.urls import path
from .views import asesores
from .views import catalogos
from .views import polizas

app_name = 'documentos' 

urlpatterns = [    
    path('lista_tipo_conducto_pago/', catalogos.TipoConductoPagoView.as_view(), name='lista_tipo_conducto_pago'),
    path('lista_tipo_persona/', catalogos.TipoPersonaView.as_view(), name='lista_tipo_persona'),
    path('lista_forma_pago/', catalogos.FormaPagoView.as_view(), name='lista_forma_pago'),
    path('lista_documentos/', catalogos.DocumentosView.as_view(), name='lista_documentos'),
    path('lista_tipo_medio_conctacto/', catalogos.TipoMediocontactoView.as_view(), name='lista_tipo_medio_conctacto'),
    path('lista_parentesco/', catalogos.ParentescoView.as_view(), name='lista_parentesco'),
    path('lista_empresa/', asesores.EmpresaContratanteView.as_view(), name='lista_empresa'),
    path('lista_planes/', asesores.PlanesView.as_view(), name='lista_planes'),
    #Asesores y sus clientes
    path('asesor_add', asesores.crear_o_editar_asesor, name='asesor_add'),
    path('asesor_update/<int:pk>/', asesores.crear_o_editar_asesor, name='asesor_update'),
    path('asesor_list', asesores.ListAseror.as_view(), name='asesor_list'),
    path('principal_list', asesores.ListCliente.as_view(), name='principal_list'),
    path('principal_add', asesores.PersonaPrincipalAdd.as_view(), name='principal_add'),
    path('principal_update/<int:pk>/', asesores.PersonaPrincipalUpdate.as_view(), name='principal_update'),
    #Polizas
    path('polizas', polizas.Poliza_List.as_view(), name='polizas'),
    path('poliza_add', polizas.edit_poliza, name='poliza_add'),
    path('poliza_update/<int:pk>/', polizas.edit_poliza, name='poliza_update'),
    #Sinestros
    path('siniestros', polizas.Poliza_List.as_view(), name='siniestros'),
    path('siniestro_add', polizas.edit_poliza, name='siniestro_add'),
    path('siniestro_update/<int:pk>/', polizas.edit_poliza, name='siniestro_update'), 
    #Documentos
    path('doc_poliza/<int:pk>/', polizas.upload_documentos_poliza, name='doc_poliza'),
    path('doc_siniestros/<int:pk>/', polizas.upload_documentos_poliza, name='doc_siniestros'),
]