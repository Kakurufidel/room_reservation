from django.utils.timezone import now
from .models import UserRequestHistory


class UserRequestHistoryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Crée un enregistrement de l'historique de l'utilisateur
            UserRequestHistory.objects.create(
                path=request.path,
                user=request.user,  # Définit le champ created_by avec l'utilisateur
            )
            print(f"User {request.user.username} accessed {request.path} at {now()}")

        response = self.get_response(request)
        return response
