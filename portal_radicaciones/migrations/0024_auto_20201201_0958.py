# Generated by Django 3.1.3 on 2020-12-01 14:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_radicaciones', '0023_auto_20201130_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radicacionmodel',
            name='datetime_radicado',
            field=models.DateField(blank=True, default=datetime.date(2020, 12, 1), verbose_name='fecha de radicación'),
        ),
    ]