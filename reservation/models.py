from django.db import models
from .apps.core.models import BaseModel


class Room(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    locate = models.CharField(max_length=200)
    capacity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=1)

    def __str__(self):
        return self.name


class Reservation(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return f"Reservation for {self.room.name} from {self.date_start} to {self.date_end}"
