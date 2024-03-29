# Generated by Django 5.0 on 2024-03-28 05:54

import apps.movie.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0007_alter_episode_video_alter_series_countries'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='video',
            field=apps.movie.models.VideoFileField(blank=True, null=True, upload_to='series/videos/'),
        ),
    ]