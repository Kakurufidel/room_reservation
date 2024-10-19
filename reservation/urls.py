from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('', views.list_rooms, name='list_rooms'),
    path('reserver_room', views.reserver_room, name='reserver_room'),
    path('reserve/<int:room_id>/', views.reserver_room, name='reserver_room'),
    path('list_reservations', views.list_reservations, name='list_reservations'),
    path('new_room', views.new_room, name='new_room'),
    path('api/rooms/', views.RoomListAPI.as_view(), name='room_list_api'),
    path('api/salle/<int:pk>/', views.ModifierRoomAPI.as_view(), name='modifier_room_api'),
    path('api/salle/<int:pk>/delete/', views.DeleteRoomAPI.as_view(), name='delete_room_api'),
    path('api/reservation/', views.ReserverRoom.as_view(), name='ReserverRoom_api'),
]
