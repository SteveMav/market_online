from .models import CartItem
import uuid

class CartMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exécuté pour chaque requête avant la vue
        self._process_cart_count(request)
        
        response = self.get_response(request)
        
        # Exécuté pour chaque requête après la vue
        return response
    
    def _process_cart_count(self, request):
        """Calcule le nombre d'articles dans le panier et le stocke dans la session"""
        if request.user.is_authenticated:
            # Utilisateur connecté - compter les articles du panier depuis la base de données
            cart_count = CartItem.objects.filter(user=request.user).count()
        else:
            # Utilisateur non connecté - utiliser la session
            session_id = request.session.get('cart_session_id')
            if not session_id:
                session_id = str(uuid.uuid4())
                request.session['cart_session_id'] = session_id
            
            cart_count = CartItem.objects.filter(session_id=session_id).count()
        
        # Stocker le nombre d'articles dans la session
        request.session['cart_count'] = cart_count
