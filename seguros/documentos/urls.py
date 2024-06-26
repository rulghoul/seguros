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
    #Asesores 
    path('asesor_add', asesores.crear_o_editar_asesor, name='asesor_add'),
    path('asesor_update/<int:pk>/', asesores.crear_o_editar_asesor, name='asesor_update'),
    path('asesor_delete/<int:pk>/', asesores.borrar_asesor.as_view(), name='asesor_delete'),
    path('asesor_list', asesores.ListAseror.as_view(), name='asesor_list'),
    # Clientes
    path('clientes', asesores.ListCliente.as_view(), name='clientes'),
    path('cliente_add', asesores.PersonaPrincipalAdd.as_view(), name='cliente_add'),
    path('borra_cliente/<int:pk>/', asesores.borrar_cliente.as_view(), name='borra_cliente'),
    path('cliente_update/<int:pk>/', asesores.PersonaPrincipalUpdate.as_view(), name='cliente_update'),
    path('buscar_cliente_por_curp/', asesores.buscar_cliente_por_curp, name='buscar_cliente_por_curp'),
    #Polizas
    path('polizas', polizas.Poliza_List.as_view(), name='polizas'),
    path('polizas_cliente/<int:pk>/', polizas.polizas_cliente.as_view(), name='polizas_cliente'),
    path('poliza_add', polizas.edit_poliza, name='poliza_add'),
    path('poliza_delete/<int:pk>/', polizas.borrar_poliza.as_view(), name='poliza_delete'),
    path('poliza_update/<int:pk>/', polizas.edit_poliza, name='poliza_update'),
    path('poliza_cliente_update/<int:pk>/<int:cliente>/', polizas.edit_poliza_cliente, name='poliza_cliente_update'),
    path('poliza_cliente_add/<int:cliente>/', polizas.edit_poliza_cliente, name='poliza_cliente_add'),
    #Sinestros
    path('siniestros/<int:pk>/', polizas.Siniestro_List.as_view(), name='siniestros'),
    path('siniestro_add/<int:pk>/', polizas.Siniestro_Add.as_view(), name='siniestro_add'),
    path('siniestro_update/<int:pk>/', polizas.Siniestro_Update.as_view(), name='siniestro_update'), 
    #Documentos
    path('doc_poliza/<int:pk>/', polizas.upload_documentos_poliza.as_view(), name='doc_poliza'),
    path('doc_siniestros/<int:pk>/', polizas.upload_documentos_siniestro.as_view(), name='doc_siniestros'),
]