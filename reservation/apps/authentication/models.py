from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profession = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username
