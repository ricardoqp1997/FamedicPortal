from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, id, email, password=None, is_active=True, is_admin=False):
        if not email:
            raise ValueError('Es requerido ingresar el correo electrónico.')
        if not password:
            raise ValueError('Es requerido ingresar una contraseña.')

        user_obj = self.model(
            id=self.normalize_username(id),
            email=self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.is_active = is_active
        user_obj.is_admin = is_admin
        user_obj.save(using=self._db)

        return user_obj

    def create_admin(self, id, email, password=None):
        user = self.create_user(
            id=id,
            email=email,
            password=password,
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
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['id']

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_id(self):
        return self.id

    @property
    def is_admin(self):
        return self.is_admin

    @property
    def is_active(self):
        return self.is_active

    @is_active.setter
    def is_active(self, value):
        self._is_active = value

    @is_admin.setter
    def is_admin(self, value):
        self._is_admin = value

    class Meta:
        db_table = 'auth_user'
