from django.shortcuts import render, redirect
from .models import Room, Reservation
from .forms import ReservationForm, RoomForm
from django.contrib.auth.decorators import login_required


def list_rooms(request):
    rooms = Room.objects.all()
    return render(request, "list_rooms.html", {"rooms": rooms})


@login_required
def reserver_room(request, room_id, room_name):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.room_id = room_id
            reservation.save()
            return redirect(
                "confirmation_page", room_name=room_name
            )  # Redirection correcte
    else:
        form = ReservationForm()
    return render(request, "reserver_room.html", {"form": form, "room_name": room_name})


def confirmation_page(request, room_name):
    return render(
        request, "confirmation_page.html", {"room_name": room_name}
    )  # Passage du contexte correct


@login_required
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
    reservations = Reservation.objects.filter(created_by=request.user)
    return render(request, "list_reservations.html", {"reservations": reservations})


# je dois revoir ceci


# class RoomListAPI(APIView):
#     def get(self, request):
#         rooms = Room.objects.all()
#         return Response([room.name for room in rooms])


# class ModifierRoomAPI(APIView):
#     def put(self, request, pk):
#         room = room.objects.get(pk=pk)
#         form = RoomForm(request.data, instance=room)
#         if form.is_valid():
#             form.save()
#             return Response({"message": "La salle a ete  modifiee avec succes"})
#         return Response(form.errors, status=400)


# class DeleteRoomAPI(APIView):
#     def delete(self, request, pk):
#         room = Room.objects.get(pk=pk)
#         room.delete()
#         return Response({"message": "La salle a  t  supprim e avec succ s"})


# class ReserverRoom(APIView):
#     def post(self, request):
#         form = ReservationForm(request.data)
#         if form.is_valid():
#             reservation = form.save(commit=False)
#             reservation.user = request.user
#             reservation.save()
#             return Response({"message": "La salle a ete  reservee avec succes"})
#         return Response(form.errors, status=400)
