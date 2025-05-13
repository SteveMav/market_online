from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class CartItem(models.Model):
    """Modèle pour les éléments du panier"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'product', 'session_id')
        verbose_name = 'Élément du panier'
        verbose_name_plural = 'Éléments du panier'
    
    def __str__(self):
        if self.user:
            return f"{self.user.username} - {self.product.name} ({self.quantity})"
        return f"Session {self.session_id[:8]} - {self.product.name} ({self.quantity})"
    
    @property
    def total_price(self):
        """Calcule le prix total pour cet élément du panier"""
        return self.product.price * self.quantity
