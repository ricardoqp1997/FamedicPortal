from django.db import models
from famedic_users.models import FamedicUser


# Clase para el manejo de formularios de radicación
class RadicacionModel(models.Model):

    # Selección de régimen
    REGIMEN_CHOICES = [
        ('CT', 'Contributivo'),
        ('SB', 'Subsidiario'),
    ]

    # Selección de sede
    SEDE_CHOICES = [
        ('FMETA', 'FAMEDIC - IPS'),
        ('FCESP', 'FAMEDIC - IPS CENTRO ESPECIALISTAS'),
        ('FBASI', 'FAMEDIC - IPS BÁSICA'),
        ('FAPYP', 'FAMEDIC - PYP'),
        ('FVILL', 'FAMELAB - VILLAVICENCIO'),
        ('FACAC', 'FAMEDIC - IPS ACACIAS'),
        ('FPLPZ', 'FAMEDIC - IPS PUERTO LÓPEZ'),
        ('FGRAN', 'FAMEDIC - IPS GRANADA'),
        ('FPGTN', 'FAMEDIC - IPS PUERTO GAITÁN'),
        ('FCASN', 'FAMEDIC - IPS CASANARE'),
        ('FLIBR', 'FAMEDIC - IPS LIBERTADORES'),
        ('FVMSR', 'FAMELAB - VITAL MEDICAL SERVICE'),
        ('FARAU', 'FAMEDIC - IPS ARAUCA'),
        ('FTAME', 'FAMEDIC - TAME'),
        ('FTUNJ', 'FAMEDIC - IPS TUNJA'),
        ('FDUIT', 'FAMEDIC - IPS DUITAMA'),
        ('FSOGA', 'FAMEDIC - IPS SOGAMOSO'),
        ('FCHIQ', 'FAMEDIC - IPS CHIQUINQUIRÁ'),
    ]

    # Que usuario realizó la radicación
    radicador = models.ForeignKey(FamedicUser, blank=True, null=True, on_delete=models.CASCADE)

    # Números identificadores únicos de la factura
    id_factura = models.IntegerField(verbose_name='número de factura', unique=True)

    # Monto de factura a radicar
    monto_factura = models.IntegerField(verbose_name='monto de la factura')

    # Archivos requeridos para la tramitación
    file_factura = models.FileField(verbose_name='factura')
    file_aportes = models.FileField(verbose_name='aportes')
    file_soporte = models.FileField(verbose_name='soportes de factura')
    file_ribs = models.FileField(verbose_name='ribs')

    # Campo para asignación de tipo de regimen
    regimen_type = models.CharField(verbose_name='regimen', max_length=2, choices=REGIMEN_CHOICES, default=REGIMEN_CHOICES[0])

    # Campo para asignación de sede
    sede_select = models.CharField(verbose_name='sede correspondiente', max_length=5, choices=SEDE_CHOICES, default=SEDE_CHOICES[0])

    # Campo de observaciones adicionales para diligenciar
    observaciones = models.TextField(verbose_name='observaciones')

    # Validación de aprobación del radicado
    aproved = models.BooleanField(verbose_name=' radicado aprovado', default=False)

    REQUIRED_FIELDS = [
        'id_radicado',
        'id_factura',
        'monto_factura',
        'file_factura',
        'file_aportes',
        'file_soporte',
        'file_ribs',
        'regimen_type',
        'sede_select'
    ]

    def __str__(self):
        return str(self.id_factura)

    @property
    def is_aproved(self):
        return self.aproved
