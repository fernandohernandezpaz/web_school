# Generated by Django 3.0.3 on 2020-03-02 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0018_auto_20200302_0707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='family_role',
            field=models.CharField(choices=[('ABUELO/A', 'ABUELO/A'), ('TIO/A', 'TIO/A'), ('PAPA', 'PAPA'), ('MAMA', 'MAMA'), ('HERMANO/A', 'HERMANO/A')], max_length=20, verbose_name='Rol Familiar'),
        ),
    ]