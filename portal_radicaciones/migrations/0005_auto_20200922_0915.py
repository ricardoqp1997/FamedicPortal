# Generated by Django 3.0.3 on 2020-09-22 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_radicaciones', '0004_auto_20200922_0915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locacion',
            name='locacion_name',
            field=models.CharField(default='Arauca', max_length=50, verbose_name='nombre de la locación'),
        ),
    ]
