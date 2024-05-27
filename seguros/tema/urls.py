from django.urls import path
from . import views

app_name = 'tema'  



urlpatterns = [
    path('add_color', views.add_color.as_view(), name='add_color'),
    path('update_color/<int:pk>/', views.update_color.as_view(), name='update_color'),
    path('list_color', views.list_color.as_view(), name='list_color'),
    #imagenes
    path('add_imagen', views.add_imagen.as_view(), name='add_imagen'),
    path('update_imagen/<int:pk>/', views.update_imagen.as_view(), name='update_imagen'),
    path('list_imagen', views.list_imagen.as_view(), name='list_imagen'),
] 