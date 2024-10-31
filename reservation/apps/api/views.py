from django.contrib.auth.models import User
from .serializer import UserSerializer
from rest_framework import generics
from rest_framework.permissions import IsAdminUser


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
)
from authentication.models import Room, Reservation
from serializers import RoomSerializer, ReservationSerializer


class RoomListAPI(ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ModifierRoomAPI(RetrieveUpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class DeleteRoomAPI(DestroyAPIView):
    queryset = Room.objects.all()


class ReserverRoom(CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


def perform_create(self, serializer):
    serializer.save(user=self.request.user)
