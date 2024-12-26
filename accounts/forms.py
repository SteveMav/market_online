from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile



class loginForm(forms.Form):
    username = forms.CharField(
        max_length=15, 
        required=True, 
        label='Nom d\'utilisateur', 
        widget=forms.TextInput(attrs={'class': 'form-control my-3', 'id': 'usernameInput'}), 
        help_text=''
    )
    password = forms.CharField(
        max_length=15, 
        required=True, 
        label='Mot de passe', 
        widget=forms.PasswordInput(attrs={'class': 'form-control my-3', 'id': 'passwordInput'}), 
        help_text=''
    )
    
    # Custom initialization of the login form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update({'class': 'form-control my-3', 'id': 'passwordInput'})
        self.fields['password'].help_text = ''
        self.fields['password'].label = 'Mot de passe'

