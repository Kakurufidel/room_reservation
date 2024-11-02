from django.db import models
from reservation.apps.authentication.models import User
from django.utils import timezone


class ReservationQuerySet(models.QuerySet):
    def active(self):
        return self.filter(deleted_at__isnull=True)

    def created_by_user(self, user):
        return self.filter(created_by=user)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True
    )
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    objects = ReservationQuerySet.as_manager()

    class Meta:
        abstract = True

    @classmethod
    def is_room_available(cls, room, date_start, date_end):
        """
        Vérifie si la salle est disponible entre deux dates.
        """
        return not cls.objects.filter(
            room=room,
            date_start__lt=date_end,
            date_end__gt=date_start,
            deleted_at__isnull=True,
        ).exists()

    def cancel(self):
        """
        Annule la réservation et met à jour le statut de la salle.
        """
        self.deleted_at = timezone.now()
        self.status = "available"
        self.save()
