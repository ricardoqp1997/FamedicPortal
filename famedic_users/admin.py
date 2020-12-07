from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.mail import EmailMultiAlternatives

from .models import FamedicUser as User
from portal_radicaciones.forms import (
    UserAdminCreationForm,
    UserAdminChangeForm
)


# Función de desbloqueo de usuarios

"""
def desbloquearUsuarios(modeladmin, request, queryset):

    for user in queryset:
        user.bloqueado = user.is_active = True
        user.intentos_acceso = 0
        user.save()

desbloquearUsuarios.short_description = 'Desbloquear usuario/s'
"""


# Esta función recibe un queryset con los usuarios seleccionados
def Reenviar_correo(modeladmin, request, queryset):
    remitente = settings.EMAIL_HOST_USER

    for user in queryset:
        user.updated = False
        user.set_password('Famedic2020')
        user.phone = None
        user.save()
        # Estructura correo
        access_mail = EmailMultiAlternatives(

            from_email=remitente,
            to=[user.email],

            subject='Actalización credenciales de acceso - Famedic IPS',
            body='Sr(a). Usuario(a) del portal de proveedores.\n '

                 '\nSe realizo el correcto registro de sus datos en el portal de radicacones Famedic IPS\n'
                 '\nel cual le permitira realizar las radicaciones de su facturación, para ingresar dirijase a\n'
                 '\nhttp://proveedores.famedicips.co/login/ para realizar la actualización de datos e iniciar sesión.\n'


                 '\nSus credenciales de acceso serán: \n'
                 '\nusuario: ' + user.email + '\n'
                                              '\nContraseña: Famedic2020 \n'

                                              '\n\n Este es un mensaje automático y no es necesario responder.',
        )

        access_mail.send()


Reenviar_correo.short_description = 'Reenviar correo de actualización'


class UserAdmin(BaseUserAdmin):
    # Vinculacion de los formularios personalizados de Famedic al portal admin de Django
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    actions = [
        Reenviar_correo,
        # desbloquearUsuarios
    ]

    # Parametrización de los filtros de búsqueda y de visualización de contenido dentro de Famedic Users
    list_display = ['id_famedic', 'last_name', 'first_name', 'email', 'admin', 'updated', 'get_usuario_bloqueado']
    list_filter = ['active', 'admin', 'id_famedic', 'email']

    # Campos de información del usuario a mostrar en el panel de Famedic Users (Creación)
    add_fieldsets = (
        (
            'Credenciales', {
                'classes': ['wide', ],
                'fields': ['id_famedic', 'email', ]
            }
        ),
        (
            'Información personal del usuario', {
                'classes': ['wide', ],
                'fields': ['location', ]
            }
        ),
    )

    # Campos de información del usuario a mostrar en el panel de Famedic Users (visualización, edición y eliminación)
    fieldsets = (
        (
            'Credenciales', {
                'fields': ['id_famedic', 'email', 'recovery_email', 'password']
            }
        ),
        (
            'Información personal del usuario', {
                'fields': ['profile_foto', 'first_name', 'last_name', 'phone', 'location']
            }
        ),
        (
            'Permisos en el sitio', {
                'fields': ['updated', 'active', 'staff', 'admin']
            }
        )
    )

    # Parametros de filtrado y busqueda de usuarios en Famedic Users
    search_fields = ['email', 'id_famedic', 'first_name', 'last_name', 'phone', 'location']
    ordering = ['email', 'id_famedic']
    filter_horizontal = []

    def get_usuario_bloqueado(self, obj):
        return obj.bloqueado

    get_usuario_bloqueado.boolean = True
    get_usuario_bloqueado.short_description = 'Usuario bloqueado'

# Para incluir Famedic Users y la clase UserAdmin en el panel administrativo de Django
admin.site.register(User, UserAdmin)

# Para eliminar las secciónes que no serán necesarias
admin.site.unregister(Group)
admin.site.unregister(Site)
