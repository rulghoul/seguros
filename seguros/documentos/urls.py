from django.urls import path
from . import views

app_name = 'documentos' 

urlpatterns = [    
    path('lista_tipo_conducto_pago/', views.TipoConductoPagoView.as_view(), name='lista_tipo_conducto_pago'),
    path('lista_tipo_persona/', views.TipoPersonaView.as_view(), name='lista_tipo_persona'),
    path('lista_forma_pago/', views.FormaPagoView.as_view(), name='lista_forma_pago'),
    path('lista_documentos/', views.DocumentosView.as_view(), name='lista_documentos'),
    path('lista_tipo_medio_conctacto/', views.TipoMediocontactoView.as_view(), name='lista_tipo_medio_conctacto'),
    path('lista_parentesco/', views.ParentescoView.as_view(), name='lista_parentesco'),
    path('lista_empresa/', views.EmpresaContratanteView.as_view(), name='lista_empresa'),
    path('lista_planes/', views.PlanesView.as_view(), name='lista_planes'),
    #Asesores y sus clientes
    path('asesor_add', views.AsesorAdd.as_view(), name='asesor_add'),
    path('principal_add', views.PersonaPrincipalAdd.as_view(), name='principal_add'),
]