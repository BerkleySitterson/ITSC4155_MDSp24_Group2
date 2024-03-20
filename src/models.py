from django.db import models

# This file is used to define the models for the application. This is where you define the structure of the database tables and the relationships between them.

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    
class Albums(models.Model):
    album_name = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    release_date = models.DateField()
    
class Songs(models.Model):
    title = models.CharField(max_length=50)
    artist = models.CharField(max_length=50)
    genre = models.CharField(max_length=50)
    release_date = models.DateField()
    album = models.ForeignKey(Albums, on_delete=models.CASCADE) # This foreign key indicates it is in a many-to-one relationship with the Albums table.