from django.urls import path
from . import views

app_name = 'sepomex' 


urlpatterns = [
    path('carga_sepomex', views.upload_xml, name='carga_sepomex'),
    ##Listados    
    path('estado', views.EstadoView.as_view(), name='estado'),
    path('municipio', views.MunicipioView.as_view(), name='municipio'),
    path('asentamiento', views.AsentamientoView.as_view(), name='asentamiento'),
    path('tipo_asentamiento', views.TipoAsentamientoView.as_view(), name='tipo_asentamiento'),
    path('asentamiento_details/<int:id>/', views.get_asentamiento_details, name='asentamiento_details'),
]