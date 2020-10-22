from django.contrib import admin
from django.conf import settings
from django.contrib import messages

from .models import *
from famedic_users.models import FamedicUser

from django.http import HttpResponseRedirect

from django.core.mail import (
    send_mail,
    EmailMessage,
    EmailMultiAlternatives
)


class RadicacionAdmin(admin.ModelAdmin):

    change_form_template = 'AdminExtends/RadicadoApproval.html'

    # Parametrización de los filtros de búsqueda y de visualización de contenido
    list_display = ['id', 'id_factura', 'radicador', 'monto_factura', 'sede_selection', 'aproved']
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

    def active(self, obj):
        return obj.aproved == 1

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def response_change(self, request, obj):

        sender_mail = settings.EMAIL_HOST_USER
        user = FamedicUser.objects.get(email=obj.radicador)
        test_mail = 'ricardoq@tics-sas.com'
        # test_mail = 'direccioninformatica@famedicips.com'

        if '_aprove-radicado' in request.POST:

            if obj.aproved != 'SINAP':

                self.message_user(request, "El radicado ya ha sido revisado, "
                                           "no es posible cambiar su estado.", messages.ERROR)

                return HttpResponseRedirect(".")

            obj.aproved = 'RADSI'
            obj.save()

            # Correo enviado al usuario radicador
            if obj.obs_admin:

                mail_to_user = EmailMultiAlternatives(

                    from_email=sender_mail,
                    to=[user.email, test_mail],

                    subject='Notificación de radicación aprobada - Famedic IPS',
                    body='Sr(a). ' + user.get_full_name() + '.\n '
        
                         '\nSe le notifica que el radicado con número ' + str(obj.id) + ' que usted realizó '
                         'fué revisado y aprovado por los administradores del portal de radicaciones de Famedic IPS. '
                         
                         ' Durante la revisión se indicaron los siguientes comentarios: \n\n'

                         + obj.obs_admin + '\n\n'                                                              
                         
                         'Con dicha validación el proceso de radicación ha finalizado correctamente. \n'
        
                         '\n\n Este es un mensaje automático y no es necesario responder.',
                )

            else:
                mail_to_user = EmailMultiAlternatives(

                    from_email=sender_mail,
                    to=[user.email, test_mail],

                    subject='Notificación de radicación aprobada - Famedic IPS',
                    body='Sr(a). ' + user.get_full_name() + '.\n\n'

                         '\nSe le notifica que el radicado con número ' + str(obj.id) + ' que usted realizó '
                         'fué revisado y aprovado por los administradores del portal de radicaciones de Famedic IPS. '

                         'Con dicha validación el proceso de radicación ha finalizado correctamente. \n'

                         '\n\n Este es un mensaje automático y no es necesario responder.',
                )

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

                    subject='Notificación de radicación rechazada - Famedic IPS',
                    body='Sr(a). ' + user.get_full_name() + '.\n '
    
                         '\nSe le notifica que el radicado con número ' + str(obj.id) + ' que usted realizó '
                         'fué revisado y no fue aprobado por no cumplir con todos los requisitos.'
                                                                                        
                         ' Durante la revisión se indicaron los siguientes comentarios: \n\n'

                         + obj.obs_admin + '\n\n'
                                                                                        
                         'Debido a l resultado negativo en la revisión de su radicado será necesario'
                         'que realice el proceso nuevamente. \n'
    
                         '\n\n Este es un mensaje automático y no es necesario responder.',
                )

            else:
                mail_to_user = EmailMultiAlternatives(

                    from_email=sender_mail,
                    to=[user.email, test_mail],

                    subject='Notificación de radicación rechazada - Famedic IPS',
                    body='Sr(a). ' + user.get_full_name() + '.\n '

                         '\nSe le notifica que el radicado con número ' + str(
                        obj.id) + ' que usted realizó '
                                  'fué revisado y no fue aprobado por no cumplir con todos los requisitos.'

                                  'El administrador del portal de radicaciónes rechazó su radicado y será necesario'
                                  'que realice el proceso nuevamente. \n'

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
                     ' reversión de cambios en el estado del radicado ' + str(obj.id) + '.' 
                     
                     '\n\n Este es un mensaje automático y no es necesario responder.',
            )

            mail_to_user.send()

            self.message_user(request, "Se ha restablecido la revision del radicado", messages.WARNING)
            return HttpResponseRedirect(".")

        return super().response_change(request, obj)


class LocacionAdmin(admin.ModelAdmin):

    # Parametrización de los filtros de búsqueda y de visualización de contenido
    list_display = ['id', 'municipio',  'locacion_name', 'locacion_status']
    list_filter = ['id', 'municipio',  'locacion_name', 'locacion_status']

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
