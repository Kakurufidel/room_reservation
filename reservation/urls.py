from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path("register/", RegisterView.as_view(), name="register"),
    #  path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("", include("reservation.apps.authentication.urls")),
    path("", include("reservation.apps.api.urls")),
    # path("/", include("reservation.apps.core.urls")),
    #     path("login/", obtain_auth_token, name="login"),
    #     path("logout/", LogoutView.as_view(), name="api_logout"),
    #     # path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    #     path("", views.list_rooms, name="list_rooms"),
    #     path("reserve/<int:room_id>/<str:room_name>/",views.reserver_room,name="reserver_room"),
    #     path("confirmation/<str:room_name>/",views.confirmation_page,name="confirmation_page"),
    #     path("list_reservations", views.list_reservations, name="list_reservations"),
    #     path("new_room", views.new_room, name="new_room"),
    #     path("api/V1/rooms/", views.RoomListAPI.as_view(), name="room_list_api"),
    #     path("api/V1/rooms/<int:pk>/",views.ModifierRoomAPI.as_view(),name="modifier_room_api"),
    #     path("api/V1/rooms/<int:pk>/delete/",views.DeleteRoomAPI.as_view(),name="delete_room_api"),
    #     path("api/V1/reservation/", views.ReserverRoom.as_view(), name="ReserverRoom_api"),
]
