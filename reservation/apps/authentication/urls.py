from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import set_language
from reservation.apps.authentication.views import (
    LoginView,
    RegistrationView,
    LogoutView,
    ListRoomsView,
    ReserverRoomView,
    NewRoomView,
    ListReservationsView,
    # UserHistoryView,  # Supprime cette ligne
    ModifyReservationView,
    DeleteReservationView,
    ConfirmDeleteReservationView,
    ConfirmationReservationView,
    HomeView,
    AdminDashboardView,
    CreateRoomView,
    RoomListView,
    RoomUpdateView,
    UserListView,
    RoomDeleteView,
    ReservationListAdminView,
)

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", RegistrationView.as_view(), name="register"),
    path("list_rooms", ListRoomsView.as_view(), name="list_rooms"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("", HomeView.as_view(), name="index"),
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
    path("set-language/", set_language, name="set_language"),
    path("admin-dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),
    path("create/", CreateRoomView.as_view(), name="create_room"),
    path("list/", RoomListView.as_view(), name="list_rooms_admin"),
    path("update/<int:pk>/", RoomUpdateView.as_view(), name="update_room"),
    path("delete/<int:pk>/", RoomDeleteView.as_view(), name="delete_room"),
    path("users/", UserListView.as_view(), name="user_list"),
    path(
        "list_reservations_admin/",
        ReservationListAdminView.as_view(),
        name="list_reservations_admin",
    ),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
