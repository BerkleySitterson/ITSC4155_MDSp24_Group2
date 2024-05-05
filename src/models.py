from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        

class Playlist(models.Model):
    """Model representing a playlist"""
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='playlists')

    def __str__(self):
        return self.name

class Song(models.Model):
    """Model representing a song"""
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    album = models.ForeignKey('Album', on_delete=models.CASCADE, related_name='songs', blank=True, null=True)
    playlist = models.ManyToManyField(Playlist, related_name='songs', blank=True)

    def __str__(self):
        return f"{self.title} - {self.artist}"

class Album(models.Model):
    """Model representing an album"""
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.title} - {self.artist}"
