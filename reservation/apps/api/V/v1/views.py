from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .serializer import (
    ReservationSerializer,
    RoomSerializer,
    UserRequestHistorySerializer,
)
from .permissions import IsAdminOrReadOnly
from reservation.models import Reservation, Room
from reservation.apps.authentication.models import UserRequestHistory
from rest_framework.pagination import PageNumberPagination


# Pagination personnalisée pour les réservations
class ReservationPagination(PageNumberPagination):
    page_size = 10  # Nombre d'éléments par page
    page_size_query_param = "page_size"
    max_page_size = 100


# Pagination personnalisée pour l'historique des actions utilisateurs
class UserRequestHistoryPagination(PageNumberPagination):
    page_size = 15  # Nombre d'éléments par page
    page_size_query_param = "page_size"
    max_page_size = 100


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]  # Recherche par nom de la salle
    ordering_fields = ["name", "capacity"]  # Champs triables
    ordering = ["name"]  # Ordre par défaut


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.active().select_related(
        "room", "created_by"
    )  # Optimisation avec select_related
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "room__name",
        "created_by__username",
    ]  # Recherche par nom de salle ou d'utilisateur
    ordering_fields = ["date_start", "date_end"]  # Tri par date
    ordering = ["date_start"]  # Ordre par défaut
    pagination_class = ReservationPagination  # Pagination personnalisée

    def perform_create(self, serializer):
        """
        Assigne automatiquement l'utilisateur connecté et vérifie la disponibilité de la salle.
        """
        room = serializer.validated_data["room"]
        date_start = serializer.validated_data["date_start"]
        date_end = serializer.validated_data["date_end"]

        if not Reservation.is_room_available(room, date_start, date_end):
            raise serializers.ValidationError(
                {
                    "room": "Cette salle n'est pas disponible pour les dates sélectionnées."
                }
            )

        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        """
        Permet la mise à jour d'une réservation.
        """
        serializer.save(updated_at=timezone.now())

    def perform_destroy(self, instance):
        """
        Annule la réservation en mettant à jour le champ `deleted_at`.
        """
        instance.cancel()


class UserRequestHistoryViewSet(viewsets.ModelViewSet):
    queryset = UserRequestHistory.objects.select_related("user").order_by(
        "-timestamp"
    )  # Optimisation avec select_related
    serializer_class = UserRequestHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = [
        "user__username",
        "action",
        "path",
    ]  # Recherche par utilisateur, action ou chemin
    ordering_fields = ["timestamp", "action"]  # Tri par horodatage ou type d'action
    ordering = ["-timestamp"]  # Ordre par défaut (décroissant)
    pagination_class = UserRequestHistoryPagination  # Pagination personnalisée
