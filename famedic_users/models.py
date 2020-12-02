from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)

# Clase para manipulacion, creacion, edicion de usuarios de Famedic User
class UserManager(BaseUserManager):

    # método base para la creación de los usuarios
    def create_user(self, id_famedic, email, location, password=None, is_active=True, is_staff=False, is_admin=False,
                    is_updated=False):
        if not email:
            raise ValueError('Es requerido ingresar el correo electrónico.')
        if not password:
            raise ValueError('Es requerido ingresar una contraseña.')
        user_obj = self.model(
            id_famedic=str(id_famedic),
            email=self.normalize_email(email),
            location=location,
        )
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.admin = is_admin
        user_obj.staff = is_staff
        user_obj.updated = is_updated
        user_obj.save(using=self._db)
        return user_obj

    # método para la asignación de usuarios staff
    def create_staffuser(self, id_famedic, email, location, password=None):
        user = self.create_user(
            id_famedic=str(id_famedic),
            email=self.normalize_email(email),
            location=location,
            password=password,
            is_staff=True

        )
        return user

    # método para la asignación de usuarios superuser
    def create_superuser(self, id_famedic, email, location, password=None):
        user = self.create_user(
            id_famedic=str(id_famedic),
            email=self.normalize_email(email),
            location=location,
            password=password,
            is_staff=True,
            is_admin=True,
            is_updated=True,
        )
        return user


# Clase para estructurar el modelo de datos de los usuarios de Famedic
class FamedicUser(AbstractBaseUser):

    DOCUMENT_TYPE_CHOICES = [
        ('NIT', 'Número NIT con indicativo al final'),
        ('CC', 'Cédula de ciudadanía'),
        ('CE', 'Cédula de extranjería'),
        ('PP', 'Pasaporte')
    ]
    # tipo de documento del usuario
    id_type = models.CharField(verbose_name='tipo de documento', max_length=3, choices=DOCUMENT_TYPE_CHOICES, default='CC')
    # documento del usuario
    id_famedic = models.CharField(verbose_name='cédula/NIT', max_length=10, unique=True)
    # nombre y apellidos del usuario
    first_name = models.CharField(verbose_name='nombre(s)', max_length=50, null=True)
    last_name = models.CharField(verbose_name='apellido(s)', max_length=50, null=True)
    # Foto de perfil del usuario
    profile_foto = models.ImageField(verbose_name='foto de perfil', blank=True, null=True)
    # correo electrónico de cuenta y para recuperación
    email = models.EmailField(verbose_name='correo electrónico', max_length=255, unique=True)
    recovery_email = models.EmailField(verbose_name='correo electrónico de recuperación', max_length=255, null=True)
    # número de teléfono del usuario
    phone = models.CharField(verbose_name='teléfono celular', max_length=10, unique=True, null=True)
    # empresa vinculada del usuario
    location = models.CharField(verbose_name='entidad a la que pertenece', max_length=255)
    # atributos adicionales para el usuario
    active = models.BooleanField(verbose_name='estado activo', default=True)
    staff = models.BooleanField(verbose_name='miembro del portal', default=True)
    admin = models.BooleanField(verbose_name='administrador del portal', default=False)
    # revisión de estado de cuenta (actualizada o no)
    updated = models.BooleanField(verbose_name='datos actualizados', default=False)

    token = models.CharField(null=True, max_length=6)
    authenticated = models.BooleanField(default=False)

    intentos_acceso = models.IntegerField(null=True, default=0)
    bloqueado = models.BooleanField(default=False)

    # Parametro desactivado
    is_active = models.BooleanField(verbose_name='Activo', default=True)

    # parametros del model
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'id_famedic',
        'location'
    ]
    objects = UserManager()

    # métodos base del modelo
    class Meta:
        verbose_name = 'Usuario'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        print(perm, obj)
        return True

    def has_module_perms(self, app_label):
        print(app_label)
        return True

    # métodos adicionales del model para obtención de datos del usuario
    def get_first_name(self):
        try:
            return self.first_name
        except:
            return 'N/A'

    def get_last_name(self):
        try:
            return self.last_name
        except:
            return 'N/A'

    def get_full_name(self):
        try:
            return str(self.first_name + ' ' + self.last_name)
        except:
            return 'N/A'

    def get_id(self):
        return self.id_famedic

    def get_phone(self):
        try:
            return self.phone
        except:
            return 'N/A'

    def get_mail(self):
        return self.email

    def get_location(self):
        return self.location

    # propiedades del model de usuario
    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_updated(self):
        return self.updated

    @property
    def is_validated(self):
        return self.authenticated


class TokenAccess(models.Model):

    user = models.ForeignKey(FamedicUser, on_delete=models.SET_NULL, null=True)
    token = models.CharField(default='0', max_length=6)
    datetime_loken = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Token'
