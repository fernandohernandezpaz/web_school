# Generated by Django 3.0.3 on 2020-02-27 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0010_auto_20200227_2212'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Students',
            new_name='Student',
        ),
    ]