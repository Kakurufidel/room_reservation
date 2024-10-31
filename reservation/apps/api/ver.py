# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from rest_framework.views import APIView
# from serializer import UserRegistrationSerializer, RoomSerializer, ReservationSerializer
# from .models import Room, Reservation

# class RegisterView(generics.CreateAPIView):
#     serializer_class = UserRegistrationSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         token, created = Token.objects.get_or_create(user=user)
#         headers = self.get_success_headers(serializer.data)
#         return Response({"token": token.key, "message": "bien enregistré."},status=status.HTTP_201_CREATED,headers=headers)

# class LogoutView(APIView):


#     def post(self, request):
#         if request.user.is_authenticated:
#             try:
#                 token = Token.objects.get(user=request.user)
#                 token.delete()
#                 return Response({"message": "Déconnexion réussie."}, status=status.HTTP_200_OK
# )
#             except Token.DoesNotExist:
#                 return Response({"error": "Token non trouvé."}, status=status.HTTP_400_BAD_REQUEST)
#         return Response({"error": "Utilisateur non authentifié."},status=status.HTTP_401_UNAUTHORIZED)

# class RoomListAPI(generics.ListAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer

# class ModifierRoomAPI(generics.RetrieveUpdateAPIView):
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer

# class DeleteRoomAPI(generics.DestroyAPIView):
#     queryset = Room.objects.all()

# class ReserverRoom(generics.CreateAPIView):
#     queryset = Reservation.objects.all()
#     serializer_class = ReservationSerializer

# def perform_create(self, serializer):
#     serializer.save(user=self.request.user)

# def create(self, request, *args, **kwargs):
#     room_id = request.data.get('room')
#         try :
#             room = Room.objects.get(id=room_id)
#         except Room.DoesNotExist:
#             return Response({"error": "Room not found"}, status=status.HTTP_404_NOT_FOUND)

#         if not Room.is_room_available(room, request.data.get('date_start'), request.data.get('date_end')):
#             return Response({"error": "Room is not available for the selected dates"}, status=status.HTTP_400_BAD_REQUEST)

#     return super().create(request, *args, **kwargs)
