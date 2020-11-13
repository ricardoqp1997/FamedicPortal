# Librerías de Django para el manejo de las vistas, plantillas y navegación
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from datetime import date, time, datetime, timedelta

# Librería para restricción de vistas con autenticación realizada
from django.contrib.auth.decorators import login_required, user_passes_test

# Librería con los formularios requeridos para el C.R.U.D
from .forms import (
    UserRegisterForm,
    TokenAccessForm,
    UserLoginForm,
    RadicacionForm
)

# Librería con los models requeridos para los formularios
from famedic_users.models import (
    FamedicUser,
    UserManager,

    TokenAccess
)

# Librería para la manipulación de usuarios
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

# Librerías para generar y enviar por SMS las OTP y correos de confirmación de formularios
import secrets
from twilio.rest import Client
from django.core.mail import (
    send_mail,
    EmailMessage,
    EmailMultiAlternatives
)
from django.conf import settings

# Librerías para la vista blog (lista de radicados)
from .models import RadicacionModel, Sedes
from django.views.generic import (
    ListView,
    DetailView,
    View
)

from django.contrib.auth.views import LoginView

# variables globales para el paso de información entre vistas
loged_user = False

id_login = ""
email_login = ""
password_login = ""
phone_number_login = ""
location_login = ""

otp = ""

invoice_id = 0
invoice_finished = False
invoice_mail = ''

user = None


# redireccionamiento al panel administrativo
def admin_redirect(request):
    return redirect('/admin/')


def logout_redirect(request):
    usr = FamedicUser.objects.get(id=request.user.id)
    usr.authenticated = False
    usr.token = None
    usr.save()
    return redirect('/logout/')


# redireccionamiento desde index hasta la ventana de login
def index(request):
    global loged_user
    if request.user.is_authenticated:
        return redirect('main/')
    else:
        loged_user = False
        logout(request)
        return redirect('login/')


def verification_required(user_auth):
    return user_auth.is_validated


class LoginFamedic(LoginView):

    logged_mail = logged_pass = logged_idnt = user_logged = None

    authentication_form = UserLoginForm
    form_class = UserLoginForm

    template_name = 'FamedicDesign/LogIn.html'

    def form_valid(self, form):

        secret_otp = secrets.SystemRandom()
        token = str(secret_otp.randrange(100000, 999999))

        print(token)

        self.user_logged = form.get_user()

        cc = self.user_logged.id_famedic
        self.logged_idnt = form.cleaned_data.get('id_famedic')

        if self.user_logged.is_validated:
            self.user_logged.authenticated = False
            self.user_logged.save()

        if cc != self.logged_idnt:
            messages.warning(self.request, 'Por favor verifique el número de identificación ingresado.')
            logout(self.request)

            return redirect('/login/')

        if not self.user_logged.is_updated:
            self.request.session['member_id'] = self.user_logged.id
            messages.warning(self.request, 'Por favor actualice los datos de su cuenta antes de proceder e iniciar '
                                           'sesión.')
            return redirect('/registro/')

        self.user_logged.token = token
        self.user_logged.save()

        sender_mail = settings.EMAIL_HOST_USER

        token_mail = EmailMultiAlternatives(

            from_email=sender_mail,
            to=[self.logged_mail],

            subject='Token de acceso al portal de facturas - Famedic IPS',
            body='Sr(a). Usuario(a) del portal de proveedores.\n'

                 '\nSe ha detectado un intento de acceso al portal de radicación de facturas.'
                 ' Su token de acceso para esta sesión es ' + str(token) + '. Si usted no trató de'
                 ' ingresar recientemente por favor contactese con un administrador del portal'
                 ' para revisar y garantizar la seguridad de su cuenta.'

                 '\n\n Este es un mensaje automático y no es necesario responder.',
        )

        # print(token_mail.message())
        token_mail.send()

        self.request.session['member_id'] = self.user_logged.id

        print('login session id: ', self.request.session['member_id'])
        print('authenticated?: ', self.user_logged.is_authenticated)
        print('validated?: ', self.user_logged.is_validated)

        return super(LoginView, self).form_valid(form)


class TokenAccess(LoginFamedic):

    user_mail = user_pass = user_tokn = None

    template_name = 'FamedicDesign/TokenAccess.html'
    form_class = TokenAccessForm
    authentication_form = TokenAccessForm

    def form_valid(self, form):

        self.user_tokn = FamedicUser.objects.get(id=self.request.session['member_id']).token
        print(self.user_tokn)

        if form.cleaned_data.get('token') == self.user_tokn:
            usr = FamedicUser.objects.get(id=self.request.session['member_id'])
            usr.token = None
            usr.authenticated = True
            usr.save()

            login(self.request, usr)

            return redirect('/main/')

        messages.warning(self.request, 'Por favor verifique el número de token ingresado.')
        return redirect('/verificacion/')


