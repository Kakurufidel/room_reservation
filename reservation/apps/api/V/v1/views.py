from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from reservation.apps.authentication.models import User
from .users_filter import UserReservationsFilter, RoomFilter

from .serializer import (
    ReservationSerializer,
    RoomSerializer,
    UserHistorySerializer,
    UserSerializer,
)
from .permissions import IsAdminOrReadOnly
from reservation.models import Reservation, Room
from reservation.apps.authentication.models import UserRequestHistory
from reservation.apps.core.pagination import LargeResultsSetPagination


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = UserReservationsFilter
    ordering_fields = ["username", "profession"]  # Tri by date
    ordering = ["username"]  # default
    pagination_class = LargeResultsSetPagination


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filterset_class = RoomFilter
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ["name", "capacity", "price"]
    ordering_fields = ["name", "capacity", "price"]
    ordering = ["name"]
    pagination_class = LargeResultsSetPagination


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.active().select_related("room", "created_by")
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    search_fields = ["room__name", "created_by__username"]
    ordering_fields = ["date_start", "date_end"]
    ordering = ["date_start"]
    pagination_class = LargeResultsSetPagination

    def perform_create(self, serializer):
        room = serializer.validated_data["room"]
        date_start = serializer.validated_data["date_start"]
        date_end = serializer.validated_data["date_end"]

        if not Reservation.is_room_available(room, date_start, date_end):
            raise serializer.ValidationError(
                {"room": "Cette salle n'est pas disponible pour la date selectionee"}
            )

        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_at=timezone.now())

    def perform_destroy(self, instance):
        instance.cancel()


class UserRequestHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = UserHistorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LargeResultsSetPagination

    def get_queryset(self):
        if self.request.user.is_staff:
            user_id = self.request.query_params.get("user_id", None)
            if user_id:
                return (
                    UserRequestHistory.objects.filter(user_id=user_id)
                    .select_related("user")
                    .order_by("-timestamp")
                )
            return UserRequestHistory.objects.select_related("user").order_by(
                "-timestamp"
            )
        return (
            UserRequestHistory.objects.filter(user=self.request.user)
            .select_related("user")
            .order_by("-timestamp")
        )

    search_fields = ["user__username", "action", "path"]
    ordering_fields = ["timestamp", "action"]
    ordering = ["-timestamp"]
