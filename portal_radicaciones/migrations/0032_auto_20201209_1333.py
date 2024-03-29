# Generated by Django 3.1.4 on 2020-12-09 18:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_radicaciones', '0031_auto_20201207_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radicacionmodel',
            name='datetime_factura1',
            field=models.DateTimeField(blank=True, null=True, verbose_name='fecha inicial de la factura'),
        ),
        migrations.AlterField(
            model_name='radicacionmodel',
            name='datetime_factura2',
            field=models.DateTimeField(blank=True, null=True, verbose_name='fecha final de la factura'),
        ),
        migrations.AlterField(
            model_name='radicacionmodel',
            name='datetime_radicado',
            field=models.DateField(blank=True, default=datetime.date(2020, 12, 9), verbose_name='fecha de radicación'),
        ),
    ]
