from django.db import models
from django.contrib.auth.models import User

class Entreprise(models.Model):
    name = models.CharField(max_length=255)
    proprio = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.CharField(max_length=255, null=True)
    image = models.ImageField(upload_to='images_entreprises/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