class Registration(LoginFamedic):

    template_name = 'FamedicDesign/Registro.html'
    form_class = UserRegisterForm
    authentication_form = UserRegisterForm

    def form_valid(self, form):

        usr = FamedicUser.objects.get(id=self.request.session['member_id'])

        usr.first_name = form.cleaned_data.get('first_name')
        usr.last_name = form.cleaned_data.get('last_name')
        usr.recovery_email = form.cleaned_data.get('recovery_email')
        usr.phone = form.cleaned_data.get('phone')
        usr.set_password(form.cleaned_data.get('password2'))

        usr.updated = True
        usr.save()

        messages.success(request, f'Cuenta actualizada correctamente.')
        return redirect('/login/')


# envío de nuevo del token
def resend_token(request):

    usr_id = request.session['member_id']
    usr = FamedicUser.objects.get(id=usr_id)

    new_secret_otp = secrets.SystemRandom()
    token = str(new_secret_otp.randrange(100000, 999999))
    print(token)

    sender_mail = settings.EMAIL_HOST_USER

    token_mail = EmailMultiAlternatives(

        from_email=sender_mail,
        to=[usr.email],

        subject='Token de acceso al portal de facturas - Famedic IPS',
        body='Sr(a). Usuario(a) del portal de proveedores.\n'

             '\nSe ha detectado un intento de acceso al portal de radicación de facturas.'
             ' Su token de acceso para esta sesión es ' + str(token) +
             '. Si usted no trató de'
             ' ingresar recientemente por favor contactese con un administrador del portal'
             ' para revisar y garantizar la seguridad de su cuenta.'

             '\n\n Este es un mensaje automático y no es necesario responder.',
    )

    token_mail.send()

    usr.token = token
    usr.save()

    messages.success(request, f'Se envió un nuevo token para el acceso')
    return redirect('/verificacion/')


# ingreso al  portal principal
@user_passes_test(verification_required)
@login_required(login_url='/login/')
def hola_mundo(request):
    tz = timezone.localdate()
    # print(tz)

    if request.user.is_authenticated:

        # phone_number = '+57' + request.user.get_phone()
        # print(phone_number)

        form_main = {
            'page_title': 'Pagina principal',
            'user_name': request.user.get_full_name(),
        }

        return render(request, 'FamedicDesign/Main.html', form_main)
    else:
        return redirect('/login/')


# sección de perfil del usuario
@login_required(login_url='/login/')
@user_passes_test(verification_required)
def perfil(request):
    form_profile = {
        'page_title': 'Perfil del usuario'
    }
    return render(request, 'FamedicDesign/PerfilUsuario.html', form_profile)


# sección de radicación
@login_required(login_url='/login/')
@user_passes_test(verification_required)
def radicacion(request):
    tz = timezone.localdate()
    # print(tz)
    # print(tz.day)
    # print(type(tz.day))
    global invoice_id
    global invoice_finished

    pk_user = {'radicador': request.user}

    form = RadicacionForm(request.POST or None, request.FILES, pk_user)
    invoice_finished = False

    if request.method == 'POST':

        if form.is_valid():

            invoice_finished = True

            fecha1 = form.cleaned_data.get('datetime_factura1')
            fecha2 = form.cleaned_data.get('datetime_factura2')
            # print(str(fecha1) + ' - ini')
            # print(str(fecha2) + ' - fin')

            if fecha1 < fecha2:

                sede = form.cleaned_data.get('sede_selection')
                sede_id = get_object_or_404(Sedes, sede_name=sede)

                data_form = form.save(commit=False)
                data_form.radicador = request.user
                data_form.save()

                invoice_id = data_form.pk

                form = RadicacionForm()

                return redirect('/main/done/')

            else:
                form = RadicacionForm()
                messages.warning(request, 'Fechas ingresadas incorrectamente')

        else:
            form = RadicacionForm()
            messages.warning(request, 'Error validando formulario')

    else:
        form = RadicacionForm()

    form_rad = {
        'page_title': 'Radicación de facturas',
        'user_name': request.user.get_full_name(),
        'id_user': request.user.pk,
        'form': form,
        'timezone_rad': tz
    }

    return render(request, 'FamedicDesign/RadicadosSite.html', form_rad)


