# Generated by Django 2.2.10 on 2020-04-07 03:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0047_notecontroledition'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='matriculationgradesection',
            unique_together={('matriculation', 'gradesection')},
        ),
    ]