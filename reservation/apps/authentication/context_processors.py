from django.contrib.auth import get_user_model
from reservation.models import Reservation, Room
from django.utils.translation import get_language
from django.conf import settings


def user_info(request):
    if request.user.is_authenticated:
        return {
            "user_info": request.user.username,
            "initial": request.user.username[:2].upper(),
            # "reservation" : request.reservation
        }
    return {}


def language_context(request):
    return {
        "LANGUAGE_CODE": get_language(),
        "LANGUAGES": settings.LANGUAGES,
    }
