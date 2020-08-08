from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    # index de "portal_radicaciones" redireccionará a Login si no se ha iniciado sesión
    path('', views.index, name='index'),

    # Vistas de registro y validación creadas en el views.py de la app "portal_radicaciones"
    path('registro/', views.register_famedic, name='register'),
    path('verificacion/', views.token_famedic, name='token_access'),
    path('resend-token', views.resend_token, name='resend'),

    # Vistas de inicio de sesión cargadas directamente desde las librerías de Django
    path('login/', views.login_famedic, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='FamedicDesign/LogOut.html'), name='logout'),

    # Vista a menú principal de la aplicación después de haber iniciado sesión de forma correcta
    path('main/', views.hola_mundo, name='main')
]
