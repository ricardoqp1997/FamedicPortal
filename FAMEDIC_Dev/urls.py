"""FAMEDIC_Dev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.contrib.auth import views as auth_views
from portal_radicaciones import views as portal_views
from portal_radicaciones.views import ListaRadicados

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.decorators import login_required


urlpatterns = [

    # Acceso al panel administrativo
    path('admin-redirect', portal_views.admin_redirect, name='admin'),
    path('admin/', admin.site.urls),

    # index de "portal_radicaciones" redireccionará a Login si no se ha iniciado sesión
    path('', portal_views.index, name='index'),

    # Vistas de registro y validación creadas en el views.py de la app "portal_radicaciones"
    path('registro/', portal_views.register_famedic, name='register'),
    path('verificacion/', portal_views.token_famedic, name='token_access'),
    path('resend-token', portal_views.resend_token, name='resend'),

    # Vistas de inicio de sesión cargadas directamente desde las librerías de Django
    path('login/', portal_views.login_famedic, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='FamedicDesign/LogOut.html'), name='logout'),

    # Vistas del menú principal de la aplicación después de haber iniciado sesión de forma correcta
    path('main/', portal_views.hola_mundo, name='main'),
    path('main/perfil/', portal_views.perfil, name='profile'),
    path('main/radicar/', portal_views.radicacion, name='radicar'),
    path('main/historial/', login_required(ListaRadicados.as_view()), name='radicados_list'),

    # Vista al haber realizado radicación exitosa
    path('main/done/', portal_views.radicacion_finish, name='radicado_finished')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
