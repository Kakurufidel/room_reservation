from django.contrib import admin
from django.urls import path
from .views import logout_view
from . import views
from .views import reserver_room


urlpatterns = [
    path("admin/", admin.site.urls),
    path("logout/", logout_view, name="api_logout"),
    # path("", include("authentication.urls")),
    path("", views.list_rooms, name="list_rooms"),
    path(
        "reserve/<int:room_id>/<str:room_name>/",
        views.reserver_room,
        name="reserver_room",
    ),
    path(
        "confirmation/<str:room_name>/",
        views.confirmation_page,
        name="confirmation_page",
    ),
    path("list_reservations", views.list_reservations, name="list_reservations"),
    path("new_room", views.new_room, name="new_room"),
]


# from django.contrib import admin
# from django.urls import path, include
# from . import views
# from .views import reserver_room


# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("", include("authentication.urls")),
#     path("", views.list_rooms, name="list_rooms"),
#     path("reserve/<int:room_id>/<str:room_name>/", views.reserver_room,name="reserver_room"),
#     path("confirmation/<str:room_name>/",views.confirmation_page,name="confirmation_page"),
#     path("list_reservations", views.list_reservations, name="list_reservations"),
#     path("new_room", views.new_room, name="new_room"),
# ]
