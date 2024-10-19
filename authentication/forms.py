
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'profession', 'email', 'password1', 'password2', 'address')
        labels = {
            'username': 'Nom',
            'profession': 'Profession',
            'email': 'Email',
            'password1': 'Mot de passe',
            'password2': 'Confirmation du mot de passe',
            'address': 'Adresse',
        }
        help_texts = {
            'username': None, 
            'password1': None,
            'password2': None,  
            'address': None,  
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages = {
            'required': 'complete le champs.',
        }
        self.fields['email'].error_messages = {
            'required': 'complete le champs',
        }
        self.fields['password1'].error_messages = {
            'required': 'complete le champs',
        }
        self.fields['password2'].error_messages = {
            'required': 'complete le champs',
        }
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control d-block'})
            
            
        
        
class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control d-block'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control d-block'}))

