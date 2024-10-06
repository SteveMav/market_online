from django.db import models
from django.contrib.auth.models import User

class Entreprise(models.Model):
    name = models.CharField(max_length=255)
    proprio = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='entreprise_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
