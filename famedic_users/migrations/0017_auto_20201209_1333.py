# Generated by Django 3.1.4 on 2020-12-09 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('famedic_users', '0016_auto_20201201_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='famedicuser',
            name='intentos_acceso',
            field=models.IntegerField(default=0),
        ),
    ]