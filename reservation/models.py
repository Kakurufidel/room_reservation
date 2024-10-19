from django.db import models
from authentication.models import User

class Room(models.Model):
    name = models.CharField(max_length=100)
    locate = models.CharField(max_length=200)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Reservation(models.Model):
    room = models.CharField(max_length=255)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Reservation for {self.room} from {self.date_start} to {self.date_end}"

    class Meta:
        unique_together = ('room', 'date_start', 'date_end')