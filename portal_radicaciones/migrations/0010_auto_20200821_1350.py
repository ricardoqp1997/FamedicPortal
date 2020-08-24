# Generated by Django 3.0.3 on 2020-08-21 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal_radicaciones', '0009_auto_20200821_1253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='radicacionmodel',
            name='id_radicado',
        ),
        migrations.AlterField(
            model_name='radicacionmodel',
            name='regimen_type',
            field=models.CharField(choices=[('CT', 'Contributivo'), ('SB', 'Subsidiario')], default='CT', max_length=2, verbose_name='régimen'),
        ),
        migrations.AlterField(
            model_name='radicacionmodel',
            name='sede_select',
            field=models.CharField(choices=[('SOGA', 'Famedic - IPS Sogamoso'), ('CLAB', 'Famelab - Vital Medical Service'), ('TUNJ', 'Famedic - IPS Tunja'), ('DUIT', 'Famedic - IPS Duitama'), ('CLIB', 'Famedic - IPS Libertadores'), ('ARAU', 'Famedic - IPS Arauca'), ('MESP', 'Famedic - IPS Centro Especialistas'), ('MPLP', 'Famedic - IPS Puerto López'), ('MBAS', 'Famelab - IPS Básica'), ('ATAM', 'Famedic - Tame'), ('MPYP', 'Famedic - PYP'), ('CASN', 'Famedic - IPS Casanare'), ('MGRA', 'Famedic - IPS Granada'), ('MPGA', 'Famedic - IPS Puerto Gaitán'), ('CHIQ', 'Famedic - IPS Chiquinquirá'), ('CAQZ', 'Famedic - IPS Caquezá'), ('MACA', 'Famedic - IPS Acacias'), ('MVLL', 'Famelab - Villavicencio')], default='ARAU', max_length=4, verbose_name='sede correspondiente'),
        ),
    ]
