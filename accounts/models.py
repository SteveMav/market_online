from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _



class Profil(models.Model):
    """Modèle pour le profil utilisateur étendu"""
    
    # Choix pour le champ gender
    GENDER_CHOICES = (
        ('M', _('Masculin')),
        ('F', _('Féminin')),
        ('O', _('Autre')),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    phone_number = models.BigIntegerField(blank=True, null=True, verbose_name=_('Numéro de téléphone'))
    profile_picture = models.ImageField(
        upload_to='profile_pictures/%Y/%m/', 
        null=True, 
        blank=True, 
        verbose_name=_('Photo de profil')
    )
    bio = models.TextField(
        null=True, 
        blank=True, 
        verbose_name=_('Biographie'),
        help_text=_('Une brève description de vous-même')
    )
    is_seller = models.BooleanField(
        default=False, 
        verbose_name=_('Vendeur'),
        help_text=_('Indique si l\'utilisateur peut vendre des produits')
    )
    
    def update_seller_status(self):
        """Met à jour le statut de vendeur en fonction des entreprises possédées"""
        from entreprises.models import Entreprise
        # Vérifier si l'utilisateur possède au moins une entreprise
        has_entreprise = Entreprise.objects.filter(proprio=self.user).exists()
        
        # Mettre à jour le statut de vendeur si nécessaire
        if has_entreprise and not self.is_seller:
            self.is_seller = True
            self.save(update_fields=['is_seller'])
        
        return self.is_seller
    
    @classmethod
    def is_user_seller(cls, user):
        """Vérifie si un utilisateur est vendeur"""
        if hasattr(user, 'profil'):
            return user.profil.is_seller
        return False
    city = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name=_('Ville')
    )
    commune = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        verbose_name=_('Commune')
    )
    address = models.CharField(
        max_length=255, 
        blank=True, 
        null=True, 
        verbose_name=_('Adresse')
    )
    date_of_birth = models.DateField(
        blank=True, 
        null=True, 
        verbose_name=_('Date de naissance')
    )
    gender = models.CharField(
        max_length=1, 
        choices=GENDER_CHOICES, 
        blank=True, 
        null=True, 
        verbose_name=_('Genre')
    )
    interests = models.TextField(
        blank=True, 
        null=True, 
        verbose_name=_('Centres d\'intérêt'),
        help_text=_('Vos centres d\'intérêt, séparés par des virgules')
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date de création'), null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Dernière mise à jour'), null=True)

    class Meta:
        verbose_name = _('Profil')
        verbose_name_plural = _('Profils')
        ordering = ['-created_at']

    def __str__(self):
        return f'Profil de {self.user.username}'
    
    def get_full_address(self):
        """Retourne l'adresse complète de l'utilisateur"""
        address_parts = []
        if self.address:
            address_parts.append(self.address)
        if self.commune:
            address_parts.append(self.commune)
        if self.city:
            address_parts.append(self.city)
        
        return ', '.join(address_parts) if address_parts else _('Adresse non renseignée')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crée automatiquement un profil pour chaque nouvel utilisateur"""
    if created:
        profile = Profil.objects.create(user=instance)
        # Vérifier si l'utilisateur possède déjà des entreprises
        profile.update_seller_status()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Sauvegarde le profil lors de la sauvegarde de l'utilisateur"""
    try:
        instance.profil.save()
    except Profil.DoesNotExist:
        Profil.objects.create(user=instance)
