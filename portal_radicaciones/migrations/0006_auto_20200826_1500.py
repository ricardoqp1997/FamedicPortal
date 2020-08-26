# Generated by Django 3.0.3 on 2020-08-26 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_radicaciones', '0005_auto_20200826_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radicacionmodel',
            name='aproved',
            field=models.BooleanField(choices=[(True, 'Radicado aprobado'), (False, 'Radicado no aprobado')], default=False, verbose_name='estado de radicado'),
        ),
    ]