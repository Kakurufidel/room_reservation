from reservation.models import Room, Reservation
from reservation.views import ReservationForm, RoomForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import UserCreationForm, UserLoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print("tout est bon")
                return redirect("liste_salles")
            else:
                messages.error(request, "Nom d’utilisateur ou mot de passe incorrect.")
    else:
        form = UserLoginForm()
    return render(request, "login.html", {"form": form})


def logout_view(request):
    """
    Logs the user out and redirects to the success page.

    :param request: the request object
    :return: a redirect to the success page
    """
    logout(request)
    return redirect(login_view)


def list_rooms(request):
    rooms = Room.objects.all()
    return render(request, "list_rooms.html", {"rooms": rooms})


def reserver_room(request, room_id, room_name):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.room_id = room_id
            reservation.save()
            return redirect(
                request, f"confirmation/{room_name}", {"room_name": room_name}
            )
    else:
        form = ReservationForm()


def confirmation_page(request, room_name):
    return render(request, "confirmation_page.html", {"room_name": room_name})


def new_room(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.save()
            return redirect("list_rooms")
    else:
        form = RoomForm()
        return render(request, "new_room.html", {"form": form})


@login_required
def list_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, "list_reservations.html", {"reservations": reservations})


# class RegisterView(APIView):
#     def post(self, request):
#         serializer = UserRegistrationSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             token, created = Token.objects.get_or_create(user=user)
#             return Response(
#                 {"token": token.key, "message": "bien enreigistre."},
#                 status=status.HTTP_201_CREATED,
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LogoutView(APIView):
#     """
#     View to logout by deleting the user's token.
#     """

#     def post(self, request):
#         if request.user.is_authenticated:
#             try:
#                 token = Token.objects.get(user=request.user)
#                 token.delete()
#                 return Response(
#                     {"message": "Déconnexion réussie."}, status=status.HTTP_200_OK
#                 )
#             except Token.DoesNotExist:
#                 return Response(
#                     {"error": "Token non trouvé."}, status=status.HTTP_400_BAD_REQUEST
#                 )
#         return Response(
#             {"error": "Utilisateur non authentifié."},
#             status=status.HTTP_401_UNAUTHORIZED,
#         )
