# Generated by Django 3.1.3 on 2020-11-30 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_radicaciones', '0021_auto_20201130_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='glosa',
            name='glosa_valor',
            field=models.IntegerField(null=True, verbose_name='valor asignar a la glosa'),
        ),
    ]