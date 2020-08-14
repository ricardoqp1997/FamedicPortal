from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from famedic_users.models import (
    FamedicUser,
    UserManager
)


# Form de inicio de sesión para usuarios
class UserLoginForm(forms.Form):
    email = forms.CharField(label='Correo electrónico')
    id = forms.CharField(label='Cédula', widget=forms.NumberInput, max_length=10)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        id = self.cleaned_data.get('id')
        password = self.cleaned_data.get('password')

        if email and id and password:
            user = authenticate(email=email, id=id, password=password)

            if not user:
                raise forms.ValidationError('Por favor verifique los datos de usuario ingresados.')
            if not user.check_password(password):
                raise forms.ValidationError('Por favor verifique la contraseña ingresada.')
            if not user.is_active:
                raise forms.ValidationError('El usuario ingresado no está activo.')
        return super(UserLoginForm, self).clean()


# Form de registro de usuarios (añadiendole el campo de email al form base de registro de Django)
class UserRegisterForm(UserCreationForm):

    id = forms.CharField(label='Cédula/NIT', widget=forms.NumberInput, max_length=10)
    first_name = forms.CharField(label='Nombre(s)', max_length=25)
    last_name = forms.CharField(label='Apellido(s)', max_length=25)
    phone = forms.CharField(label='Teléfono celular', widget=forms.NumberInput, max_length=10)
    email = forms.EmailField(label='Correo electrónico')
    recovery_email = forms.EmailField(label='Correo electrónico de recuperación')

    class Meta:
        model = FamedicUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'recovery_email',
            'phone',
            'password1',
            'password2'
        ]


# Form de ingreso del token de acceso (Solo obtención del token, la validación se hace en views.py)
class TokenAccessForm(forms.Form):

    token = forms.CharField(
        widget=forms.NumberInput,
        label='Token de autenticación',
        required=True
    )


# Form de radicacion de facturas
class RadicacionForm(forms.Form):

    monto_factura = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Ingrese un monto',
                'class': 'form-control monto_field',
                'aria-label': 'Amount (to the nearest dollar)'
            }
        ),
        required=True
    )

    file_factura = forms.FileField(
        allow_empty_file=False,
        widget=forms.FileInput(
            attrs={
                'type': 'file',
                'class': 'custom-file-input',
                'id': 'customFileLang',
                'lang': 'es'
            }
        ),
        label='Factura',
        required=True
    )
    file_aportes = forms.FileField(
        allow_empty_file=False,
        widget=forms.FileInput(
            attrs={
                'type': 'file',
                'class': 'custom-file-input',
                'id': 'customFileLang',
                'lang': 'es'
            }
        ),
        label='Aportes',
        required=True
    )
    file_soporte = forms.FileField(
        allow_empty_file=False,
        widget=forms.FileInput(
            attrs={
                'type': 'file',
                'class': 'custom-file-input',
                'id': 'customFileLang',
                'lang': 'es'
            }
        ),
        label='Soportes',
        required=True
    )
    file_ribs = forms.FileField(
        allow_empty_file=False,
        widget=forms.FileInput(
            attrs={
                'type': 'file',
                'class': 'custom-file-input',
                'id': 'customFileLang',
                'lang': 'es'
            }
        ),
        label='Ribs',
        required=True
    )

    observaciones = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'exampleFormControlTextarea1',
                'rows': '8'
            }
        )
    )
