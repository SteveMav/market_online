from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from django.http import JsonResponse
import uuid

from products.models import Product
from .models import CartItem

class CartView(View):
    """Classe principale pour gérer les fonctionnalités du panier"""
    
    def get_cart_items(self, request):
        """Récupère les éléments du panier pour l'utilisateur ou la session"""
        if request.user.is_authenticated:
            # Utilisateur connecté - récupérer les éléments du panier depuis la base de données
            cart_items = CartItem.objects.filter(user=request.user)
            
            # Si l'utilisateur a des éléments dans sa session, les migrer vers son compte
            session_id = request.session.get('cart_session_id')
            if session_id:
                session_items = CartItem.objects.filter(session_id=session_id, user__isnull=True)
                for item in session_items:
                    # Vérifier si l'utilisateur a déjà ce produit dans son panier
                    existing_item = CartItem.objects.filter(user=request.user, product=item.product).first()
                    if existing_item:
                        # Mettre à jour la quantité
                        existing_item.quantity += item.quantity
                        existing_item.save()
                        item.delete()
                    else:
                        # Transférer l'élément au compte de l'utilisateur
                        item.user = request.user
                        item.session_id = None
                        item.save()
                
                # Supprimer l'ID de session du panier
                del request.session['cart_session_id']
        else:
            # Utilisateur non connecté - utiliser la session
            session_id = request.session.get('cart_session_id')
            if not session_id:
                session_id = str(uuid.uuid4())
                request.session['cart_session_id'] = session_id
            
            cart_items = CartItem.objects.filter(session_id=session_id)
        
        return cart_items
    
    def cart_summary(self, request):
        """Vue pour afficher le contenu du panier"""
        cart_items = self.get_cart_items(request)
        
        # Calculer le total du panier
        cart_total = sum(item.total_price for item in cart_items)
        
        context = {
            'cart_items': cart_items,
            'cart_total': cart_total,
            'cart_count': cart_items.count(),
        }
        
        return render(request, 'cart/cart_summary.html', context)
    
    def add_to_cart(self, request, product_id):
        """Vue pour ajouter un produit au panier"""
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if request.user.is_authenticated:
            # Utilisateur connecté - ajouter au panier en base de données
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                # Le produit existe déjà dans le panier, mettre à jour la quantité
                cart_item.quantity += quantity
                cart_item.save()
        else:
            # Utilisateur non connecté - utiliser la session
            session_id = request.session.get('cart_session_id')
            if not session_id:
                session_id = str(uuid.uuid4())
                request.session['cart_session_id'] = session_id
            
            cart_item, created = CartItem.objects.get_or_create(
                session_id=session_id,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                # Le produit existe déjà dans le panier, mettre à jour la quantité
                cart_item.quantity += quantity
                cart_item.save()
        
        messages.success(request, f'{product.name} a été ajouté à votre panier.')
        
        # Vérifier si la requête est AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            cart_items = self.get_cart_items(request)
            cart_count = cart_items.count()
            return JsonResponse({
                'success': True,
                'message': f'{product.name} a été ajouté à votre panier.',
                'cart_count': cart_count
            })
        
        # Rediriger vers la page précédente ou la page du produit
        next_url = request.POST.get('next') or request.GET.get('next')
        if next_url:
            return redirect(next_url)
        return redirect('products:product_detail', product_id=product_id)
    
    def update_cart(self, request, item_id):
        """Vue pour mettre à jour la quantité d'un produit dans le panier"""
        cart_item = get_object_or_404(CartItem, id=item_id)
        
        # Vérifier que l'utilisateur est autorisé à modifier cet élément
        if request.user.is_authenticated:
            if cart_item.user != request.user:
                messages.error(request, 'Vous n\'êtes pas autorisé à modifier cet élément.')
                return redirect('cart:cart_summary')
        else:
            session_id = request.session.get('cart_session_id')
            if cart_item.session_id != session_id:
                messages.error(request, 'Vous n\'êtes pas autorisé à modifier cet élément.')
                return redirect('cart:cart_summary')
        
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Panier mis à jour avec succès.')
        else:
            cart_item.delete()
            messages.success(request, 'Produit retiré du panier.')
        
        # Vérifier si la requête est AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            cart_items = self.get_cart_items(request)
            cart_total = sum(item.total_price for item in cart_items)
            return JsonResponse({
                'success': True,
                'cart_total': cart_total,
                'item_total': cart_item.total_price if quantity > 0 else 0,
                'cart_count': cart_items.count()
            })
        
        return redirect('cart:cart_summary')
    
    def remove_from_cart(self, request, item_id):
        """Vue pour supprimer un produit du panier"""
        cart_item = get_object_or_404(CartItem, id=item_id)
        
        # Vérifier que l'utilisateur est autorisé à supprimer cet élément
        if request.user.is_authenticated:
            if cart_item.user != request.user:
                messages.error(request, 'Vous n\'êtes pas autorisé à supprimer cet élément.')
                return redirect('cart:cart_summary')
        else:
            session_id = request.session.get('cart_session_id')
            if cart_item.session_id != session_id:
                messages.error(request, 'Vous n\'êtes pas autorisé à supprimer cet élément.')
                return redirect('cart:cart_summary')
        
        product_name = cart_item.product.name
        cart_item.delete()
        
        messages.success(request, f'{product_name} a été retiré de votre panier.')
        
        # Vérifier si la requête est AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            cart_items = self.get_cart_items(request)
            cart_total = sum(item.total_price for item in cart_items)
            return JsonResponse({
                'success': True,
                'message': f'{product_name} a été retiré de votre panier.',
                'cart_total': cart_total,
                'cart_count': cart_items.count()
            })
        
        return redirect('cart:cart_summary')
    
    def clear_cart(self, request):
        """Vue pour vider le panier"""
        if request.user.is_authenticated:
            CartItem.objects.filter(user=request.user).delete()
        else:
            session_id = request.session.get('cart_session_id')
            if session_id:
                CartItem.objects.filter(session_id=session_id).delete()
        
        messages.success(request, 'Votre panier a été vidé.')
        
        # Vérifier si la requête est AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Votre panier a été vidé.',
                'cart_total': 0,
                'cart_count': 0
            })
        
        return redirect('cart:cart_summary')
