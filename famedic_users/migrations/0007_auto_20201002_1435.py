# Generated by Django 3.0.3 on 2020-10-02 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('famedic_users', '0006_auto_20200915_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='famedicuser',
            name='recovery_email',
            field=models.EmailField(max_length=255, null=True, verbose_name='correo electrónico de recuperación'),
        ),
    ]
