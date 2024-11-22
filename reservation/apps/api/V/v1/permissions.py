from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Permission qui permet aux administrateurs d'effectuer toutes les actions,
    mais qui permet aux utilisateurs non administrateurs de ne faire que des actions de lecture (GET).
    """

    def has_permission(self, request, view):
        # Si la requête est une action de lecture (GET, HEAD, OPTIONS), permet l'accès
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Sinon, vérifie si l'utilisateur est administrateur
        return request.user and request.user.is_staff
