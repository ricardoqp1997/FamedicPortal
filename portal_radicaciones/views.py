# Librerías de Django para el manejo de las vistas, plantillas y navegación
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

# Librería para restricción de vistas con autenticación realizada
from django.contrib.auth.decorators import login_required

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
    UserManager
)

# Librería para la manipulación de usuarios
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)

# Librerías para generar y enviar por SMS las OTP
import secrets
from twilio.rest import Client

loged_user = False
id_login = ""
email_login = ""
password_login = ""
phone_number_login = ""
otp = ""
invoice_id = 0
invoice_finished = False
invoice_mail = ''


# redireccionamiento al panel administrativo
def admin_redirect(request):
    return redirect('/admin/')


# redireccionamiento desde index hasta la ventana de login
def index(request):
    global loged_user
    if request.user.is_authenticated:
        return redirect('main/')
    else:
        loged_user = False
        logout(request)
        return redirect('login/')


# registro de usuario
def register_famedic(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            id = form.cleaned_data.get('id_famedic')
            messages.success(request, f'Cuenta creada: {id}')
            return redirect('/login/')
    else:
        form = UserRegisterForm()

    form_register = {
        'page_title': 'Registro de usuarios',
        'form': form
    }

    return render(request, 'FamedicDesign/Registro.html', form_register)


# ventana de inicio de sesion
def login_famedic(request):

    form = UserLoginForm(request.POST or None)

    global loged_user
    global id_login
    global email_login
    global password_login
    global phone_number_login
    global otp

    if form.is_valid():

        id_login = form.cleaned_data.get('id')
        email_login = form.cleaned_data.get('email')
        password_login = form.cleaned_data.get('password')

        user = authenticate(email=email_login, id=id_login, password=password_login)
        phone_number_login = '+57' + user.get_phone()
        print(phone_number_login)

        secret_otp = secrets.SystemRandom()
        otp = str(secret_otp.randrange(100000, 999999))
        print(otp)
        """
        account_sid = 'AC87661e5cf909a34afc46401f943466b8'
        auth_token = '42c8e8dda0ed20b0a6cee6461e979f1e'
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
                body=f"Su código de acceso al portal de radicación de facturas es: {otp}.",
                from_='+12165846582',
                to=phone_number_login
            )

        print(message.sid)
        """
        loged_user = True
        return redirect('/verificacion/')

    login_form = {
        'page_title': 'Inicio de sesión',
        'form': form
    }

    return render(request, 'FamedicDesign/LogIn.html', login_form)


# ingreso de token para acceso
def token_famedic(request):

    form = TokenAccessForm(request.POST or None)

    global loged_user
    global id_login
    global email_login
    global password_login
    global phone_number_login
    global otp

    if request.user.is_authenticated:
        return redirect('/main/')
    else:
        if loged_user:
            if form.is_valid():
                token_number = form.cleaned_data.get('token')

                if token_number == otp:
                    user = authenticate(email=email_login, id=id_login, password=password_login)
                    login(request, user)
                    return redirect('/main/')
                else:
                    messages.error(request, 'Error en validación del token. Vuelva a ingresarlo.')
                    return redirect('/verificacion/')

            token_form = {
                'page_title': 'Validación de ingreso',
                'form': form,
            }

            return render(request, 'FamedicDesign/TokenAccess.html', token_form)
        else:
            return redirect('/login/')


# envío de nuevo del token
def resend_token(request):
    global otp

    new_secret_otp = secrets.SystemRandom()
    otp = str(new_secret_otp.randrange(100000, 999999))
    print(otp)
    """
    account_sid = 'AC87661e5cf909a34afc46401f943466b8'
    auth_token = '42c8e8dda0ed20b0a6cee6461e979f1e'
    client = Client(account_sid, auth_token)
    
    message = client.messages \
        .create(
            body=f"Su código de acceso al portal de radicación de facturas es: {otp}.",
            from_='+12165846582',
            to=phone_number_login
        )
    
    print(message.sid)
    """
    messages.success(request, f'Se envió un nuevo token para el acceso')
    return redirect('/verificacion/')


# ingreso al  portal principal
@login_required(login_url='/login/')
def hola_mundo(request):

    if request.user.is_authenticated:
        form_main = {
            'page_title': 'Pagina principal',
            'user_name': request.user.get_full_name()
        }
        return render(request, 'FamedicDesign/Main.html', form_main)
    else:
        return redirect('/login/')


# sección de perfil del usuario
@login_required(login_url='/login/')
def perfil(request):
    form_profile = {
        'page_title': 'Perfil del usuario'
    }
    return render(request, 'FamedicDesign/PerfilUsuario.html', form_profile)


# sección de opciones de sitio
@login_required(login_url='/login/')
def opciones(request):
    form_settings = {
        'page_title': 'Opciones del sitio'
    }
    return render(request, 'FamedicDesign/OpcionesSitio.html', form_settings)


# sección de radicación
@login_required(login_url='/login/')
def radicacion(request):

    global invoice_id
    global invoice_finished

    pk_user = {'radicador': request.user}

    form = RadicacionForm(request.POST or None, request.FILES, pk_user)
    invoice_finished = False

    if request.method == 'POST':

        if form.is_valid():

            invoice_finished = True

            """form.radicador = request.user
            saved_form = form.save()
            invoice_id = saved_form.pk
            form.save()"""

            data_form = form.save(commit=False)
            data_form.radicador = request.user
            data_form.save()

            invoice_id = data_form.pk

            form = RadicacionForm()

            return redirect('/main/done/')
        else:
            form = RadicacionForm()
            messages.add_message(request, messages.ERROR, 'Error validando formulario')

    else:
        form = RadicacionForm()

    form_rad = {
        'page_title': 'Radicación de facturas',
        'user_name': request.user.get_full_name(),
        'id_user': request.user.pk,
        'form': form,
    }

    return render(request, 'FamedicDesign/RadicadosSite.html', form_rad)


# Vista de radicación realizada
@login_required(login_url='/login/')
def radicacion_finish(request):

    global invoice_id
    global invoice_mail
    global invoice_finished

    invoice_mail = 'admin1234@mail.com'

    if invoice_finished:

        form_finished = {
            'page_title': 'Radicación realizada',
            'user_name': request.user.get_full_name(),
            'invoice_id': invoice_id,
            'invoice_mail': invoice_mail
        }

        invoice_finished = False

        return render(request, 'FamedicDesign/Radicado.html', form_finished)
    else:

        return redirect('/main/radicar/')


# sección de lista de radicados
@login_required(login_url='/login/')
def list_radicados(request):
    form_list_rad = {
        'page_title': 'Lista de radicados',
        'user_name': request.user.get_full_name()
    }
    return render(request, 'FamedicDesign/ListaRadicados.html', form_list_rad)


# sección de lista de radicados
@login_required(login_url='/login/')
def search_radicados(request):
    form_search_rad = {
        'page_title': 'Búsqueda de radicados',
        'user_name': request.user.get_full_name()
    }
    return render(request, 'FamedicDesign/ListaRadicados.html', form_search_rad)
