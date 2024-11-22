from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext as _
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
from django.core.paginator import Paginator
from django.db.models import Count
from django.conf import settings

# fonction pour la traduction
# def translate_text(text, target_language):
#     client = translate.Client()
#     result = client.translate(text, target_language=target_language)
#     return result['translatedText']


class RegistrationView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                _("Inscription réussie. Vous pouvez maintenant vous connecter."),
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
                return redirect("list_rooms")
            else:
                messages.error(
                    request, _("Nom d’utilisateur ou mot de passe incorrect.")
                )
        return render(request, "login.html", {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("login")

        """
        Traite le formulaire de changement de langue et redirige l'utilisateur.
        """


class ListRoomsView(LoginRequiredMixin, View):
    def get(self, request):
        rooms_list = Room.objects.annotate(reservation_count=Count("reservation"))

        # Pagination
        paginator = Paginator(rooms_list, 8)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # Récupérer le nom d'utilisateur de la session
        username = request.session.get("username")
        return render(
            request, "list_rooms.html", {"page_obj": page_obj, "username": username}
        )


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
            reservation.created_by = request.user
            reservation.room_id = room_id
            reservation.save()
            return redirect("confirmation_reservation", reservation_id=reservation.id)

        return render(
            request, "reserver_room.html", {"form": form, "room_name": room_name}
        )


class ConfirmationReservationView(View):
    def get(self, request, reservation_id):
        reservation = get_object_or_404(
            Reservation, id=reservation_id, created_by=request.user
        )
        # Récupérer le nom de la salle réservée
        room_name = reservation.room.name

        # Afficher la page de confirmation avec le nom de la salle
        return render(request, "confirmation_page.html", {"room_name": room_name})


class NewRoomView(LoginRequiredMixin, View):
    def get(self, request):
        form = RoomForm()
        return render(request, "new_room.html", {"form": form})

    def post(self, request):
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            room = form.save(commit=False)
            room.save()
            return redirect("list_rooms")
        return render(request, "new_room.html", {"form": form})


class ListReservationsView(LoginRequiredMixin, View):
    def get(self, request):
        user_reservations = Reservation.objects.filter(
            created_by=request.user, is_delete=False
        )

        # pagination
        paginator_reservation = Paginator(user_reservations, 5)
        page_number = request.GET.get("page")
        page_obj = paginator_reservation.get_page(page_number)
        return render(request, "list_reservations.html", {"page_obj": page_obj})


class UserHistoryView(TemplateView):
    template_name = "user_history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Récupérer l'historique des faits de l'utilisateur
        user_history = self.request.user.request_history.all()

        # piginer l'histoirique
        paginator = Paginator(user_history, 10)  # 10 éléments par page

        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # Ajouter la pagination à ton contexte
        context["page_obj"] = page_obj
        return context


class ModifyReservationView(UpdateView):
    model = Reservation
    fields = ["room", "date_start", "date_end", "status"]
    template_name = "modify_reservation.html"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("list_reservations")


class DeleteReservationView(View):
    def post(self, request, pk):
        # recuperation
        reservation = get_object_or_404(
            Reservation, pk=pk, created_by=request.user, is_delete=False
        )

        # on bascule is_delete en true
        reservation.is_delete = True
        reservation.deleted_at = timezone.now()
        reservation.save()

        # Rediriger vers la liste des réservations
        return redirect("list_reservations")


class ConfirmDeleteReservationView(View):
    def get(self, request, pk):
        reservation = get_object_or_404(
            Reservation, pk=pk, created_by=request.user, is_delete=False
        )
        return render(request, "confirm_delete.html", {"reservation": reservation})

    def post(self, request, pk):
        reservation = get_object_or_404(
            Reservation, pk=pk, created_by=request.user, is_delete=False
        )
        reservation.is_delete = True
        reservation.deleted_at = timezone.now()
        reservation.save()
        return redirect("list_reservations")
