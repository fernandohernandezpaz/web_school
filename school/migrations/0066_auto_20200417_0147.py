# Generated by Django 2.2.10 on 2020-04-17 01:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0065_auto_20200417_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='cellphone',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(11111111, 'El Teléfono debe tener 8 digitos'), django.core.validators.MaxValueValidator(99999999, 'El Teléfono debe tener 8 digitos')], verbose_name='Teléfono'),
        ),
        migrations.AlterField(
            model_name='family',
            name='mobile',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(11111111, 'El Celular debe tener 8 digitos'), django.core.validators.MaxValueValidator(99999999, 'El Celular debe tener 8 digitos')], verbose_name='Celular'),
        ),
    ]