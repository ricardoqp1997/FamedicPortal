from django.db import models
from django import forms


# Create your models here.

class LoginFamedic(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
