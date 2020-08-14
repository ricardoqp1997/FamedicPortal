from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate


# Form de inicio de sesión para usuarios

class UserLoginForm(forms.Form):
    email = forms.CharField(label='Correo electrónico')
    id_number = forms.CharField(label='Cédula', widget=forms.NumberInput, max_length=10)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        id_number = self.cleaned_data.get('id_number')
        password = self.cleaned_data.get('password')

        if email and id_number and password:
            user = authenticate(username=id_number, password=password, email=email)

            if not user:
                raise forms.ValidationError('Por favor verifique los datos de usuario ingresados.')
            if not user.check_password(password):
                raise forms.ValidationError('Por favor verifique la contraseña ingresada.')
            if not user.is_active:
                raise forms.ValidationError('El usuario ingresado no está activo.')
        return super(UserLoginForm, self).clean()


# Form de registro de usuarios (añadiendole el campo de email al form base de registro de Django)

class UserRegisterForm(UserCreationForm):

    username = forms.CharField(label='Cédula', widget=forms.NumberInput)
    first_name = forms.TextInput()
    last_name = forms.TextInput()
    email = forms.EmailField(label='Correo electrónico')

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
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
