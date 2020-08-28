# Generated by Django 3.0.3 on 2020-08-27 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_radicaciones', '0003_auto_20200827_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='radicacionmodel',
            name='aproved',
            field=models.CharField(choices=[('SINAP', 'Sin verificar'), ('RADSI', 'Radicado aprobado'), ('RADNO', 'Radicado no aprobado')], default='SINAP', max_length=5, verbose_name='estado de radicado'),
        ),
    ]
