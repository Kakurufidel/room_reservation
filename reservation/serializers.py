from rest_framework import serializers
from .models import Room, Reservation


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "_all_"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "_all_"


def create(self, validated_data):

    return Reservation.objects.create(**validated_data)
