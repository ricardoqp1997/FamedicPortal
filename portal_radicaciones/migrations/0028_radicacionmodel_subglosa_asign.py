# Generated by Django 3.1.3 on 2020-12-01 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal_radicaciones', '0027_auto_20201201_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='radicacionmodel',
            name='subglosa_asign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='portal_radicaciones.subglosa', verbose_name='subglosa'),
        ),
    ]
