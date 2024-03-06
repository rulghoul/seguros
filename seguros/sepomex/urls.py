from django.urls import path
from . import views

app_name = 'sepomex' 


urlpatterns = [
    path('carga_automatica', views.upload_xml, name='carga_automatica'),
    ##Listados    
    path('estado', views.EstadoView.as_view(), name='estado'),
    path('municipio', views.MunicipioView.as_view(), name='municipio'),
    path('asentamiento', views.AsentamientoView.as_view(), name='asentamiento'),
    path('tipo_asentamiento', views.TipoAsentamientoView.as_view(), name='tipo_asentamiento'),
]