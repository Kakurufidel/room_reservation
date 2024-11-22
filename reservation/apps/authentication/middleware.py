from django.utils.timezone import now
from .models import UserRequestHistory


class UserRequestHistoryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            action = None
            # le type d'action suppression
            # Par exemple :
            if request.method == "POST" and "edit" in request.path:
                action = "update"
            elif request.method == "POST" and "delete" in request.path:
                action = "delete"
            elif request.method == "POST" and "create" in request.path:
                action = "create"

            # Créez un enregistrement d'historique avec action
            if action:
                UserRequestHistory.objects.create(
                    path=request.path, user=request.user, action=action
                )
            print(f"User {request.user.username} performed {action} at {now()}")

        response = self.get_response(request)
        return response
