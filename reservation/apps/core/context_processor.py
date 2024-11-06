from reservation.models import Reservation


def user_reservations_context(request):
    if request.user.is_authenticated:
        reservations = Reservation.objects.filter(created_by=request.user)
        return {"reservations": reservations}
    return {}


def user_request_history(request):
    if request.user.is_authenticated:
        history = request.session.get("history", [])
        return {"user_request_history": history}
    return {}
