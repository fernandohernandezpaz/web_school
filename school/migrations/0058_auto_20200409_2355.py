# Generated by Django 2.2.10 on 2020-04-09 23:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0057_auto_20200409_2348'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='coursegradesection',
            unique_together={('course', 'grade_section')},
        ),
    ]
