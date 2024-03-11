"""
URL configuration for seguros project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from tema import views as tema_views
from documentos import views as doc_views
from sepomex import views as sepomex_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('tema', include('tema.urls')),
    path('sepomex/', include('sepomex.urls')),
    path('documentos/', include('documentos.urls')),
    path("select2/", include("django_select2.urls")),
    path('', tema_views.home_view, name='home'),    
    path('accounts/profile/', tema_views.home_view, name='profile'),
    path('login/', tema_views.CustomLoginView.as_view(), name='login'),
    path('logout/', tema_views.CustomLogoutView.as_view(), name='logout'),
    path('change-password/', auth_views.PasswordChangeView.as_view(), name="password_change"),    
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #\
