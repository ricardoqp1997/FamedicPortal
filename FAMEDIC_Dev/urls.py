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


# librerías estandar para el manejo de accesos, URLs y panel administrativo
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

# class views para manejo de inicio y cierre de sesión (se usa solo para cierre)
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import include

# class views para manejo de listado y detalle de radicados
from portal_radicaciones import views as portal_views
from portal_radicaciones.views import (
    ListaRadicados,
    RadicadoDetail,
    LoginFamedic,
    TokenAccess,
    Registration,
    passwordchangesave,
    capacitacion

)

# librerías de django para configuración de alojamiento de archivos estaticos cargados en la radicación
from django.conf import settings
from django.conf.urls.static import static

# librerías de django y django OTP para la configuración de OTP en el portal administrativo
import django_otp.admin
from django.db import models
from django_otp.models import Device, ThrottlingMixin
from django.contrib.admin.sites import AdminSite
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin

# modelo y clase (admin class) de usuarios famedic para el portal administrativo con OTP
from famedic_users.models import FamedicUser as User
from famedic_users.admin import UserAdmin

# modelos y clases (admin class) de radicaciones famedic para el portal administrativo con OTP
from portal_radicaciones.models import *
from portal_radicaciones.admin import *


# Nuevo sitio con OTP para acceso
class OTPAdminSite(AdminSite):

    login_form = django_otp.admin.OTPAdminAuthenticationForm
    login_template = django_otp.admin._admin_template_for_django_version()

    def has_permission(self, request):
        return super().has_permission(request) and \
               request.user.is_authenticated and \
               request.user.is_admin and not request.user.bloqueado


# Llamado de la clase (class admin) para el manejo del portal admin cin OTP
class OTPAdmin(OTPAdminSite):
    pass


# adición de contenido de modelos y clases de DISPOSITIVOS OTP al nuevo panel administrativio
admin_site = OTPAdmin(name='OTPAdmin')
admin_site.register(TOTPDevice, TOTPDeviceAdmin)

# adición de contenido de modelos y clases de USUARIOS FAMEDIC al nuevo panel administrativio
admin_site.register(User, UserAdmin)

# adición de contenido de modelos y clases de RADICACION FAMEDIC al nuevo panel administrativio
admin_site.register(Locacion, LocacionAdmin)
admin_site.register(RadicacionModel, RadicacionAdmin)
admin_site.register(Sedes, SedesAdmin)
admin_site.register(Glosa, GlosaAdmin)
admin_site.register(Subglosa, SubglosaAdmin)

# Personalización de titulo y nombre del sitio de administración Django acorde a Famedic IPS
admin_site.site_header = 'Panel administrativo: Famedic'
admin_site.site_title = 'Famedic IPS'


# URLs del portal de radicación de facturas famedic
urlpatterns = [

    # index de "portal_radicaciones" redireccionará a Login si no se ha iniciado sesión
    path('', portal_views.index, name='index'),

    # Vistas de inicio de sesión cargadas directamente desde las librerías de Django
    # path('login/', portal_views.login_famedic, name='login'),
    path('login/', LoginFamedic.as_view(), name='login'),
    path('capacitacion/', portal_views.capacitacion, name="capacitacion"),
    path('ending-session', portal_views.logout_redirect, name='pre-logout'),
    path('logout/', auth_views.LogoutView.as_view(template_name='FamedicDesign/LogOut.html'), name='logout'),

    # Vistas de registro y validación creadas en el views.py de la app "portal_radicaciones"
    path('registro/', Registration.as_view(), name='register'),
    path('verificacion/', TokenAccess.as_view(), name='token_access'),
    path('resend-token', portal_views.resend_token, name='resend'),

    # Acceso al panel administrativo
    path('admin-redirect', portal_views.admin_redirect, name='admin'),
    path('admin/', admin_site.urls),

    # Vistas del menú principal de la aplicación después de haber iniciado sesión de forma correcta
    path('main/', portal_views.hola_mundo, name='main'),
    path('main/perfil/', portal_views.perfil, name='profile'),
    path('main/radicar/', portal_views.radicacion, name='radicar'),
    path('main/historial/', login_required(ListaRadicados.as_view(), login_url='/login/'), name='radicados_list'),
    path('main/detalles/<int:pk>', login_required(RadicadoDetail.as_view(), login_url='/login/'), name='radicado_detail'),

    # Vista al haber realizado radicación exitosa
    path('main/done/', portal_views.radicacion_finish, name='radicado_finished'),

    # Vista cambio de contraseña
    path('passwordchangesave/', portal_views.passwordchangesave, name='passwordchangesave'),
]

# Configuración del flujo de archivos multimedia cargados en cada formulario de radicación
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
