# Generated by Django 3.0.3 on 2020-09-15 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('famedic_users', '0003_famedicuser_updated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='famedicuser',
            name='phone',
            field=models.CharField(max_length=10, null=True, unique=True, verbose_name='teléfono celular'),
        ),
    ]
