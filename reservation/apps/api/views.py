from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from reservation.models import Room, Reservation
from .serializers import (
    UserSerializer,
    RoomSerializer,
    ReservationSerializer,
    UserRegistrationSerializer,
)

User = get_user_model()


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class RoomListAPI(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ModifierRoomAPI(generics.RetrieveUpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class DeleteRoomAPI(generics.DestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class ReserverRoom(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LogoutView(APIView):
    """
    View to logout by deleting the user's token.
    """

    def post(self, request):
        if request.user.is_authenticated:
            try:
                token = Token.objects.get(user=request.user)
                token.delete()
                return Response(
                    {"message": "Déconnexion réussie."}, status=status.HTTP_200_OK
                )
            except Token.DoesNotExist:
                return Response(
                    {"error": "Token non trouvé."}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {"error": "Utilisateur non authentifié."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {"token": token.key, "message": "Bien enregistré."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
