from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        if not self.pk:
            # New instance, hash the password
            self.set_password(self.password)
        super().save(*args, **kwargs)
        
    class Meta:
        app_label = 'src'
    
