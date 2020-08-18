from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)


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
        # user.save(using=self._db)

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
        # user.save(using=self._db)

        return user


class FamedicUser(AbstractBaseUser):

    # cédula del usuario
    id_famedic = models.CharField(verbose_name='id_famedic', max_length=10, unique=True)

    # nombre y apellidos del usuario
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    # correo electrónico de cuenta y para recuperación
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    recovery_email = models.EmailField(verbose_name='recovery email', max_length=60)

    # número de teléfono del usuario
    phone = models.CharField(max_length=10, unique=True)

    # empresa vinculada del usuario
    location = models.CharField(max_length=255)

    # atributos adicionales para el usuario
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)

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

    # métodos base del model
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
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