# Vista de radicación realizada
@login_required(login_url='/login/')
@user_passes_test(verification_required)
def radicacion_finish(request):
    global invoice_id
    global invoice_mail
    global invoice_finished

    tz = timezone.localdate()

    # invoice_mail = 'ricardoq@tics-sas.com'
    invoice_mail = 'direccioninformatica@famedicips.com'
    user_mail = request.user.get_username()
    user_fullname = request.user.get_full_name()

    sender_mail = settings.EMAIL_HOST_USER

    if request.user.is_authenticated:
        if invoice_finished:

            # Correo enviado al usuario radicador
            mail_to_user = EmailMultiAlternatives(

                from_email=sender_mail,
                to=[user_mail],

                subject='Asunto: Confirmación De Radicación Exitosa',

                body='Sr(a). Usuario(a)' + request.user.get_full_name() + ', su solicitud de pago fue registrada '
                     'exitosamente con numero de radicación.' + str(invoice_id) + '\n'

                     '\nSERVICIOS MEDICOS FAMEDIC SAS notifica que dentro de los treinta (20) días hábiles siguientes '
                     'a la presentación de la presente factura o cuenta de cobro, comunicará el resultado de la '
                     'auditoria realizada a la presente solicitud. Lo anterior de acuerdo al decreto Numero 4747 de '
                     'diciembre de 2007, por medio del cual se regulan algunos aspectos de las relaciones entre los '
                     'prestadores de servicios de salud y las entidades responsables del pago de la población a su '
                     'cargo.\n'
                     
                     '\n\n Cualquier duda o inquietud con gusto será resuelta en el correo.'
                     '\n\n Este es un mensaje automático y no es necesario responder.',
            )

            # Correo enviado al usuario administrador
            mail_to_admin = EmailMultiAlternatives(

                from_email=sender_mail,
                to=[invoice_mail],
                bcc=[sender_mail],

                subject='Radicación de archivos recibida - Famedic IPS',
                body='Sr(a) administrador(a) del portal.\n '

                     '\nSe le notifica que el usuario ' + user_fullname + ' (' + user_mail + ') '
                                                                                             'realizó un radicado identificado con el numero ' + str(
                    invoice_id) + ', para realizar '
                                  'el proceso de revisión y aprobación será necesario revisar el correspondiente '
                                  'en el portal de radicaciones de Famedic IPS. \n'

                                  '\nDespués de acceder y confirmar dicho proceso realizado por el usuario el radicado quedará '
                                  'aprobado en el portal. \n'


                                  '\n\n Este es un mensaje automático y no es necesario responder.'
            )

            mail_to_user.send()
            mail_to_admin.send()

            form_finished = {
                'page_title': 'Radicación realizada',
                'user_name': request.user.get_full_name(),
                'invoice_id': invoice_id,
                'invoice_mail': invoice_mail
            }

            invoice_finished = False

            if tz.day > 20:
                # print('fecha mayor')
                messages.warning(request, 'Recuerde que todo registro después del dia 20'
                                          ' del mes vigente quedará pendiente para el '
                                          'siguiente. \n'
                                          'Tendrá que esperar a que inicie el proximo'
                                          'mes para que su radicado sea estudiado.')
                return render(request, 'FamedicDesign/Radicado.html', form_finished)

            else:
                return render(request, 'FamedicDesign/Radicado.html', form_finished)

        else:

            return redirect('/main/radicar/')
    else:
        return redirect('/login/')


# sección de lista de radicados
class ListaRadicados(ListView):
    paginate_by = 5
    model = RadicacionModel
    template_name = 'FamedicDesign/ListaRadicados.html'
    queryset = RadicacionModel.objects.all()

    def get_queryset(self):
        if self.request.user.is_admin:
            return RadicacionModel.objects.all()
        else:
            return RadicacionModel.objects.filter(radicador=self.request.user.pk)


# sección de detalles de radicados
class RadicadoDetail(DetailView):
    model = RadicacionModel
    template_name = 'FamedicDesign/DetalleRadicados.html'


# sección de lista de radicados
@login_required(login_url='/login/')
@user_passes_test(verification_required)
def search_radicados(request):
    form_search_rad = {
        'page_title': 'Búsqueda de radicados',
        'user_name': request.user.get_full_name()
    }
    return render(request, 'FamedicDesign/ListaRadicados.html', form_search_rad)
