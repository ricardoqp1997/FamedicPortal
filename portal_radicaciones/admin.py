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


"""class ForeignRadicado(resources.ModelResource):
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
        model = RadicacionModel"""


class RadicacionDespacho(resources.ModelResource):

    numero_radicado = fields.Field(column_name='Consecutivo del radicado', attribute='id')
    numero_factura = fields.Field(column_name='Numero de factura', attribute='id_factura')
    nombre_radicador = fields.Field(column_name='Nombre de radicador')
    tipo_id_radicador = fields.Field(column_name='Tipo de documento')
    id_radicador = fields.Field(column_name='Número de documento')
    telefono_radicador = fields.Field(column_name='Telefono radicador')
    fecha_factura = fields.Field(column_name='Fecha de radicación de la factura', attribute='datetime_radicado')
    periodo_factura = fields.Field(column_name='Periodo de facturación')
    monto_factura = fields.Field(column_name='Monto de factura', attribute='monto_factura')
    sede_radicado = fields.Field(column_name='Sede radicadora')
    estado_radicado = fields.Field(column_name='Estado del radicado')
    glosa_radicado = fields.Field(column_name='Glosa')
    subglosa_radicado = fields.Field(column_name='Subglosa')
    valor_glosa = fields.Field(column_name='Valor de glosa', attribute='glosa_valor')
    neto_a_pagar = fields.Field(column_name='Neto a pagar')

    class Meta:
        model = RadicacionModel

        fields = [
            'nombre_radicador',
            'tipo_id_radicador',
            'id_radicador',
            'telefono_radicador',
            'numero_radicado',
            'numero_factura',
            'fecha_factura',
            'periodo_factura',
            'monto_factura',
            'sede_radicado',
            'estado_radicado',
            'glosa_radicado',
            'subglosa_radicado',
            'valor_glosa',

        ]

        export_order = fields

    @staticmethod
    def dehydrate_nombre_radicador(radicado):
        return radicado.radicador.get_full_name()

    @staticmethod
    def dehydrate_tipo_id_radicador(radicado):
        return radicado.radicador.id_type

    @staticmethod
    def dehydrate_id_radicador(radicado):
        return radicado.radicador.id_famedic

    @staticmethod
    def dehydrate_telefono_radicador(radicado):
        if radicado.radicador.phone:
            return radicado.radicador.phone
        else:
            return 'Sin teléfono inscrito'

    @staticmethod
    def dehydrate_sede_radicado(radicado):
        return radicado.sede_selection.sede_name

    @staticmethod
    def dehydrate_estado_radicado(radicado):
        return radicado.get_aproved_display()

    @staticmethod
    def dehydrate_glosa_radicado(radicado):
        try:
            return radicado.glosa_asign.glosa_name
        except:
            return 'Sin glosa asignada'

    @staticmethod
    def dehydrate_subglosa_radicado(radicado):
        try:
            return radicado.subglosa_asign.Subglosa_name
        except:
            return 'Sin subglosa asignada'

    @staticmethod
    def dehydrate_periodo_factura(radicado):
        return str(radicado.datetime_factura1) + ' - ' + str(radicado.datetime_factura2)

    @staticmethod
    def dehydrate_neto_a_pagar(radicado):
        try:
            return radicado.monto_factura - radicado.glosa_valor
        except:
            return radicado.monto_factura


