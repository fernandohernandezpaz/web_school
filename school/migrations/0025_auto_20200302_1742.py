# Generated by Django 3.0.3 on 2020-03-02 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0024_auto_20200302_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matriculation',
            name='school_year',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='school.Grade', verbose_name='Año Escolar'),
        ),
    ]
