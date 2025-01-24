from django.db import models
from reservation.apps.core.models import BaseModel
from django.utils import timezone
from django.core.exceptions import ValidationError


class Room(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    locate = models.CharField(max_length=200)
    image_room = models.ImageField(
        verbose_name="image_Room", upload_to="images/", null=True, blank=True
    )
    capacity = models.IntegerField()
    price = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name


class Reservation(BaseModel):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True, blank=True)
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()
    status = models.CharField(max_length=20, default="encour")
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"Reservation for {self.room.name} from {self.date_start} to {self.date_end}"

    # Méthode de validation pour vérifier les dates
    def clean(self):
        if self.date_start < timezone.now():
            raise ValidationError("La date de début ne peut pas être dans le passé.")
        if self.date_end <= self.date_start:
            raise ValidationError("La date de fin doit être après la date de début.")