class RadicacionAdmin(ImportExportModelAdmin):
    resource_class = RadicacionDespacho  # ForeignRadicado

    change_form_template = 'AdminExtends/RadicadoApproval.html'

    subglosa_radicado = fields.Field(column_name='Subglosa')
    valor_glosa = fields.Field(column_name='Valor de glosa', attribute='glosa_valor')

    # Parametrización de los filtros de búsqueda y de visualización de contenido
    list_display = [
        'id',
        'id_factura',
        'get_nombre_radicador',
        'get_tipo_id_radicador',
        'get_id_radicador',
        'get_telefono_radicador',
        'datetime_radicado',
        'get_periodo_factura',
        'monto_factura',
        'get_sede_radicado',
        'aproved',
        'get_glosa_radicado',
        'get_subglosa_radicado',
        'glosa_valor',
        'get_neto_a_pagar'
    ]
    list_filter = ['aproved', 'radicador__id_famedic', 'id', 'sede_selection', 'regimen_type']

    fieldsets = (
        (
            'Revisión de la factura', {
                'classes': ['wide', 'extrapretty'],
                'fields': ['glosa_asign', 'subglosa_asign', 'glosa_valor', 'aproved', 'obs_admin']
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
        'id',                         # Consecutovo
        'id_factura',                 # Numero asignado de factura
        'aproved',                    # Radicados aprobados
        'radicador__id_famedic',      # Cedula
        'radicador__email',           # Correo electronico
        'sede_selection__sede_name',  # Sede
        'regimen_type',               # Regimen
    ]
    ordering = ['id', 'id_factura', 'radicador']
    filter_horizontal = []

    # save_on_top = True

    def get_nombre_radicador(self, obj):
        return obj.radicador.get_full_name()

    def get_tipo_id_radicador(self, obj):
        return obj.radicador.id_type

    def get_id_radicador(self, obj):
        return obj.radicador.id_famedic

    def get_telefono_radicador(self, obj):
        if obj.radicador.phone:
            return obj.radicador.phone
        else:
            return 'Sin teléfono inscrito'

    def get_sede_radicado(self, obj):
        return obj.sede_selection.sede_name

    def get_estado_radicado(self, obj):
        return obj.get_aproved_display()

    def get_glosa_radicado(self, obj):
        try:
            return obj.glosa_asign.glosa_name
        except:
            return 'Sin glosa asignada'

    def get_subglosa_radicado(self, obj):
        try:
            return obj.subglosa_asign.Subglosa_name
        except:
            return 'Sin subglosa asignada'

    def get_periodo_factura(self, obj):
        return str(obj.datetime_factura1.date()) + ' - ' + str(obj.datetime_factura2.date())

    def get_neto_a_pagar(self, obj):
        try:
            return obj.monto_factura - obj.glosa_valor
        except:
            return obj.monto_factura

    get_nombre_radicador.short_description = 'Nombre de radicador'
    get_tipo_id_radicador.short_description = 'Tipo de documento'
    get_id_radicador.short_description = 'Número de documento'
    get_telefono_radicador.short_description = 'Teléfono del contacto'
    get_sede_radicado.short_description = 'Sede de radicación'
    get_estado_radicado.short_description = 'Estado del radicado'
    get_glosa_radicado.short_description = 'Glosa'
    get_subglosa_radicado.short_description = 'Subglosa'
    get_periodo_factura.short_description = 'Periodo de facturación'
    got_get_neto_a_pagar = 'Neto a pagar'

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
        test_mail = 'radicacion@famedicips.com'

        if '_aprove-radicado' in request.POST:
            
            if (obj.glosa_asign.glosa_name != '0-Aprobada Sin Glosa') \
                    or (obj.subglosa_asign.Subglosa_name != '0-Aprobada Sin SubGlosa')\
                    or (obj.glosa_valor is not None):
                self.message_user(request, 'Esto es una radicación sin glosa'
                                  ' por favor, desmarque la opción', messages.ERROR)

                return HttpResponseRedirect(".")

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
                    to=[user.email],

                    subject='Proceso Exitoso de Auditoria',

                    body='Sr(a). Usuario(a)  ' + user.get_full_name() + ', el proceso de auditoria a su solicitud de '
                                                                        'pago con numero de radicación bajo el consecutivo ' + str(
                        obj.id) + ', culminó exitosamente '
                                  'sin diferencia contractual alguna. Se procederá a remitir al proceso de auditoria médica'

                                  '\n\n' + obj.obs_admin + '\n\n'

                                  '\n\n Si posterior a este mensaje no recibe glosa por auditoria médica, el valor total '
                                  'se remitirá a procesamiento para pago.\n\n'

                                  '\n\nCualquier duda o inquietud con gusto será resuleta en los correos '
                                  'direccionoperativa@famedicips.com y radicacion@famedicips.com \n\n'

                                  '\n\n Este es un mensaje automático y no es necesario responder.',
                )

            else:  # == 0 - sin glosa

                self.message_user(request,
                                  "Es necesario seleccionar un elemento de la lista glosa si va a realizar la aprobación del radicado. Para aprobar sin glosa, seleccione el elemento: 0-Aprobada Sin Glosa")
                return HttpResponseRedirect(".")

            mail_to_user.send()

            self.message_user(request, "Se ha cambiado el estado del radicado a: Aprobado")
            return HttpResponseRedirect(".")

        # ------------ Aprobación con glosa ---------------------


        if '_glosa-radicado' in request.POST: 

            if (obj.glosa_asign.glosa_name == '0-Aprobada Sin Glosa') \
                    or (obj.subglosa_asign.Subglosa_name == '0-Aprobada Sin SubGlosa') \
                    or (obj.glosa_valor is None):
                    self.message_user(request, 'Debe asignar una glosa al radicado y especificarle un valor', messages.ERROR)
                        
                    return HttpResponseRedirect(".")
                
            if (obj.glosa_valor > obj.monto_factura):
                self.message_user(request, 'Asigne un valor inferior al valor'
                                       ' de la facturación correspondiente', messages.ERROR)
                return HttpResponseRedirect(".")

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
                    to=[user.email],

                    subject='Proceso de Auditoria con diferencias contractuales o normativas (glosa)',

                    body='Sr(a). Usuario(a)  ' + user.get_full_name() + ', su solicitud de pago con numero de radicación bajo el consecutivo '
                                                                        + str(
                        obj.id) + ', presenta glosa por valor de: \n\n' + str(obj.glosa_valor) + 
                                    '\n\n Observaciones del administrador: \n\n'
                                    '\n\n' + obj.obs_admin + '\n\n'

                                                           '\n\nSERVICIOS MEDICOS FAMEDIC SAS se permite notificar que la presente glosa '
                                                           ' que se relaciona a continuación, debe ser subsanada dentro de los quince (15) días '
                                                           ' hábiles siguientes a su recepción, o se dará como aceptada. '
                                                           ' Los soportes que subsanen la glosa se deben remitir al correo: direccionoperativa@famedicips.com '
                                                           ' radicacion@famedicips.com \n\n'
                                                           
                                                           '\n\nCausal y subcausal escogida '
                                                          
                                                           ' De acuerdo al decreto Numero 4747 de diciembre de 2007, '
                                                           ' por medio del cual se regulan algunos aspectos de las '
                                                           ' relaciones entre los prestadores de servicios de salud '
                                                           ' y las entidades responsables del pago de la población a '
                                                           ' su cargo. \n\n'

                                                           
                                                           '\n\n Este es un mensaje automático y no es necesario responder.',
                )

            else:# == 0 - sin glosa
                self.message_user(request,'Es necesario seleccionar un elemento de la lista '
                    ' glosa si va a realizar la aprobación del radicado. Para aprobar sin glosa, '
                    ' seleccione el elemento: 0-Aprobada Sin Glosa \n\n')
                    
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
                    to=[user.email],

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
                    to=[user.email],

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
                to=[user.email],

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
    list_filter = ['id', 'glosa_name',  'glosa_status']

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


class SubglosaAdmin(admin.ModelAdmin):

    # Parametrización de los filtros de búsqueda y de visualización de contenido
    list_display = ['id', 'Subglosa_name', 'subglosa_status']
    list_filter = ['id', 'Subglosa_name',  'subglosa_status']

    fieldsets = (
        (
            'Datos básicos de la Subglosa', {
                'classes': ['wide', ],
                'fields': ['glosa', 'Subglosa_name']
            }
        ),
        (
            'Revisión de estado de la Subglosa', {
                'classes': ['wide', ],
                'fields': ['subglosa_status']
            }
        )
    )

    # Parametros de filtrado y busqueda
    search_fields = ['id', 'Subglosa_name', 'subglosa_status']
    ordering = ['id', 'Subglosa_name', 'subglosa_status']
    filter_horizontal = []
