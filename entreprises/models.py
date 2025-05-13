from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Entreprise(models.Model):
    name = models.CharField(max_length=255)
    proprio = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to='images_entreprises/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

# Signal pour mettre à jour le statut de vendeur de l'utilisateur
@receiver(post_save, sender=Entreprise)
def update_seller_status(sender, instance, created, **kwargs):
    """Met à jour le statut de vendeur de l'utilisateur lorsqu'il crée une entreprise"""
    if created:  # Seulement lors de la création, pas lors de la mise à jour
        user = instance.proprio
        if hasattr(user, 'profil') and not user.profil.is_seller:
            user.profil.is_seller = True
            user.profil.save()
