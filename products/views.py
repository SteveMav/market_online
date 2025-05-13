from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from django.db.models import Q

from .models import Product, Category
from .forms import ProductForm, CategoryForm
from entreprises.models import Entreprise

class ProductsView(View):
    """Classe principale pour gérer les fonctionnalités des produits"""
    
    def product_list(self, request):
        """Vue pour afficher tous les produits"""
        # Paramètres de filtrage et de recherche
        category_id = request.GET.get('category')
        search_query = request.GET.get('q')
        sort_by = request.GET.get('sort', 'name')  # Par défaut, tri par nom
        
        # Filtrer les produits
        products = Product.objects.all()
        
        if category_id:
            products = products.filter(category_id=category_id)
        
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
        
        # Trier les produits
        if sort_by == 'price_asc':
            products = products.order_by('price')
        elif sort_by == 'price_desc':
            products = products.order_by('-price')
        elif sort_by == 'newest':
            products = products.order_by('-created_at')
        else:  # sort_by == 'name'
            products = products.order_by('name')
        
        # Récupérer toutes les catégories pour le filtre
        categories = Category.objects.all()
        
        context = {
            'products': products,
            'categories': categories,
            'current_category': category_id,
            'search_query': search_query,
            'sort_by': sort_by,
        }
        
        return render(request, 'products/product_list.html', context)
    
    def product_detail(self, request, product_id):
        """Vue pour afficher les détails d'un produit"""
        product = get_object_or_404(Product, id=product_id)
        
        # Produits similaires (même catégorie, même entreprise)
        similar_products = Product.objects.filter(
            Q(category=product.category) | Q(entreprises=product.entreprises)
        ).exclude(id=product.id)[:4]
        
        context = {
            'product': product,
            'similar_products': similar_products,
        }
        
        return render(request, 'products/product_detail.html', context)
    
    @method_decorator(login_required(login_url='accounts:login'))
    def my_products(self, request):
        """Vue pour afficher les produits de l'utilisateur"""
        # Récupérer les entreprises de l'utilisateur
        entreprises = Entreprise.objects.filter(proprio=request.user)
        
        # Récupérer tous les produits des entreprises de l'utilisateur
        products = Product.objects.filter(entreprises__in=entreprises)
        
        # Filtrer par entreprise si spécifié
        entreprise_id = request.GET.get('entreprise')
        if entreprise_id:
            products = products.filter(entreprises_id=entreprise_id)
        
        context = {
            'products': products,
            'entreprises': entreprises,
            'current_entreprise': entreprise_id,
        }
        
        return render(request, 'products/my_products.html', context)
    
    @method_decorator(login_required(login_url='accounts:login'))
    def create_product(self, request, entreprise_id=None):
        """Vue pour créer un nouveau produit"""
        # Vérifier si l'utilisateur a des entreprises
        entreprises = Entreprise.objects.filter(proprio=request.user)
        if not entreprises.exists():
            messages.warning(request, 'Vous devez d\'abord créer une entreprise avant de pouvoir ajouter des produits.')
            return redirect('entreprises:create_entreprise')
        
        # Si l'entreprise est spécifiée, vérifier qu'elle appartient à l'utilisateur
        selected_entreprise = None
        if entreprise_id:
            try:
                selected_entreprise = entreprises.get(id=entreprise_id)
            except Entreprise.DoesNotExist:
                messages.error(request, 'Vous n\'avez pas accès à cette entreprise.')
                return redirect('products:my_products')
        
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, user=request.user, entreprise_id=entreprise_id)
            if form.is_valid():
                product = form.save(commit=False)
                
                # Si l'entreprise n'est pas déjà définie dans le formulaire
                if not product.entreprises_id:
                    # Utiliser l'entreprise sélectionnée ou la première entreprise de l'utilisateur
                    product.entreprises = selected_entreprise or entreprises.first()
                
                product.save()
                messages.success(request, 'Produit créé avec succès!')
                return redirect('products:product_detail', product_id=product.id)
            else:
                messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
        else:
            form = ProductForm(user=request.user, entreprise_id=entreprise_id)
        
        context = {
            'form': form,
            'entreprises': entreprises,
            'selected_entreprise': selected_entreprise,
        }
        
        return render(request, 'products/create_product.html', context)
    
    @method_decorator(login_required(login_url='accounts:login'))
    def update_product(self, request, product_id):
        """Vue pour modifier un produit existant"""
        product = get_object_or_404(Product, id=product_id)
        
        # Vérifier que l'utilisateur est le propriétaire du produit
        if product.entreprises.proprio != request.user:
            messages.error(request, 'Vous n\'avez pas l\'autorisation de modifier ce produit.')
            return redirect('products:product_detail', product_id=product.id)
        
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product, user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Produit mis à jour avec succès!')
                return redirect('products:product_detail', product_id=product.id)
            else:
                messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
        else:
            form = ProductForm(instance=product, user=request.user)
        
        context = {
            'form': form,
            'product': product,
        }
        
        return render(request, 'products/update_product.html', context)
    
    @method_decorator(login_required(login_url='accounts:login'))
    def delete_product(self, request, product_id):
        """Vue pour supprimer un produit"""
        product = get_object_or_404(Product, id=product_id)
        
        # Vérifier que l'utilisateur est le propriétaire du produit
        if product.entreprises.proprio != request.user:
            messages.error(request, 'Vous n\'avez pas l\'autorisation de supprimer ce produit.')
            return redirect('products:product_detail', product_id=product.id)
        
        if request.method == 'POST':
            product.delete()
            messages.success(request, 'Produit supprimé avec succès!')
            return redirect('products:my_products')
        
        context = {
            'product': product,
        }
        
        return render(request, 'products/delete_product.html', context)
    
    @method_decorator(login_required(login_url='accounts:login'))
    def manage_categories(self, request):
        """Vue pour gérer les catégories (admin uniquement)"""
        # Vérifier que l'utilisateur est un administrateur
        if not request.user.is_staff:
            messages.error(request, 'Vous n\'avez pas l\'autorisation d\'accéder à cette page.')
            return redirect('main:index')
        
        categories = Category.objects.all().order_by('name')
        
        if request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Catégorie créée avec succès!')
                return redirect('products:manage_categories')
            else:
                messages.error(request, 'Veuillez corriger les erreurs dans le formulaire.')
        else:
            form = CategoryForm()
        
        context = {
            'categories': categories,
            'form': form,
        }
        
        return render(request, 'products/manage_categories.html', context)
