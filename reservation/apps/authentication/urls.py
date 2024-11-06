from django.urls import path
from django.contrib import admin

from reservation.apps.authentication.views import (
    LoginView,
    RegistrationView,
    LogoutView,
    ListRoomsView,
    ReserverRoomView,
    ConfirmationPageView,
)
from reservation.apps.authentication.views import (
    NewRoomView,
    ListReservationsView,
    UserHistoryView,
    ModifyReservationView,
    DeleteReservationView,
    ConfirmDeleteReservationView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", LoginView.as_view(), name="login"),
    path("signup/", RegistrationView.as_view(), name="register"),
    path("rooms/", ListRoomsView.as_view(), name="list_rooms"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "reserve/<int:room_id>/<str:room_name>/",
        ReserverRoomView.as_view(),
        name="reserver_room",
    ),
    path(
        "confirmation/<str:room_name>/",
        ConfirmationPageView.as_view(),
        name="confirmation_page",
    ),
    path(
        "reservations/modify/<int:pk>/",
        ModifyReservationView.as_view(),
        name="modify_reservation",
    ),
    path(
        "reservations/delete/<int:pk>/",
        DeleteReservationView.as_view(),
        name="confirm_delete",
    ),
    path("new-room/", NewRoomView.as_view(), name="new_room"),
    path("reservations/", ListReservationsView.as_view(), name="list_reservations"),
    path("user_history/", UserHistoryView.as_view(), name="user_history"),
    path(
        "reservations/modify/<int:pk>/",
        ModifyReservationView.as_view(),
        name="modify_reservation",
    ),
    path(
        "reservations/delete/<int:pk>/",
        ConfirmDeleteReservationView.as_view(),
        name="confirm_delete",
    ),
    path(
        "reservations/delete/<int:pk>/confirm/",
        DeleteReservationView.as_view(),
        name="delete_reservation",
    ),  # URL pour confirmer la suppression
]
