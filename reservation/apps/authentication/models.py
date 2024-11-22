# from django.db import models
# from django.contrib.auth.models import AbstractUser


# class User(AbstractUser):
#     name = models.CharField(max_length=100, blank=True)
#     contact = models.CharField(max_length=100, blank=True)
#     profession = models.CharField(max_length=100, blank=True)
#     email = models.EmailField(unique=True)
#     address = models.CharField(max_length=255, blank=True)

#     def __str__(self):
#         return self.username


# verification pour le middleware
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    name = models.CharField(max_length=100, blank=True)
    contact = models.CharField(max_length=100, blank=True)
    profession = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username


class UserRequestHistory(models.Model):
    ACTION_CHOICES = [
        ("reservation", "Réservation"),
        ("modification", "Modification"),
        ("suppression", "Suppression"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="request_history"
    )
    path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} at {self.timestamp}"
