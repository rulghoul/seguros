# urls.py
from django.urls import path, include
from . import views
from rest_framework import routers 
  
# import everything from views 
from .views import *
 
# define the router 
router = routers.DefaultRouter() 
  
# define the router path and viewset to be used 
router.register(r'subscripciones', views.SuscripcionViewSet) 
router.register(r'asesores', views.AsesoresViewSet) 
router.register(r'usuarios', views.UsuariosViewSet) 
router.register(r'empresas', views.EmpresaViewSet) 
router.register(r'polizas', views.PolizasViewSet) 
router.register(r'clientes', views.ClientesViewSet)
router.register(r'sepomex', views.AsentamientosViewSet)
router.register(r'crear-asesor', views.CreaAsesorView, basename='crear-asesor')
#router.register(r'subscription', views.SubscriptionAPIView)

urlpatterns = [
    path('', include(router.urls)), 
]
