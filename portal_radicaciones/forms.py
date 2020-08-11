from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate


# Form de inicio de sesión para usuarios

class UserLoginForm(forms.Form):
    email = forms.CharField(label='Correo electrónico')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)

            if not user:
                raise forms.ValidationError('Por favor verifique los datos de usuario ingresados.')
            if not user.check_password(password):
                raise forms.ValidationError('Por favor verifique la contraseña ingresada.')
            if not user.is_active:
                raise forms.ValidationError('El usuario ingresado no está activo.')
        return super(UserLoginForm, self).clean()


# Form de registro de usuarios (añadiendole el campo de email al form base de registro de Django)

class UserRegisterForm(UserCreationForm):

    first_name = forms.TextInput()
    email = forms.EmailField(label='Correo electrónico')
    username = forms.CharField(label='Número de teléfono', widget=forms.NumberInput)

    class Meta:
        model = User
        fields = ['first_name',
                  'email',
                  'username',
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
        widget=forms.NumberInput(attrs={'placeholder': ' Ingrese un monto'}),
        required=True
    )

    file_factura = forms.FileField()
    file_aportes = forms.FileField()
    file_soporte = forms.FileField()

    observaciones = forms.TextInput()