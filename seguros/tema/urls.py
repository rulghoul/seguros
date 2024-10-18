from django.urls import path
from . import views
from django.contrib.admin.views.decorators import staff_member_required
app_name = 'tema'  



urlpatterns = [
    path('add_color', staff_member_required(views.add_color.as_view()), name='add_color'),
    path('update_color/<int:pk>/', staff_member_required(views.update_color.as_view()), name='update_color'),
    path('list_color', staff_member_required(views.list_color.as_view()), name='list_color'),
    #imagenes
    path('add_imagen', staff_member_required(views.add_imagen.as_view()), name='add_imagen'),
    path('update_imagen/<int:pk>/', staff_member_required(views.update_imagen.as_view()), name='update_imagen'),
    path('list_imagen', staff_member_required(views.list_imagen.as_view()), name='list_imagen'),
] 