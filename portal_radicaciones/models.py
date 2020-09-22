from django.db import models
from famedic_users.models import FamedicUser
from datetime import datetime
import pytz




class Locacion(models.Model):

    LOCACION_ACTIVA = True
    LOCACION_INACTIVA = False

    STATUS_CHOICES = [
        (LOCACION_ACTIVA, 'Locación activa'),
        (LOCACION_INACTIVA, 'Locación inactiva')
    ]

    locacion_name = models.CharField(verbose_name='nombre de la locación', max_length=50, default='Arauca')
    locacion_status = models.BooleanField(verbose_name='estado activo de la locación', choices=STATUS_CHOICES,
                                          default=LOCACION_ACTIVA)

    REQUIRED_FIELD = [
        'locacion_name'
    ]

    class Meta:
        verbose_name = 'Sitio'

    def __str__(self):
        return self.locacion_name


class Sedes(models.Model):
    # Selección de estado activo de la sede
    SEDE_ACTIVA = True
    SEDE_INACTIVA = False

    STATUS_CHOICES = [
        (SEDE_ACTIVA, 'Sede activa'),
        (SEDE_INACTIVA, 'Sede inactiva')
    ]

    sede_name = models.CharField(verbose_name='nombre de la sede', max_length=50, default='FAMEDIC - IPS')
    locacion_sede = models.ForeignKey(Locacion, blank=True, null=True, on_delete=models.SET_NULL,
                                      verbose_name='locación de la sede')
    address_sede = models.CharField(verbose_name='dirección', max_length=50, blank=True)
    sede_status = models.BooleanField(verbose_name='estado activo de la sede',
                                      choices=STATUS_CHOICES, default=SEDE_ACTIVA)

    REQUIRED_FIELD = [
        'sede_name'
    ]

    class Meta:
        verbose_name = 'Sede'

    def __str__(self):
        return self.sede_name


class Glosa(models.Model):
    # Selección de estado activo de la glosa
    GLOSA_ACTIVA = True
    GLOSA_INACTIVA = False

    STATUS_CHOICES = [
        (GLOSA_ACTIVA, 'Glosa activa'),
        (GLOSA_INACTIVA, 'Glosa inactiva')
    ]

    glosa_name = models.CharField(verbose_name='nombre de glosa', max_length=25, default='glosa')
    glosa_status = models.BooleanField(verbose_name='estado de la glosa',
                                       choices=STATUS_CHOICES, default=GLOSA_ACTIVA)

    REQUIRED_FIELD = [
        'glosa_name'
    ]

    class Meta:
        verbose_name = 'Glosa'

    def __str__(self):
        return self.glosa_name


# Clase para el manejo de formularios de radicación
class RadicacionModel(models.Model):

    # Selección de estado de radicado
    RAD_UNVERIFIED = 'SINAP'
    RAD_APROVED = 'RADSI'
    RAD_DISAPROVED = 'RADNO'

    STATUS_CHOICES = [
        (RAD_UNVERIFIED, 'Sin verificar'),
        (RAD_APROVED, 'Radicado aprobado'),
        (RAD_DISAPROVED, 'Radicado no aprobado')
    ]

    # Selección de régimen
    REGIMEN_CHOICES = [
        ('CT', 'Contributivo'),
        ('SB', 'Subsidiario'),
    ]

    # Que usuario realizó la radicación
    radicador = models.ForeignKey(FamedicUser, blank=True, null=True, on_delete=models.SET_NULL)

    # Números identificadores únicos de la factura
    id_factura = models.IntegerField(verbose_name='número de factura')

    # Monto de factura a radicar
    monto_factura = models.IntegerField(verbose_name='monto de la factura')

    # Documentos requeridos para el radicado
    file_factura = models.FileField(verbose_name='factura')
    file_aportes = models.FileField(verbose_name='aportes')
    file_soporte = models.FileField(verbose_name='soportes de factura')

    # Rips adjuntos al radicado
    file_ribs1 = models.FileField(verbose_name='rip 1', blank=True)
    file_ribs2 = models.FileField(verbose_name='rip 2', blank=True)
    file_ribs3 = models.FileField(verbose_name='rip 3', blank=True)
    file_ribs4 = models.FileField(verbose_name='rip 4', blank=True)

    # Campo para asignación de tipo de regimen
    regimen_type = models.CharField(verbose_name='regimen', max_length=2, choices=REGIMEN_CHOICES,
                                    default=REGIMEN_CHOICES[0])

    # Campo para asignación de sede
    sede_selection = models.ForeignKey(Sedes, blank=True, null=True, on_delete=models.SET_NULL,
                                       verbose_name='sede correspondiente')

    # Campo de observaciones adicionales para diligenciar
    observaciones = models.TextField(verbose_name='observaciones')

    # Validación de aprobación del radicado
    aproved = models.CharField(verbose_name='estado de radicado', max_length=5, default=RAD_UNVERIFIED,
                               choices=STATUS_CHOICES)
    obs_admin = models.TextField(verbose_name='observaciones del administrador', blank=True, null=True)

    # Campo para asignacion de glosa
    glosa_asign = models.ForeignKey(Glosa, blank=True, null=True, on_delete=models.SET_NULL, verbose_name='glosa')

    # Fecha de registro del radicado
    datetime_radicado = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='fecha de radicación')

    REQUIRED_FIELDS = [
        'id_factura',
        'monto_factura',

        'file_factura',
        'file_aportes',
        'file_soporte',

        'file_ribs1',
        'file_ribs2',
        'file_ribs3',
        'file_ribs4',

        'regimen_type',
        'sede_selection'
    ]

    # métodos base del modelo
    class Meta:
        verbose_name = 'Radicado'

    def __str__(self):
        return str(self.id_factura)

    # propiedades del modelo
    @property
    def is_aproved(self):
        return self.aproved
