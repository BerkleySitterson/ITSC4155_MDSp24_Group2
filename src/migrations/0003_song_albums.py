# Generated by Django 5.0.3 on 2024-05-05 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0002_album_alter_user_options_alter_user_username_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='albums',
            field=models.ManyToManyField(blank=True, related_name='song_albums', to='src.album'),
        ),
    ]
