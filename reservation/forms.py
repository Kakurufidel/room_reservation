from django import forms
from .models import (Reservation, Room)

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['room', 'date_start', 'date_end']
        widgets = {
            'room': forms.Select(attrs={'class': 'form-control'}),
            'date_start': forms.DateInput(attrs={'class': 'form-control',"type":"date"}),
            'date_end': forms.DateInput(attrs={'class': 'form-control',"type":"date"}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model =Room
        fields = ['name', 'locate', 'capacity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control d-block'}),
            'locate': forms.TextInput(attrs={'class': 'form-control d-block'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control d-block'}),
        }
