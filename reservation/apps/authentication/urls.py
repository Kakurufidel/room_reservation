from django.urls import path
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from reservation.apps.authentication.views import (
    LoginView,
    RegistrationView,
    LogoutView,
    ListRoomsView,
    ReserverRoomView,
    NewRoomView,
    ListReservationsView,
    UserHistoryView,
    ModifyReservationView,
    DeleteReservationView,
    ConfirmDeleteReservationView,
    ConfirmationReservationView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", RegistrationView.as_view(), name="register"),
    path("", ListRoomsView.as_view(), name="list_rooms"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "reservation/<int:room_id>/<str:room_name>/",
        ReserverRoomView.as_view(),
        name="reserver_room",
    ),
    path(
        "confirmation/<int:reservation_id>/",
        ConfirmationReservationView.as_view(),
        name="confirmation_reservation",
    ),
    path("new_room/", NewRoomView.as_view(), name="new_room"),
    path(
        "list_reservations/", ListReservationsView.as_view(), name="list_reservations"
    ),
    path("history/", UserHistoryView.as_view(), name="user_history"),
    path(
        "reservation/modify/<int:pk>/",
        ModifyReservationView.as_view(),
        name="modify_reservation",
    ),
    path(
        "reservation/confirm_delete/<int:pk>/",
        ConfirmDeleteReservationView.as_view(),
        name="confirm_delete_reservation",
    ),
    path(
        "reservation/delete/<int:pk>/",
        DeleteReservationView.as_view(),
        name="delete_reservation",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
