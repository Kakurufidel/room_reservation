from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.contrib.auth.views import redirect_to_login

from django.http import HttpResponseRedirect
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
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic import CreateView, ListView

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


class HomeView(TemplateView):
    template_name = "index.html"


class ReserverRoomView(View):
    def get(self, request, room_id, room_name):
        if not request.user.is_authenticated:
            messages.error(request, "Vous devez être connecté pour réserver une salle.")
            return redirect(
                "login"
            )  # Remplace 'login' par le nom de ton URL de connexion si nécessaire
        form = ReservationForm()
        return render(
            request,
            "reserver_room.html",
            {"form": form, "room_id": room_id, "room_name": room_name},
        )

    def post(self, request, room_id, room_name):
        if not request.user.is_authenticated:
            messages.error(request, "Vous devez être connecté pour réserver une salle.")
            return redirect("login")

        form = ReservationForm(request.POST)

        # Vérification si la salle est déjà réservée pour la plage horaire demandée
        if form.is_valid():
            date_start = form.cleaned_data["date_start"]
            date_end = form.cleaned_data["date_end"]

            # Vérifier les réservations existantes pour la salle
            existing_reservation = Reservation.objects.filter(
                room_id=room_id,
                date_start__lt=date_end,  # Si l'heure de début de la réservation est avant l'heure de fin choisie
                date_end__gt=date_start,  # Si l'heure de fin de la réservation est après l'heure de début choisie
            ).exists()

            if existing_reservation:
                messages.error(
                    request, "La salle est déjà réservée pour cette date et heure."
                )
                return render(
                    request,
                    "reserver_room.html",
                    {"form": form, "room_id": room_id, "room_name": room_name},
                )

            # Si aucune réservation existante, créer une nouvelle réservation
            reservation = form.save(commit=False)
            reservation.room_id = room_id
            reservation.created_by = (
                request.user
            )  # Ajoute l'utilisateur qui a fait la réservation
            reservation.save()

            messages.success(request, "Réservation effectuée avec succès!")
            return redirect("confirmation_reservation", reservation_id=reservation.id)

        return render(
            request,
            "reserver_room.html",
            {"form": form, "room_id": room_id, "room_name": room_name},
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


# cote admin


class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "admin_dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        # Vérifie si l'utilisateur est un superutilisateur (administrateur)
        if not request.user.is_superuser:
            return (
                HttpResponseForbidden()
            )  # Renvoie une erreur 403 si l'utilisateur n'est pas administrateur
        return super().dispatch(request, *args, **kwargs)


class CreateRoomView(CreateView):
    model = Room
    form_class = RoomForm
    template_name = "create_room.html"
    success_url = reverse_lazy("list_rooms")  # Redirection vers la liste des salles

    def form_valid(self, form):
        name = form.cleaned_data["name"]
        locate = form.cleaned_data["locate"]

        if Room.objects.filter(name=name, locate=locate).exists():
            messages.error(
                self.request, "Une salle avec ce nom et cet emplacement existe déjà."
            )
            return HttpResponseRedirect(self.request.path)
        # Si la salle n'existe pas déjà, enregistrer la nouvelle salle
        return super().form_valid(form)


class RoomListView(LoginRequiredMixin, ListView):
    model = Room
    template_name = "list_room_admin.html"  # Template pour afficher la liste des salles
    context_object_name = "rooms"  # Le nom de l'objet dans le template
    paginate_by = 10  # Optionnel : Nombre de salles affichées par page

    def get_queryset(self):
        # Tu peux personnaliser ici les salles à afficher
        return Room.objects.filter(deleted_at__isnull=True).order_by(
            "name"
        )  # Afficher uniquement les salles actives


class RoomUpdateView(LoginRequiredMixin, UpdateView):
    model = Room
    fields = ["name", "image_room", "capacity", "price"]
    template_name = "update_room.html"  # Template pour la modification
    success_url = reverse_lazy("list_rooms_admin")  # Redirection après succès

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.object.name
        return context

    def form_valid(self, form):
        messages.success(self.request, "La salle a été modifiée avec succès.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("list_rooms_admin")


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "user_list.html"
    context_object_name = "users"

    def get_queryset(self):
        return User.objects.filter(is_active=True).order_by("username")


class RoomDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # Récupère la salle et effectue la suppression logique
        room = get_object_or_404(Room, id=kwargs["pk"])
        room.deleted_at = now()
        room.save()
        # Retourne une réponse JSON
        return redirect("list_rooms_admin")


class ReservationListAdminView(LoginRequiredMixin, ListView):
    model = Reservation
    template_name = "list_reservations_admin.html"
    context_object_name = "reservations"

    def get_queryset(self):
        return Reservation.objects.select_related("created_by", "room").all()

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect_to_login(self.request.get_full_path())
