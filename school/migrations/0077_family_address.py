# Generated by Django 2.2.13 on 2020-09-13 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0076_auto_20200913_2235'),
    ]

    operations = [
        migrations.AddField(
            model_name='family',
            name='address',
            field=models.TextField(default='', max_length=255, verbose_name='Dirección'),
        ),
    ]