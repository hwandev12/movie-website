# Generated by Django 5.0 on 2024-03-29 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('series', '0008_alter_episode_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='episode',
            name='video',
        ),
    ]