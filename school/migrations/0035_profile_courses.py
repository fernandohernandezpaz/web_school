# Generated by Django 3.0.3 on 2020-03-14 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0034_auto_20200314_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='courses',
            field=models.ManyToManyField(to='school.Course', verbose_name='Asignaturas'),
        ),
    ]
