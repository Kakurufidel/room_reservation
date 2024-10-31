from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView, LogoutView
from .views import RoomListAPI, ModifierRoomAPI, DeleteRoomAPI, ReserverRoom

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", obtain_auth_token, name="login"),
    path("logout/", LogoutView.as_view(), name="api_logout"),
    path("api/V1/rooms/", RoomListAPI.as_view(), name="room_list_api"),
    path("api/V1/rooms/<int:pk>/", ModifierRoomAPI.as_view(), name="modifier_room_api"),
    path(
        "api/V1/rooms/<int:pk>/delete/", DeleteRoomAPI.as_view(), name="delete_room_api"
    ),
    path("api/V1/reservation/", ReserverRoom.as_view(), name="reserver_room_api"),
]
