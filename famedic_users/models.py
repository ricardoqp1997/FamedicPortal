from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)


# Clase para manipulacion, creacion, edicion de usuarios de Famedic User
class UserManager(BaseUserManager):

    # método base para la creación de los usuarios
    def create_user(self, id_famedic, first_name, last_name, email, recovery_email, phone, location, password=None, is_active=True, is_staff=False, is_admin=False):
        if not email:
            raise ValueError('Es requerido ingresar el correo electrónico.')
        if not password:
            raise ValueError('Es requerido ingresar una contraseña.')

        user_obj = self.model(
            id_famedic=str(id_famedic),
            first_name=str(first_name),
            last_name=str(last_name),
            email=self.normalize_email(email),
            recovery_email=self.normalize_email(recovery_email),
            phone=str(phone),
            location=location,
        )
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.admin = is_admin
        user_obj.staff = is_staff
        user_obj.save(using=self._db)

        return user_obj

    # método para la asignación de usuarios staff
    def create_staffuser(self, id_famedic, first_name, last_name, email, recovery_email, phone, location, password=None):
        user = self.create_user(
            id_famedic=str(id_famedic),
            first_name=str(first_name),
            last_name=str(last_name),
            email=self.normalize_email(email),
            recovery_email=self.normalize_email(recovery_email),
            phone=str(phone),
            location=location,
            password=password,
            is_staff=True
        )

        return user

    # método para la asignación de usuarios superuser
    def create_superuser(self, id_famedic, first_name, last_name, email, recovery_email, phone, location, password=None):
        user = self.create_user(
            id_famedic=str(id_famedic),
            first_name=str(first_name),
            last_name=str(last_name),
            email=self.normalize_email(email),
            recovery_email=self.normalize_email(recovery_email),
            phone=str(phone),
            location=location,
            password=password,
            is_staff=True,
            is_admin=True
        )

        return user


# Clase para estructurar el modelo de datos de los usuarios de Famedic
class FamedicUser(AbstractBaseUser):

    # cédula del usuario
    id_famedic = models.CharField(verbose_name='cédula/NIT', max_length=10, unique=True)

    # nombre y apellidos del usuario
    first_name = models.CharField(verbose_name='nombre(s)', max_length=50)
    last_name = models.CharField(verbose_name='apellido(s)', max_length=50)

    # Foto de perfil del usuario
    profile_foto = models.ImageField(verbose_name='foto de perfil', blank=True)

    # correo electrónico de cuenta y para recuperación
    email = models.EmailField(verbose_name='correo electrónico', max_length=255, unique=True)
    recovery_email = models.EmailField(verbose_name='correo electrónico de recuperación', max_length=60)

    # número de teléfono del usuario
    phone = models.CharField(verbose_name='teléfono celular', max_length=10, unique=True)

    # empresa vinculada del usuario
    location = models.CharField(verbose_name='entidad a la que pertenece', max_length=255)

    # atributos adicionales para el usuario
    active = models.BooleanField(verbose_name='estado activo', default=True)
    staff = models.BooleanField(verbose_name='miembro del portal', default=True)
    admin = models.BooleanField(verbose_name='administrador del portal', default=False)

    # parametros del model
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'id_famedic',
        'first_name',
        'last_name',
        'recovery_email',
        'phone',
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
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_full_name(self):
        return str(self.first_name + ' ' + self.last_name)

    def get_id(self):
        return self.id_famedic

    def get_phone(self):
        return self.phone

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

