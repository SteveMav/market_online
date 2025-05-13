from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profil


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150, 
        required=True, 
        label='Nom d\'utilisateur', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre nom d\'utilisateur'}), 
        help_text=''
    )
    password = forms.CharField(
        max_length=128, 
        required=True, 
        label='Mot de passe', 
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre mot de passe'}), 
        help_text=''
    )


# Custom registration form that extends UserCreationForm
class RegistrationForm(UserCreationForm):
    # Define choices for city field
    CITY_CHOICES = [
        ('', 'Sélectionnez une ville'),
        ('Kinshasa', 'Kinshasa'),
        ('Kisangani', 'Kisangani'),
        ('Lubumbashi', 'Lubumbashi'),
        ('Goma', 'Goma'),
        ('Bukavu', 'Bukavu'),
        ('Matadi', 'Matadi'),
        ('Kananga', 'Kananga'),
        ('Mbuji-Mayi', 'Mbuji-Mayi'),
    ]
    
    # Add custom fields for phone number and city
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre email'})
    )
    phone_number = forms.CharField(
        max_length=15, 
        required=False, 
        label='Numéro de téléphone', 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 0812345678'}), 
        help_text=''
    )
    commune = forms.ChoiceField(
        choices=CITY_CHOICES,
        required=False, 
        label='Ville', 
        widget=forms.Select(attrs={'class': 'form-control'}), 
        help_text=''
    )

    # Meta class to specify model and form fields
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'commune', 'password1', 'password2']
        labels = {
            'username': 'Nom d\'utilisateur',
            'email': 'Email',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choisissez un nom d\'utilisateur'}),
        }
        help_texts = {
            'username': '',
        }

    # Custom initialization of the form
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Choisissez un mot de passe'})
        self.fields['password1'].help_text = 'Le mot de passe doit contenir au moins 8 caractères.'
        self.fields['password1'].label = 'Mot de passe'
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmez votre mot de passe'})
        self.fields['password2'].help_text = ''
        self.fields['password2'].label = 'Confirmation du mot de passe'

    # Custom save method to handle profile creation
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Convert phone_number to integer if not empty
            phone_number = None
            if self.cleaned_data['phone_number']:
                try:
                    phone_number = int(self.cleaned_data['phone_number'])
                except ValueError:
                    pass
                
            # Update the profile that was created by the signal
            try:
                profile = user.profil
                profile.phone_number = phone_number
                profile.city = self.cleaned_data['commune']
                profile.save()
            except Profil.DoesNotExist:
                # Fallback in case the signal didn't create the profile
                profile = Profil(
                    user=user,
                    phone_number=phone_number,
                    city=self.cleaned_data['commune']
                )
                profile.save()
        return user


class ProfileForm(forms.ModelForm):
    # Define choices for gender and city fields
    GENDER_CHOICES = [
        ('', 'Sélectionnez votre genre'),
        ('M', 'Masculin'),
        ('F', 'Féminin'),
        ('O', 'Autre'),
    ]
    
    CITY_CHOICES = [
        ('', 'Sélectionnez une ville'),
        ('Kinshasa', 'Kinshasa'),
        ('Kisangani', 'Kisangani'),
        ('Lubumbashi', 'Lubumbashi'),
        ('Goma', 'Goma'),
        ('Bukavu', 'Bukavu'),
        ('Matadi', 'Matadi'),
        ('Kananga', 'Kananga'),
        ('Mbuji-Mayi', 'Mbuji-Mayi'),
    ]
    
    # User model fields
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Nom d\'utilisateur',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    # Profile model fields with improved widgets
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        label='Numéro de téléphone',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 0812345678'})
    )
    city = forms.ChoiceField(
        choices=CITY_CHOICES,
        required=False,
        label='Ville',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    commune = forms.CharField(
        max_length=255,
        required=False,
        label='Commune',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre commune'})
    )
    address = forms.CharField(
        max_length=255,
        required=False,
        label='Adresse',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Votre adresse complète'})
    )
    date_of_birth = forms.DateField(
        required=False,
        label='Date de naissance',
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        input_formats=['%Y-%m-%d']
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        required=False,
        label='Genre',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    bio = forms.CharField(
        required=False,
        label='Biographie',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Parlez-nous de vous'})
    )
    interests = forms.CharField(
        required=False,
        label='Centres d\'intérêt',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Vos centres d\'intérêt, séparés par des virgules'})
    )
    profile_picture = forms.ImageField(
        required=False,
        label='Photo de profil',
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    is_seller = forms.BooleanField(
        required=False,
        label='Je souhaite devenir vendeur',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = Profil
        fields = ['phone_number', 'city', 'commune', 'address', 'date_of_birth', 
                 'gender', 'bio', 'interests', 'profile_picture', 'is_seller']
    
    def __init__(self, *args, **kwargs):
        # Get the user instance if provided
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # If user is provided, set initial values for user fields
        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email
            
            # Convert phone_number from integer to string if it exists
            if self.instance and self.instance.phone_number:
                self.fields['phone_number'].initial = str(self.instance.phone_number)
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        
        # Update user fields if user is provided
        if self.user:
            self.user.username = self.cleaned_data['username']
            self.user.email = self.cleaned_data['email']
            if commit:
                self.user.save()
        
        # Convert phone_number to integer if not empty
        if self.cleaned_data['phone_number']:
            try:
                profile.phone_number = int(self.cleaned_data['phone_number'])
            except ValueError:
                profile.phone_number = None
        else:
            profile.phone_number = None
            
        if commit:
            profile.save()
            
        return profile
