# Generated by Django 2.2.13 on 2020-11-17 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0080_merge_20200915_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='document',
            field=models.CharField(help_text='<strong style="color: black">Formato xxx-xxxxxx-xxxxL</strong>', max_length=16, unique=True, verbose_name='Cédula'),
        ),
    ]
