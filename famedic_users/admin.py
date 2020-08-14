from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import FamedicUser


admin.site.register(FamedicUser)

