from django.contrib import admin
from reservation.models import Reservation, Room
from reservation.apps.authentication.models import User


class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "locate", "capacity", "created_by")


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email")


class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "room", "date_start", "date_end", "created_by")


admin.site.register(User, UserAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Reservation, ReservationAdmin)
