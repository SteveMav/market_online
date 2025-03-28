from django.urls import path
from .views import Entreprise, Entreprise_view


app_name = 'entreprises'

urlpatterns = [
    path('', Entreprise_view().entreprises, name='entreprises'),
    path('my-entreprises', Entreprise_view().entreprises, name='my_entreprises'),
    path('create-entreprise', Entreprise_view().create_entreprise, name='create_entreprise'),
]
