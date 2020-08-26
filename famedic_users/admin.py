from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import FamedicUser as User
from portal_radicaciones.forms import (
    UserAdminCreationForm,
    UserAdminChangeForm
)

# Personalización de titulo y nombre del sitio de administración Django acorde a Famedic IPS
admin.site.site_header = 'Panel administrativo: Famedic'
admin.site.site_title = 'Famedic IPS'


class UserAdmin(BaseUserAdmin):

    # Vinculacion de los formularios personalizados de Famedic al portal admin de Django
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # Parametrización de los filtros de búsqueda y de visualización de contenido dentro de Famedic Users
    list_display = ['id_famedic', 'last_name', 'first_name', 'email', 'admin']
    list_filter = ['active', 'admin', 'id_famedic', 'email']

    # Campos de información del usuario a mostrar en el panel de Famedic Users (Creación)
    add_fieldsets = (
        (
            'Credenciales', {
                'classes': ['wide', ],
                'fields': ['id_famedic', 'email', 'password1', 'password2']
            }
        ),
        (
            'Información personal del usuario', {
                'classes': ['wide', ],
                'fields': ['location', 'first_name', 'last_name', 'phone', 'recovery_email']
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
                'fields': ['active', 'staff', 'admin']
            }
        )
    )

    # Parametros de filtrado y busqueda de usuarios en Famedic Users
    search_fields = ['email', 'id_famedic']
    ordering = ['email', 'id_famedic']
    filter_horizontal = []


# Para incluir Famedic Users y la clase UserAdmin en el panel administrativo de Django
admin.site.register(User, UserAdmin)

# Para eliminar las secciónes que no serán necesarias
admin.site.unregister(Group)
admin.site.unregister(Site)
