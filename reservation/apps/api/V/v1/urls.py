from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    RoomViewSet,
    ReservationViewSet,
    UserRequestHistoryViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register(r"rooms", RoomViewSet, basename="rooms")
router.register(r"reservations", ReservationViewSet, basename="reservations")
router.register(r"history", UserRequestHistoryViewSet, basename="history")
router.register(r"users", UserViewSet, basename="users")
urlpatterns = [
    path("", include(router.urls)),
]
