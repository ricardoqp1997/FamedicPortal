# Librerías base para la manipulación de formularios Django
from django.conf import settings
from django import forms
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from bootstrap_datepicker_plus import DatePickerInput

# Librería personalizada para el uso de los modelos propios de usuarios Famedic
from famedic_users.models import (
    FamedicUser,
    UserManager
)

import secrets

from django.conf import settings
from django.core.mail import (
    EmailMultiAlternatives
)

# Librería personalizada para el uso del modelo de radicación
from .models import RadicacionModel, Sedes
from django.contrib.auth.forms import AuthenticationForm


# Form de inicio de sesión para usuarios
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Correo electrónico')
    id_famedic = forms.CharField(label='Cédula/NIT', widget=forms.NumberInput, max_length=10)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    field_order = ['username', 'id_famedic', 'password']

    def clean(self, *args, **kwargs):

        username = self.cleaned_data.get('email')
        id_famedic = self.cleaned_data.get('id_famedic')
        password = self.cleaned_data.get('password')

        if username and id_famedic and password:
            user = authenticate(email=username, id_famedic=id_famedic, password=password)
            print("Hola mundo 1")

            try:
                if user.get_id() != id_famedic:
                    raise forms.ValidationError('Por favor verifique el número de identificación ingresado.')
                if not user:
                    raise forms.ValidationError('Por favor verifique los datos de usuario ingresados.')
                if not user.check_password(password):
                    print("Hola mundo2")
                    usuario = FamedicUser.objects.get(id_famedic=id_famedic)
                    usuario.intentos_acceso = user.intentos_acceso + 1
                    if usuario.intentos_acceso >= 5:
                        usuario.bloqueado = True
                    usuario.save()
                    raise forms.ValidationError('Por favor verifique la contraseña ingresada.')
                if not user.is_active:
                    raise forms.ValidationError('El usuario ingresado no está activo.')
            except:
                raise forms.ValidationError('Error validando sus datos, rectifiquelos e ingreselos de nuevo.')

        return super(UserLoginForm, self).clean()


# Form de registro de usuarios (añadiendole el campo de email al form base de registro de Django)
class UserRegisterForm(forms.ModelForm):

    def __init__(self, request=None, *args, **kwargs):

        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    first_name = forms.CharField(label='Nombre(s)', max_length=25)
    last_name = forms.CharField(label='Apellido(s)', max_length=25)
    phone = forms.CharField(label='Teléfono celular', widget=forms.NumberInput, max_length=10)
    recovery_email = forms.EmailField(label='Correo electrónico de recuperación')

    password1 = forms.CharField(
        label='Nueva contraseña',
        widget=forms.PasswordInput(

        )
    )

    password2 = forms.CharField(
        label='Confirme su nueva contraseña',
        widget=forms.PasswordInput(

        )
    )

    updated = forms.BooleanField(
        widget=forms.HiddenInput(
            attrs={
                'value': True
            }
        ),
        required=False
    )

    class Meta:

        model = FamedicUser
        fields = [
            'first_name',
            'last_name',
            'recovery_email',
            'phone',
            'updated'
        ]

    def clean_email(self):

        email = self.cleaned_data.get('email')
        recovery = self.cleaned_data.get('recovery_email')

        qs = FamedicUser.objects.filter(email=email)

        if qs.exists():
            raise forms.ValidationError("El correo electrónico ya está registrado")
        if email == recovery:
            raise forms.ValidationError("Su correo de acceso y el de recuperación deben ser distintos")

        return email

    def clean_password2(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('La confirmación no coincide con la contraseña ingresada')

        return password2

    def save(self, commit=True):

        user = super(UserRegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

        return user


# Form de registro de administradores
class UserAdminCreationForm(forms.ModelForm):
    id_famedic = forms.CharField(label='Cédula/NIT', widget=forms.NumberInput, max_length=10)
    location = forms.CharField(label='Entidad a la que pertenece', max_length=50)
    email = forms.EmailField(label='Correo electrónico')

    class Meta:
        model = FamedicUser
        fields = [
            'id_famedic',
            'email',
            'location'
        ]

    """def clean_password2(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('La confirmación no coincide con la contraseña ingresada')

        return password2"""

    def save(self, commit=True):
        random = secrets.SystemRandom()
        random_password = str(random.randrange(10000000, 99999999))
        print(random_password)

        receptor = self.cleaned_data.get('email')
        id_acceso = self.cleaned_data.get('id_famedic')
        print(receptor)

        sender_mail = settings.EMAIL_HOST_USER

        access_mail = EmailMultiAlternatives(

            from_email=sender_mail,
            to=[receptor],

            subject='Creación de credenciales de acceso - Famedic IPS',
            body='Sr(a). Usuario(a) del portal de proveedores.\n '

                 '\nSe han creado sus nuevas credenciales para el ingreso al portal de radicación '
                 'http://proveedores.famedicips.co/login/.\n'
                 'Sus credenciales de acceso serán:\n\n '
                 ''
                 'Correo: ' + receptor +
                 '\nIdentificación: ' + id_acceso +
                 '\nContraseña: ' + str(random_password) + '\n'
                 '\nPara ingresar será requerido inicialmente que actualice los datos de su cuenta desde el portal '
                 'proveedores.famedicips.co, luego de dicha actualización podrá acceder y usar el portal de '
                 'proveedores de Famedic IPS.'

                 '\n\n Este es un mensaje automático y no es necesario responder.',
        )

        access_mail.send()

        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(str(random_password))

        if commit:
            user.save()

        return user


# Form de cambios a administradores
class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = FamedicUser
        fields = [
            'email',
            'password',
            'active',
            'admin'
        ]

    def clean_password(self):
        return self.initial['password']


# Form de ingreso del token de acceso (Solo obtención del token, la validación se hace en views.py)
class TokenAccessForm(forms.Form):

    def __init__(self, request=None, *args, **kwargs):

        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    token = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'onkeypress': 'return isNumberKey(event)',
                'id': 'bloquear'
            }
        ),
        label='Token de autenticación',
        required=True
    )

    def clean(self):
        token = self.cleaned_data.get('token')

        if token is None:
            raise self.get_invalid_login_error()

        return self.cleaned_data


