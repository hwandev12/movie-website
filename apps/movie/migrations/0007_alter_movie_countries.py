# Generated by Django 5.0 on 2024-03-28 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0006_alter_movie_countries'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='countries',
            field=models.CharField(choices=[], max_length=200, null=True),
        ),
    ]