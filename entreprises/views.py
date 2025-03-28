from django.shortcuts import render, redirect
from django.views import View
from .models import Entreprise
from .forms import EntrepriseForm

# Create your views here

class Entreprise_view(View):
    def entreprises(self, request):
        entreprises = Entreprise.objects.all()
        return render(request, 'entreprises/entreprises.html', {'entreprises': entreprises})
    
    def my_entreprise(self, request):
        my_entreprise = Entreprise.objects.filter(user = request.user)
        return render(request, 'entreprises/my_entreprises.html', {'my_entreprise': my_entreprise})

    def create_entreprise(self, request):
        form = EntrepriseForm()
        if request.method == 'POST':
            form = EntrepriseForm(request.POST)
            if form.is_valid():
                entreprise = form.save(commit=False)
                entreprise.proprio = request.user
                entreprise.save()
                return redirect('entreprises:my_entreprises')
            else:
                return render(request, 'entreprises/create_entreprise.html', {'form': form})


        
                


        return render(request, 'entreprises/create_entreprise.html', {'form': form})
        
    