# Form de radicacion de facturas
class RadicacionForm(forms.ModelForm):
    radicador = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False
    )

    datetime_factura1 = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.DateInput(
            attrs={
                'placeholder': 'DD-MM-YYYY',
                'class': 'form-control datetimepicker-input InputBlock1',
                'data-target': '#datetimepicker1',
                'height': '40px'
            }
        ),
        required=True,
    )

    datetime_factura2 = forms.DateField(
        input_formats=settings.DATE_INPUT_FORMATS,
        widget=forms.DateInput(
            attrs={
                'placeholder': 'DD-MM-YYYY',
                'class': 'form-control datetimepicker-input InputBlock2',
                'data-target': '#datetimepicker2',
                'height': '40px'
            }
        ),
        required=True,
    )

    id_factura = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Ingrese su consecutivo',
                'class': 'form-control monto_field',
                'aria-label': ''
            }
        ),
        required=True,
    )

    monto_factura = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Ingrese un monto',
                'class': 'form-control monto_field',
                'aria-label': ''
            }
        ),
        required=True,
    )

    regimen_type = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'id': 'regimen1',
                'class': 'form-control',
            }
        ),
        label='Régimen',
        choices=RadicacionModel.REGIMEN_CHOICES,
        required=True
    )

    sede_selection = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={
                'id': 'sede1',
                'class': 'form-control',
            }
        ),
        label='Sede correspondiente',
        queryset=Sedes.objects.filter(sede_status=True),
        required=True
    )

    observaciones = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'exampleFormControlTextarea1',
                'rows': '10'
            }
        ),
        required=False
    )

    datetime_radicado = forms.DateTimeField(
        widget=forms.HiddenInput(),
        required=False
    )

    file_ribs = forms.FileField(
        required=False
    )

    class Meta:
        model = RadicacionModel
        fields = [
            'radicador',

            'datetime_factura1',
            'datetime_factura2',
            'id_factura',
            'monto_factura',

            'file_factura',
            'file_aportes',
            'file_soporte',

            'file_ribs',

            'regimen_type',
            'sede_selection',
            'observaciones',
        ]

    def save(self, commit=True):
        invoice = super(RadicacionForm, self).save(commit=False)
        invoice.radicador = self.cleaned_data.get('radicador')
        invoice.sede_select = self.cleaned_data.get('sede_select')

        if commit:
            invoice.save()

        return invoice
