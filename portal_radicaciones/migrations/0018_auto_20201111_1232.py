# Generated by Django 3.1.3 on 2020-11-11 17:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_radicaciones', '0017_auto_20201110_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radicacionmodel',
            name='datetime_radicado',
            field=models.DateField(blank=True, default=datetime.date(2020, 11, 11), verbose_name='fecha de radicación'),
        ),
    ]