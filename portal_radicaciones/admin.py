from django.contrib import admin
from .models import RadicacionModel, Glosa, Sedes
from .forms import RadicacionForm


class RadicacionAdmin(admin.ModelAdmin):

    # Parametrización de los filtros de búsqueda y de visualización de contenido
    list_display = ['id', 'id_factura', 'radicador', 'monto_factura', 'aproved']
    list_filter = ['aproved', 'id', 'sede_select', 'regimen_type']

    fieldsets = (
        (
            'Revisión de la factura', {
                'classes': ['wide', ],
                'fields': ['aproved', 'glosa_asign']
            }
        ),
        (
            'Datos de la factura', {
                'classes': ['wide', ],
                'fields': ['id_factura', 'radicador', 'monto_factura']
            }
        ),
        (
            'Información adicional de la radicación', {
                'classes': ['wide', ],
                'fields': ['regimen_type', 'sede_select', 'observaciones']
            }
        ),
        (
            'Documentos adjuntos', {
                'classes': ['wide', ],
                'fields': ['file_factura', 'file_aportes', 'file_soporte', 'file_ribs']
            }
        )
    )

    readonly_fields = [
        'id_factura',
        'radicador',
        'monto_factura',
        'sede_select',
        'regimen_type',
        'observaciones',
        'file_factura',
        'file_aportes',
        'file_soporte',
        'file_ribs'
    ]

    # Parametros de filtrado y busqueda
    search_fields = ['id', 'id_factura', 'radicador']
    ordering = ['id_factura', 'id']
    filter_horizontal = []

    def active(self, obj):
        return obj.aproved == 1

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(RadicacionModel, RadicacionAdmin)


class SedesAdmin(admin.ModelAdmin):

    # Parametrización de los filtros de búsqueda y de visualización de contenido
    list_display = ['id', 'sede_name', 'locacion_sede', 'address_sede', 'sede_status']
    list_filter = ['id', 'sede_name', 'sede_status']

    fieldsets = (
        (
            'Datos básicos de la sede', {
                'classes': ['wide', ],
                'fields': ['sede_name', 'locacion_sede', 'address_sede']
            }
        ),
        (
            'Revisión de estado de la sede', {
                'classes': ['wide', ],
                'fields': ['sede_status']
            }
        )
    )

    # Parametros de filtrado y busqueda
    search_fields = ['id', 'sede_name', 'locacion_sede']
    ordering = ['id', 'sede_name']
    filter_horizontal = []


admin.site.register(Sedes, SedesAdmin)


class GlosaAdmin(admin.ModelAdmin):
    # Parametrización de los filtros de búsqueda y de visualización de contenido
    list_display = ['id', 'glosa_name', 'glosa_status']
    list_filter = ['id', 'glosa_name', 'glosa_status']

    fieldsets = (
        (
            'Datos básicos de la glosa', {
                'classes': ['wide', ],
                'fields': ['glosa_name']
            }
        ),
        (
            'Revisión de estado de la glosa', {
                'classes': ['wide', ],
                'fields': ['glosa_status']
            }
        )
    )

    # Parametros de filtrado y busqueda
    search_fields = ['id', 'glosa_name', 'glosa_status']
    ordering = ['id', 'glosa_name', 'glosa_status']
    filter_horizontal = []


admin.site.register(Glosa, GlosaAdmin)
