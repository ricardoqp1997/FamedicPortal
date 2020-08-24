# Librerías base para la manipulación de formularios Django
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# Librería personalizada para el uso de los modelos propios de usuarios Famedic
from famedic_users.models import (
    FamedicUser,
    UserManager
)

# Librería personalizada para el uso del modelo de radicación
from .models import RadicacionModel


# Form de inicio de sesión para usuarios
class UserLoginForm(forms.Form):

    email = forms.CharField(label='Correo electrónico')
    id_famedic = forms.CharField(label='Cédula/NIT', widget=forms.NumberInput, max_length=10)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):

        email = self.cleaned_data.get('email')
        id_famedic = self.cleaned_data.get('id_famedic')
        password = self.cleaned_data.get('password')

        if email and id_famedic and password:
            user = authenticate(email=email, id_famedic=id_famedic, password=password)

            if user.get_id() != id_famedic:
                raise forms.ValidationError('Por favor verifique los datos de usuario ingresados.')
            if not user:
                raise forms.ValidationError('Por favor verifique los datos de usuario ingresados.')
            if not user.check_password(password):
                raise forms.ValidationError('Por favor verifique la contraseña ingresada.')
            if not user.is_active:
                raise forms.ValidationError('El usuario ingresado no está activo.')
        return super(UserLoginForm, self).clean()


# Form de registro de usuarios (añadiendole el campo de email al form base de registro de Django)
class UserRegisterForm(forms.ModelForm):

    id_famedic = forms.CharField(label='Cédula/NIT', widget=forms.NumberInput, max_length=10)
    first_name = forms.CharField(label='Nombre(s)', max_length=25)
    last_name = forms.CharField(label='Apellido(s)', max_length=25)
    phone = forms.CharField(label='Teléfono celular', widget=forms.NumberInput, max_length=10)
    location = forms.CharField(label='Entidad a la que pertenece', max_length=50)
    email = forms.EmailField(label='Correo electrónico')
    recovery_email = forms.EmailField(label='Correo electrónico de recuperación')

    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme la contraseña ingresada', widget=forms.PasswordInput)

    class Meta:

        model = FamedicUser
        fields = [
            'id_famedic',
            'first_name',
            'last_name',
            'email',
            'recovery_email',
            'phone',
            'location'
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
    first_name = forms.CharField(label='Nombre(s)', max_length=25)
    last_name = forms.CharField(label='Apellido(s)', max_length=25)
    phone = forms.CharField(label='Teléfono celular', widget=forms.NumberInput, max_length=10)
    location = forms.CharField(label='Entidad a la que pertenece', max_length=50)
    email = forms.EmailField(label='Correo electrónico')
    recovery_email = forms.EmailField(label='Correo electrónico de recuperación')

    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme la contraseña ingresada', widget=forms.PasswordInput)

    class Meta:

        model = FamedicUser
        fields = [
            'id_famedic',
            'first_name',
            'last_name',
            'email',
            'recovery_email',
            'phone',
            'location'
        ]

    def clean_password2(self):

        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('La confirmación no coincide con la contraseña ingresada')

        return password2

    def save(self, commit=True):

        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])

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

    token = forms.CharField(
        widget=forms.PasswordInput,
        label='Token de autenticación',
        required=True
    )


# Form de radicacion de facturas
class RadicacionForm(forms.ModelForm):

    radicador = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False
    )

    id_factura = forms.CharField(
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Ingrese un número',
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

    sede_select = forms.ChoiceField(
        widget=forms.Select(
            attrs={
                'id': 'sede1',
                'class': 'form-control',
            }
        ),
        label='Sede correspondiente',
        choices=RadicacionModel.SEDE_CHOICES,
        required=True
    )

    observaciones = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'id': 'exampleFormControlTextarea1',
                'rows': '10'
            }
        )
    )

    class Meta:

        model = RadicacionModel
        fields = [
            'radicador',
            'id_factura',
            'monto_factura',
            'file_factura',
            'file_aportes',
            'file_soporte',
            'file_ribs',
            'regimen_type',
            'sede_select',
            'observaciones',
        ]

    def save(self, commit=True):

        invoice = super(RadicacionForm, self).save(commit=False)
        invoice.radicador = self.cleaned_data.get('radicador')

        if commit:

            invoice.save()

        return invoice
