from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)


# Create your models here.

class UserManager(BaseUserManager):

    # método base para la creación de los usuarios
    def create_user(self, id, first_name, last_name, email, recovery_email, phone, password=None, is_active=True, is_admin=False, is_staff=False):
        if not email:
            raise ValueError('Es requerido ingresar el correo electrónico.')
        if not password:
            raise ValueError('Es requerido ingresar una contraseña.')

        user_obj = self.model(
            id=str(id),
            first_name=str(first_name),
            last_name=str(last_name),
            email=self.normalize_email(email),
            recovery_email=self.normalize_email(recovery_email),
            phone=str(phone)
        )
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.admin = is_admin
        user_obj.staff = is_staff
        user_obj.save(using=self._db)

        return user_obj

    # método para la asignación de usuarios staff
    def create_staffuser(self, id, first_name, last_name, email, recovery_email, phone, password=None):
        user = self.create_user(
            id=str(id),
            first_name=str(first_name),
            last_name=str(last_name),
            email=self.normalize_email(email),
            recovery_email=self.normalize_email(recovery_email),
            phone=str(phone),
            password=password,
            is_staff=True
        )

        return user

    # método para la asignación de usuarios superuser
    def create_superuser(self, id, first_name, last_name, email, recovery_email, phone, password=None):
        user = self.create_user(
            id=str(id),
            first_name=str(first_name),
            last_name=str(last_name),
            email=self.normalize_email(email),
            recovery_email=self.normalize_email(recovery_email),
            phone=str(phone),
            password=password,
            is_staff=True,
            is_admin=True
        )

        return user


class FamedicUser(AbstractBaseUser):

    # cédula del usuario
    id = models.CharField(max_length=10, unique=True, primary_key=True)

    # nombre y apellidos del usuario
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)

    # correo electrónico de cuenta y para recuperación
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    recovery_email = models.EmailField(verbose_name='recovery email', max_length=60)

    # número de teléfono del usuario
    phone = models.CharField(max_length=10)

    # atributos adicionales para el usuario
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)

    # parametros del model
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['id', 'first_name', 'last_name', 'recovery_email', 'phone']

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
        return self.id

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
