from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from .forms import RegistrationForm, LoginForm, ProfileForm
from .models import Profil


class AccountsView(View):
    """Classe principale pour gérer les fonctionnalités de compte utilisateur"""
    
    def register(self, request):
        """Vue pour l'inscription des utilisateurs"""
        # Si l'utilisateur est déjà connecté, rediriger vers la page d'accueil
        if request.user.is_authenticated:
            return redirect('main:index')
            
        form = RegistrationForm()

        if request.method == 'POST':
            form = RegistrationForm(request.POST)

            if form.is_valid():
                try:
                    user = form.save()
                    username = form.cleaned_data.get('username')
                    raw_password = form.cleaned_data.get('password1')
                    user = authenticate(username=username, password=raw_password)
                    if user is not None:
                        login(request, user)
                        messages.success(request, f'Bienvenue {username} ! Votre compte a été créé avec succès.')
                        return redirect('main:index')
                    else:
                        messages.error(request, 'Erreur lors de la connexion après la création du compte.')
                except Exception as e:
                    # Gérer les exceptions lors de la création du compte
                    messages.error(request, f'Une erreur est survenue lors de la création du compte: {str(e)}')
            else:
                # Afficher les erreurs de validation du formulaire
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.warning(request, f'Erreur dans le champ {field}: {error}')

        return render(request, 'accounts/register.html', {'form': form})

    def login_view(self, request):
        """Vue pour la connexion des utilisateurs"""
        # Si l'utilisateur est déjà connecté, rediriger vers la page d'accueil
        if request.user.is_authenticated:
            return redirect('main:index')
            
        form = LoginForm()

        if request.method == 'POST':
            form = LoginForm(request.POST)

            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f'Bienvenue {username} ! Vous êtes maintenant connecté.')
                    
                    # Rediriger vers la page demandée si next est présent dans l'URL
                    next_page = request.GET.get('next')
                    if next_page:
                        return redirect(next_page)
                    return redirect('main:index')
                else:
                    messages.error(request, 'Nom d\'utilisateur ou mot de passe invalide.')
            else:
                messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')

        return render(request, 'accounts/login.html', {'form': form})

    def logout_view(self, request):
        """Vue pour la déconnexion des utilisateurs"""
        logout(request)
        messages.success(request, 'Vous avez été déconnecté avec succès.')
        return redirect('main:index')
    
    @method_decorator(login_required(login_url='accounts:login'))
    def profile(self, request):
        """Vue pour afficher et modifier le profil utilisateur"""
        # Récupérer ou créer le profil de l'utilisateur
        profile, created = Profil.objects.get_or_create(user=request.user)
        
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Votre profil a été mis à jour avec succès.')
                return redirect('accounts:profile')
            else:
                messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
        else:
            form = ProfileForm(instance=profile, user=request.user)
        
        return render(request, 'accounts/profile.html', {'form': form})
    
    @method_decorator(login_required(login_url='accounts:login'))
    def delete_account(self, request):
        """Vue pour supprimer le compte utilisateur"""
        if request.method == 'POST':
            # Vérifier que l'utilisateur a confirmé la suppression
            confirmation = request.POST.get('confirmation')
            if confirmation == 'SUPPRIMER':
                user = request.user
                # Déconnecter l'utilisateur avant de supprimer son compte
                logout(request)
                # Supprimer l'utilisateur (et son profil par cascade)
                user.delete()
                messages.success(request, 'Votre compte a été supprimé avec succès.')
                return redirect('main:index')
            else:
                messages.error(request, 'Veuillez saisir SUPPRIMER pour confirmer la suppression de votre compte.')
                return redirect('accounts:delete_account')
        
        return render(request, 'accounts/delete_account.html')
