# Generated by Django 3.0.3 on 2020-08-19 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FamedicUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id_famedic', models.CharField(max_length=10, unique=True, verbose_name='cédula/NIT')),
                ('first_name', models.CharField(max_length=50, verbose_name='nombre(s)')),
                ('last_name', models.CharField(max_length=50, verbose_name='apellido(s)')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='correo electrónico')),
                ('recovery_email', models.EmailField(max_length=60, verbose_name='correo electrónico de recuperación')),
                ('phone', models.CharField(max_length=10, unique=True, verbose_name='teléfono celular')),
                ('location', models.CharField(max_length=255, verbose_name='entidad a la que pertenece')),
                ('active', models.BooleanField(default=True, verbose_name='estado activo')),
                ('staff', models.BooleanField(default=True, verbose_name='miembro del portal')),
                ('admin', models.BooleanField(default=False, verbose_name='administrador del portal')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
