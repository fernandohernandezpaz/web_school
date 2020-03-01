# Generated by Django 3.0.3 on 2020-03-01 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0015_auto_20200227_2354'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.CharField(max_length=1, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Nombre')),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Género',
                'verbose_name_plural': 'Géneros',
            },
        ),
        migrations.AlterField(
            model_name='family',
            name='document',
            field=models.CharField(max_length=16, unique=True, verbose_name='Cédula'),
        ),
    ]
