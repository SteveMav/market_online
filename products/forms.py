from django import forms
from .models import Product, Category
from entreprises.models import Entreprise

class ProductForm(forms.ModelForm):
    """Formulaire pour la création et la modification de produits"""
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom du produit'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description du produit'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Prix', 'min': '0', 'step': '0.01'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nom du produit',
            'description': 'Description',
            'price': 'Prix',
            'image': 'Image du produit',
            'category': 'Catégorie',
        }
    
    def __init__(self, *args, user=None, entreprise_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrer les catégories disponibles
        self.fields['category'].queryset = Category.objects.all()
        
        # Si l'entreprise est spécifiée, la définir comme valeur par défaut
        if entreprise_id and not self.instance.pk:
            try:
                entreprise = Entreprise.objects.get(id=entreprise_id, proprio=user)
                self.instance.entreprises = entreprise
            except Entreprise.DoesNotExist:
                pass

class CategoryForm(forms.ModelForm):
    """Formulaire pour la création et la modification de catégories"""
    
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la catégorie'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Description de la catégorie'}),
        }
        labels = {
            'name': 'Nom de la catégorie',
            'description': 'Description',
        }
