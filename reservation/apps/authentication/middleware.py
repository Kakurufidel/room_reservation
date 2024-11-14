from django.utils.timezone import now
from .models import UserRequestHistory


class UserRequestHistoryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            action_type = None
            # Déterminez ici le type d'action (création, modification, suppression, etc.)
            # Par exemple :
            if request.method == "POST" and "edit" in request.path:
                action_type = "update"
            elif request.method == "POST" and "delete" in request.path:
                action_type = "delete"
            elif request.method == "POST" and "create" in request.path:
                action_type = "create"

            # Créez un enregistrement d'historique avec action_type
            if action_type:
                UserRequestHistory.objects.create(
                    path=request.path,
                    user=request.user,
                    action_type=action_type,
                )
            print(f"User {request.user.username} performed {action_type} at {now()}")

        response = self.get_response(request)
        return response
