# Generated by Django 3.1.3 on 2020-11-30 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_radicaciones', '0020_auto_20201130_0938'),
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
    ]
