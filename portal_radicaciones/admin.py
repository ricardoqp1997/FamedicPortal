from django.contrib import admin
from .models import RadicacionModel, Glosa


class RadicacionAdmin(admin.ModelAdmin):

    # Parametrización de los filtros de búsqueda y de visualización de contenido dentro de Famedic Users
    list_display = ['id', 'id_factura', 'radicador', 'monto_factura', 'aproved']
    list_filter = ['aproved', 'id', 'sede_select', 'regimen_type']

    # Parametros de filtrado y busqueda de usuarios en Famedic Users
    search_fields = ['id', 'id_factura', 'radicador']
    ordering = ['id_factura', 'id']
    filter_horizontal = []

    def active(self, obj):
        return obj.aproved == 1


admin.site.register(RadicacionModel, RadicacionAdmin)
admin.site.register(Glosa)
