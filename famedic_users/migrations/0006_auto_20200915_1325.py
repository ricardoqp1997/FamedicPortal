# Generated by Django 3.0.3 on 2020-09-15 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('famedic_users', '0005_auto_20200915_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='famedicuser',
            name='profile_foto',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='foto de perfil'),
        ),
    ]
