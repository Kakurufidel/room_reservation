from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from reservation.models import Room, Reservation
from reservation.forms import ReservationForm, RoomForm
from .forms import UserCreationForm, UserLoginForm
from django.views.generic import TemplateView
from django.views.generic import UpdateView
from django.urls import reverse
from django.utils import timezone

# from reservation.apps.core.models import UserRequestHistory


class RegistrationView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Inscription réussie. Vous pouvez maintenant vous connecter."
            )
            return redirect("login")
        return render(request, "register.html", {"form": form})


class LoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print("tout est bon")
                return redirect("list_rooms")
            else:
                messages.error(request, "Nom d’utilisateur ou mot de passe incorrect.")
        return render(request, "login.html", {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")


class ListRoomsView(View):
    def get(self, request):
        rooms = Room.objects.all()
        return render(request, "list_rooms.html", {"rooms": rooms})


class ReserverRoomView(LoginRequiredMixin, View):
    def get(self, request, room_id, room_name):
        form = ReservationForm()
        return render(
            request, "reserver_room.html", {"form": form, "room_name": room_name}
        )

    def post(self, request, room_id, room_name):
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.room_id = room_id
            reservation.save()
            return render(request, "confirmation_page.html", {"room_name": room_name})
        return render(
            request, "reserver_room.html", {"form": form, "room_name": room_name}
        )


class ConfirmationPageView(View):
    def get(self, request, room_name):
        return render(request, "confirmation_page.html", {"room_name": room_name})


class NewRoomView(LoginRequiredMixin, View):
    def get(self, request):
        form = RoomForm()
        return render(request, "new_room.html", {"form": form})

    def post(self, request):
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.save()
            return redirect("list_rooms")
        return render(request, "new_room.html", {"form": form})


class ListReservationsView(LoginRequiredMixin, View):
    def get(self, request):
        user_reservations = Reservation.objects.all()
        return render(
            request, "list_reservations.html", {"reservation": user_reservations}
        )


class UserHistoryView(TemplateView):
    template_name = "user_history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 'user_request_history' est supposé être ajouté au contexte par le middleware
        context["user_history"] = self.request.user.request_history.all()
        return context


# modification de la reservation


class ModifyReservationView(UpdateView):
    model = Reservation
    fields = ["room", "date_start", "date_end", "status"]
    template_name = "modify_reservation.html"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
        # on redirige

    def get_success_url(self):
        return reverse("list_reservations")


# pour la suppresion


class ConfirmDeleteReservationView(View):
    def get(self, request, pk):
        reservation = get_object_or_404(
            Reservation, pk=pk, created_by=request.user, is_delete=False
        )
        return render(request, "confirm_delete.html", {"reservation": reservation})


class DeleteReservationView(View):
    def post(self, request, pk):
        reservation = get_object_or_404(
            Reservation, pk=pk, created_by=request.user, is_delete=False
        )
        # on change le statu de is_delete
        reservation.is_delete = True
        reservation.deleted_at = timezone.now()
        reservation.save()
        return redirect("list_reservations")


# pour le middleware

# class UserHistoryView(TemplateView):
#     template_name = 'user_history.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Récupère l'historique des actions de l'utilisateur authentifié
#         context['user_history'] = UserRequestHistory.objects.filter(created_by=self.request.user).order_by('-created_at')
#         return context
