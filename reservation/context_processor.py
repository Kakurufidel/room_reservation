from .models import Reservation


def user_reservations(request):
    if request.user.is_authenticated:
        reservations = Reservation.objects.filter(created_byr=request.user)
        return {"user_reservations": reservations}
    return {"user_reservations": []}
