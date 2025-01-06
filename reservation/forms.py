from django import forms
from .models import Reservation, Room


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["date_start", "date_end"]  # Les champs visibles
        widgets = {
            "date_start": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "date_end": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name", "locate", "capacity", "image_room", "price"]

    widgets = {
        "name": forms.TextInput(
            attrs={"class": "form-control d-block", "placeholder": "Nom de la salle"}
        ),
        "locate": forms.TextInput(
            attrs={
                "class": "form-control d-block",
                "placeholder": "Emplacement de la salle",
            }
        ),
        "capacity": forms.NumberInput(
            attrs={
                "class": "form-control d-block",
                "placeholder": "Capacité de la salle",
            }
        ),
        "price": forms.TextInput(
            attrs={"class": "form-control d-block", "placeholder": "Prix de la salle"}
        ),  # Personnalisation pour le champ `price`
        "image_room": forms.ClearableFileInput(
            attrs={"class": "form-control d-block"}
        ),  # Image de la salle avec un widget personnalisé
    }
