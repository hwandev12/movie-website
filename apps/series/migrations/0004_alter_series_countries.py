# Generated by Django 5.0 on 2024-03-27 08:18

import django_countries.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0003_alter_series_countries'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='countries',
            field=django_countries.fields.CountryField(max_length=2),
        ),
    ]
