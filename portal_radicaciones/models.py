from django.db import models
from famedic_users.models import FamedicUser


# Clase para el manejo de formularios de radicación
class RadicacionModel(models.Model):

    # Que usuario realizó la radicación
    radicador = models.ForeignKey(FamedicUser, blank=True, null=True, on_delete=models.CASCADE)

    # Número identificador único de factura
    id_factura = models.IntegerField(verbose_name='número de factura', unique=True)

    # Monto de factura a radicar
    monto_factura = models.IntegerField(verbose_name='monto de la factura')

    # Archivos requeridos para la tramitación
    file_factura = models.FileField(verbose_name='factura')
    file_aportes = models.FileField(verbose_name='aportes')
    file_soporte = models.FileField(verbose_name='soportes de factura')
    file_ribs = models.FileField(verbose_name='ribs')

    # Campo de observaciones adicionales para diligenciar
    observaciones = models.TextField(verbose_name='observaciones')

    # Validación de aprobación del radicado
    aproved = models.BooleanField(verbose_name=' radicado aprovado', default=False)

    REQUIRED_FIELDS = [
        'id_factura',
        'monto_factura',
        'file_factura',
        'file_aportes',
        'file_soporte',
        'file_ribs'
    ]

    def __str__(self):
        return str(self.id_factura)

    @property
    def is_aproved(self):
        return self.aproved
