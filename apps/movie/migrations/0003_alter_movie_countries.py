# Generated by Django 5.0 on 2024-03-27 07:38

import django_countries.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_alter_movie_countries'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='countries',
            field=django_countries.fields.CountryField(max_length=746, multiple=True),
        ),
    ]
