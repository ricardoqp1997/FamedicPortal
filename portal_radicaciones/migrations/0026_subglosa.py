# Generated by Django 3.1.3 on 2020-12-01 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal_radicaciones', '0025_auto_20201201_1057'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subglosa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Subglosa_name', models.CharField(default='Subglosa', max_length=255, verbose_name='Nombre de Subglosa')),
                ('subglosa_status', models.BooleanField(choices=[(True, 'Glosa activa'), (False, 'Glosa inactiva')], default=True, verbose_name='estado de la glosa')),
                ('glosa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal_radicaciones.glosa', verbose_name='Glosa correspondiente')),
            ],
            options={
                'verbose_name': 'Subglosa',
            },
        ),
    ]
