# Generated by Django 5.0 on 2024-03-28 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0005_alter_series_countries'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='countries',
            field=models.CharField(choices=[], max_length=200, null=True),
        ),
    ]
