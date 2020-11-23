from django.contrib import admin
from django.conf import settings
from django.contrib import messages

from .models import *
from famedic_users.models import FamedicUser

from django.http import HttpResponseRedirect, HttpResponse
from django.conf.urls import url, include
from django.urls import path

from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from import_export import resources, fields

from django.core.mail import (
    send_mail,
    EmailMessage,
    EmailMultiAlternatives
)

import xlsxwriter


class ForeignRadicado(resources.ModelResource):
    radicador = fields.Field(
        column_name='radicador',
        attribute='radicador',
        widget=ForeignKeyWidget(FamedicUser, 'email')
    )

    sede_selection = fields.Field(
        column_name='sede_selection',
        attribute='sede_selection',
        widget=ForeignKeyWidget(Sedes, 'sede_name')
    )

    glosa_asign = fields.Field(
        column_name='glosa_asign',
        attribute='glosa_asign',
        widget=ForeignKeyWidget(Sedes, 'glosa_name')
    )

    class Meta:
        model = RadicacionModel


class RadicacionAdmin(ImportExportModelAdmin):
    resource_class = ForeignRadicado

    change_form_template = 'AdminExtends/RadicadoApproval.html'

    # Parametrización de los filtros de búsqueda y de visualización de contenido
    list_display = ['id', 'id_factura', 'datetime_radicado', 'radicador', 'monto_factura', 'sede_selection', 'aproved']
    list_filter = ['aproved', 'id', 'sede_selection', 'regimen_type']

    fieldsets = (
        (
            'Revisión de la factura', {
                'classes': ['wide', 'extrapretty'],
                'fields': ['glosa_asign', 'aproved', 'obs_admin']
            }
        ),
        (
            'Datos de la factura', {
                'classes': ['wide', 'extrapretty'],
                'fields': ['datetime_radicado', 'id_factura', 'radicador',
                           'monto_factura', 'datetime_factura1', 'datetime_factura2', ]
            }
        ),
        (
            'Información adicional de la radicación', {
                'classes': ['wide', 'extrapretty'],
                'fields': ['regimen_type', 'sede_selection', 'observaciones']
            }
        ),
        (
            'Documentos adjuntos del radicado', {
                'classes': ['wide', 'extrapretty'],
                'fields': ['file_factura', 'file_aportes', 'file_soporte']
            }
        ),
        (
            'Rips adjuntos del radicado', {
                'classes': ['wide', 'extrapretty'],
                'fields': ['file_ribs']
            }
        )
    )

    readonly_fields = [
        'aproved',
        'id_factura',
        'radicador',
        'monto_factura',
        'sede_selection',
        'regimen_type',
        'observaciones',
        'file_factura',
        'file_aportes',
        'file_soporte',
        'file_ribs',
        'datetime_radicado',
        'datetime_factura1',
        'datetime_factura2',
    ]

    # Parametros de filtrado y busqueda
    search_fields = [
        'id',
        'id_factura',
        'aproved',
        'radicador__id',
        'radicador__id_famedic',
        'radicador__first_name',
        'radicador__last_name',
        'radicador__email',
        'radicador__phone',
        'sede_selection__sede_name',
        'sede_selection__locacion_sede',
        'glosa_asign__glosa_name'
    ]
    ordering = ['id', 'id_factura', 'radicador']
    filter_horizontal = []

    # save_on_top = True

    def active(self, obj):
        return obj.aproved == 1

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj):

        sender_mail = settings.EMAIL_HOST_USER
        user = FamedicUser.objects.get(email=obj.radicador)
        # test_mail = 'ricardoq@tics-sas.com'
        test_mail = 'direccioninformatica@famedicips.com'

        if '_aprove-radicado' in request.POST:

            if obj.aproved != 'SINAP':
                self.message_user(request, "El radicado ya ha sido revisado, "
                                           "no es posible cambiar su estado.", messages.ERROR)

                return HttpResponseRedirect(".")

            obj.aproved = 'RADSI'
            obj.save()

            # Correo enviado al usuario radicador
            if obj.glosa_asign:  # != 0 - sin glosa

                mail_to_user = EmailMultiAlternatives(

                    from_email=sender_mail,
                    to=[user.email, test_mail],

                    subject='Proceso Exitoso de Auditoria',

                    body='Sr(a). Usuario(a)  ' + user.get_full_name() + ', el proceso de auditoria a su solicitud de '
                                                                        'pago con numero de radicación bajo el consecutivo ' + str(
                        obj.id) + ', culminó exitosamente '
                                  'con las siguientes observaciones:'

                                  '\n\n' + obj.obs_admin + '\n\n'

                                                           '\n\nDe no haberse generado diferencia contractual alguna descrita en observaciones, su '
                                                           'solicitud continua con el proceso para pago.\n\n'

                                                           '\n\nDe haberse generado glosa descrita en observaciones SERVICIOS MEDICOS FAMEDIC SAS se '
                                                           'permite notificar que la presente glosa que se relaciona a continuación, debe ser subsanada '
                                                           'dentro de los quince (15) días hábiles siguientes a su recepción, o se dará como aceptada. '
                                                           'De acuerdo al decreto Numero 4747 de diciembre de 2007, por medio del cual se regulan '
                                                           'algunos aspectos de las relaciones entre los prestadores de servicios de salud y las '
                                                           'entidades responsables del pago de la población a su cargo. \n\n'

                                                           '\n\n Este es un mensaje automático y no es necesario responder.',
                )

            else:  # == 0 - sin glosa

                self.message_user(request,
                                  "Es necesario seleccionar un elemento de la lista glosa si va a realizar la aprobación del radicado. Para aprobar sin glosa, seleccione el elemento: 0-Aprobada Sin Glosa")
                return HttpResponseRedirect(".")

            mail_to_user.send()

            self.message_user(request, "Se ha cambiado el estado del radicado a: Aprobado")
            return HttpResponseRedirect(".")

        if '_reject-radicado' in request.POST:

            if obj.aproved != 'SINAP':
                self.message_user(request, "El radicado ya ha sido revisado, "
                                           "no es posible cambiar su estado.", messages.ERROR)

                return HttpResponseRedirect(".")

            obj.aproved = 'RADNO'
            obj.save()

            # Correo enviado al usuario radicador
            if obj.obs_admin:

                mail_to_user = EmailMultiAlternatives(

                    from_email=sender_mail,
                    to=[user.email, test_mail],

                    subject='Proceso Devolución solicitud bajo radicado Nro ' + str(obj.id) + '.',

                    body='Sr(a). Usuario(a) ' + user.get_full_name() + ', su solicitud de pago con numero de radicación '
                                                                       'bajo el consecutivo “ ” no cumple con los  requisitos mínimos para realizar un proceso de '
                                                                       'auditoria y pago, razón por la cual se realiza la devolución total para que sean subsanadas '
                                                                       'las causales que se relacionan a continuación y se vuelva a radicar nuevamente.\n\n'

                                                                       ' Durante la revisión se indicaron los siguientes comentarios: \n\n'

                         + obj.obs_admin + '\n\n'

                                           '\n\n Lo anterior de acuerdo con el decreto Numero 4747 de diciembre de 2007, por medio del '
                                           'cual se regulan algunos aspectos de las relaciones entre los prestadores de servicios de '
                                           'salud y las entidades responsables del pago de la población a su cargo.'

                                           '\n\n Este es un mensaje automático y no es necesario responder.',
                )

            else:
                mail_to_user = EmailMultiAlternatives(

                    from_email=sender_mail,
                    to=[user.email, test_mail],

                    subject='Proceso Devolución solicitud bajo radicado Nro ' + str(obj.id) + '.',

                    body='Sr(a). Usuario(a) ' + user.get_full_name() + ', su solicitud de pago con numero de radicación '
                                                                       'bajo el consecutivo “ ” no cumple con los  requisitos mínimos para realizar un proceso de '
                                                                       'auditoria y pago, razón por la cual se realiza la devolución total para que sean subsanadas '
                                                                       'las causales que se relacionan a continuación y se vuelva a radicar nuevamente.'

                                                                       '\n\n Lo anterior de acuerdo con el decreto Numero 4747 de diciembre de 2007, por medio del '
                                                                       'cual se regulan algunos aspectos de las relaciones entre los prestadores de servicios de '
                                                                       'salud y las entidades responsables del pago de la población a su cargo.'

                                                                       '\n\n Este es un mensaje automático y no es necesario responder.',
                )

            mail_to_user.send()

            self.message_user(request, "Se ha cambiado el estado del radicado a: No aprobado")
            return HttpResponseRedirect(".")

        if '_revert-radicado' in request.POST:

            if obj.aproved == 'SINAP':
                self.message_user(request, "No es posible revertir cambios, "
                                           "el radicado está sin revisar.", messages.ERROR)
                return HttpResponseRedirect(".")

            obj.aproved = 'SINAP'
            obj.save()

            mail_to_user = EmailMultiAlternatives(

                from_email=sender_mail,
                to=[user.email, test_mail],

                subject='Estado de revisión de radicado restaurado - Famedic IPS',
                body='Sr(a). Moderador(a).\n '

                     'Se le indica que el administrador ' + request.user.get_mail() + ' realizó'
                                                                                      ' reversión de cambios en el estado del radicado ' + str(
                    obj.id) + '.'

                              '\n\n Este es un mensaje automático y no es necesario responder.',
            )

            mail_to_user.send()

            self.message_user(request, "Se ha restablecido la revision del radicado", messages.WARNING)
            return HttpResponseRedirect(".")

        return super().response_change(request, obj)

    # -----------------------------------------------------------------------------------------------------------------

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('immortal/', self.set_immortal, name='admin_test'),
        ]
        return my_urls + urls

    def set_immortal(self, request):

        self.message_user(request, "Informe de radicaciones exportado")
        return HttpResponseRedirect("../")


class LocacionAdmin(admin.ModelAdmin):
    # Parametrización de los filtros de búsqueda y de visualización de contenido
    list_display = ['id', 'municipio', 'locacion_name', 'locacion_status']
    list_filter = ['id', 'municipio', 'locacion_name', 'locacion_status']

    fieldsets = (
        (
            'Datos básicos de la locación', {
                'classes': ['wide', ],
                'fields': ['locacion_name', 'municipio']
            }
        ),
        (
            'Revisión de estado de la locación', {
                'classes': ['wide', ],
                'fields': ['locacion_status']
            }
        )
    )

    # Parametros de filtrado y busqueda
    search_fields = ['id', 'locacion_name', 'locacion_status']
    ordering = ['id', 'locacion_name', 'locacion_status']
    filter_horizontal = []


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


