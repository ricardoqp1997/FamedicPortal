# Librerías de Django para el manejo de las vistas, plantillas y navegación
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

# Librería para restricción de vistas con autenticación realizada
from django.contrib.auth.decorators import login_required

# Librería con los formilarios requeridos para el C.R.U.D
from .forms import (
    UserRegisterForm,
    TokenAccessForm,
    UserLoginForm
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


email_login = ""
password_login = ""
phone_number_login = ""
otp = ""


# redireccionamiento desde index hasta la ventana de login
def index(request):
    if request.user.is_authenticated:
        return redirect('main/')
    else:
        logout(request)
        return redirect('login/')


# registro de usuario
def register_famedic(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada: {username}')
            return redirect('/login/')
    else:
        form = UserRegisterForm()

    form_register = {
        'page_title': 'Inicio de sesión',
        'form': form
    }

    return render(request, 'FamedicDesign/Registro.html', form_register)


# ventana de inicio de sesion
def login_famedic(request):

    form = UserLoginForm(request.POST or None)

    global email_login
    global password_login
    global phone_number_login
    global otp

    if form.is_valid():
        email_login = form.cleaned_data.get('email')
        password_login = form.cleaned_data.get('password')

        user = authenticate(username=email_login, password=password_login)
        phone_number_login = '+57' + user.get_username()
        print(phone_number_login)

        secret_otp = secrets.SystemRandom()
        otp = str(secret_otp.randrange(100000, 999999))
        print(otp)

        account_sid = 'AC87661e5cf909a34afc46401f943466b8'
        auth_token = '626d52267fa60f71224372dcb158e20e'
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
                body=f"Su código de acceso al portal de radicación de facturas es: {otp}.",
                from_='+12165846582',
                to=phone_number_login
            )

        print(message.sid)

        return redirect('/verificacion/')

    login_form = {
        'page_title': 'Inicio de sesión',
        'form': form
    }

    return render(request, 'FamedicDesign/LogIn.html', login_form)


# ingreso de token para acceso
def token_famedic(request):

    form = TokenAccessForm(request.POST or None)

    global email_login
    global password_login
    global phone_number_login
    global otp

    if form.is_valid():
        token_number = form.cleaned_data.get('token')

        if token_number == otp:
            user = authenticate(username=email_login, password=password_login)
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


# envío de nuevo del token
def resend_token(request):
    global otp

    new_secret_otp = secrets.SystemRandom()
    otp = str(new_secret_otp.randrange(100000, 999999))
    print(otp)

    account_sid = 'AC87661e5cf909a34afc46401f943466b8'
    auth_token = '626d52267fa60f71224372dcb158e20e'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            body=f"Su código de acceso al portal de radicación de facturas es: {otp}.",
            from_='+12165846582',
            to=phone_number_login
        )

    print(message.sid)

    messages.success(request, f'Se envió un nuevo token para el acceso')
    return redirect('/verificacion')


# ingreso al  portal principal
@login_required(redirect_field_name='login')
def hola_mundo(request):

    if request.user.is_authenticated:
        form_main = {
            'page_title': 'Pagina principal',
            'user_name': request.user.first_name
        }
        return render(request, 'FamedicDesign/Main.html', form_main)
    else:
        return redirect('/login/')


# sección de perfil del usuario
@login_required(redirect_field_name='login')
def perfil(request):
    return render(request, 'FamedicDesign/PerfilUsuario.html', user)


# sección de opciones de sitio
@login_required(redirect_field_name='login')
def opciones(request):
    return render(request, 'FamedicDesign/OpcionesSitio.html', user)


# sección de radicación
@login_required(redirect_field_name='login')
def radicacion(request):
    return render(request, 'FamedicDesign/RadicadosSite.html', user)


# sección de lista de radicados
@login_required(redirect_field_name='login')
def list_radicados(request):
    return render(request, 'FamedicDesign/ListaRadicados.html', user)
