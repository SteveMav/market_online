from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Entreprise
from .forms import EntrepriseForm

# Create your views here

class Entreprise_view(View):
    def entreprises(self, request):
        entreprises = Entreprise.objects.all()
        return render(request, 'entreprises/entreprises.html', {'entreprises': entreprises})
    
    def my_entreprise(self, request):
        if not request.user.is_authenticated:
            messages.warning(request, 'Vous devez être connecté pour voir vos entreprises.')
            return redirect('accounts:login')
        
        my_entreprises = Entreprise.objects.filter(proprio=request.user)
        return render(request, 'entreprises/my_entreprises.html', {'my_entreprises': my_entreprises})

    def create_entreprise(self, request):
        if not request.user.is_authenticated:
            messages.warning(request, 'Vous devez être connecté pour créer une entreprise.')
            return redirect('accounts:login')
            
        form = EntrepriseForm()
        if request.method == 'POST':
            form = EntrepriseForm(request.POST, request.FILES)
            if form.is_valid():
                entreprise = form.save(commit=False)
                entreprise.proprio = request.user
                entreprise.save()
                messages.success(request, 'Votre entreprise a été créée avec succès!')
                return redirect('entreprises:my_entreprises')

        return render(request, 'entreprises/create_entreprise.html', {'form': form})
    
    def update_entreprise(self, request, entreprise_id):
        if not request.user.is_authenticated:
            messages.warning(request, 'Vous devez être connecté pour modifier une entreprise.')
            return redirect('accounts:login')
            
        entreprise = get_object_or_404(Entreprise, id=entreprise_id)
        
        # Vérifier que l'utilisateur est le propriétaire de l'entreprise
        if request.user != entreprise.proprio:
            messages.error(request, 'Vous n\'êtes pas autorisé à modifier cette entreprise.')
            return redirect('entreprises:my_entreprises')
            
        form = EntrepriseForm(instance=entreprise)
        
        if request.method == 'POST':
            form = EntrepriseForm(request.POST, request.FILES, instance=entreprise)
            if form.is_valid():
                form.save()
                messages.success(request, 'Votre entreprise a été mise à jour avec succès!')
                return redirect('entreprises:my_entreprises')
                
        return render(request, 'entreprises/update_entreprise.html', {'form': form, 'entreprise': entreprise})
    
    def delete_entreprise(self, request, entreprise_id):
        if not request.user.is_authenticated:
            messages.warning(request, 'Vous devez être connecté pour supprimer une entreprise.')
            return redirect('accounts:login')
            
        entreprise = get_object_or_404(Entreprise, id=entreprise_id)
        
        # Vérifier que l'utilisateur est le propriétaire de l'entreprise
        if request.user != entreprise.proprio:
            messages.error(request, 'Vous n\'êtes pas autorisé à supprimer cette entreprise.')
            return redirect('entreprises:my_entreprises')
            
        if request.method == 'POST':
            entreprise.delete()
            messages.success(request, 'Votre entreprise a été supprimée avec succès!')
            return redirect('entreprises:my_entreprises')
            
        return render(request, 'entreprises/delete_entreprise.html', {'entreprise': entreprise})
    
    def detail_entreprise(self, request, entreprise_id):
        entreprise = get_object_or_404(Entreprise, id=entreprise_id)
        products = entreprise.products.all()
        return render(request, 'entreprises/detail_entreprise.html', {'entreprise': entreprise, 'products': products})