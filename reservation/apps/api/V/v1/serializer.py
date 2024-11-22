from rest_framework import serializers
from reservation.apps.authentication.models import User, UserRequestHistory
from reservation.models import Reservation, Room


# Sérialiseur pour les utilisateurs
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "name", "contact", "profession", "address")


# Sérialiseur pour l'historique des requêtes utilisateur
class UserRequestHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequestHistory
        fields = ("user", "path", "timestamp", "action")


# Sérialiseur pour les salles
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("id", "name", "capacity")


# Sérialiseur pour les réservations
class ReservationSerializer(serializers.ModelSerializer):
    room = RoomSerializer(
        read_only=True
    )  # En cas de besoin, vous pouvez exposer la salle réservée
    created_by = UserSerializer(
        read_only=True
    )  # Utilisateur ayant effectué la réservation

    class Meta:
        model = Reservation
        fields = (
            "id",
            "room",
            "date_start",
            "date_end",
            "status",
            "created_at",
            "created_by",
            "deleted_at",
        )

    def get_room_name(self, obj):
        return obj.room.name if obj.room else None
