from django import forms
from .models import Reservation, Room


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["room", "date_start", "date_end"]
        widgets = {
            "room": forms.Select(attrs={"class": "form-control"}),
            "date_start": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "date_end": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
        }


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name", "locate", "capacity", "image_room"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control d-block"}),
            "locate": forms.TextInput(attrs={"class": "form-control d-block"}),
            "capacity": forms.NumberInput(attrs={"class": "form-control d-block"}),
        }
