from django.contrib.auth import get_user_model
from reservation.models import Reservation, Room


def user_info(request):
    if request.user.is_authenticated:
        return {
            "user_info": request.user.username,
            "initial": request.user.username[:2].upper(),
            # "reservation" : request.reservation
        }
    return {}
