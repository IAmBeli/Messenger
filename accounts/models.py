from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    display_name = models.CharField(max_length=64, blank=True)
    avatar = models.ImageField(upload_to="avatars/",blank=True)
    bio = models.CharField(max_length=70, blank=True)

    def __str__(self):
        return self.display_name or self.username