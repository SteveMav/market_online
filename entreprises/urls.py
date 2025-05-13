from django.urls import path
from .views import Entreprise_view


app_name = 'entreprises'

urlpatterns = [
    path('', Entreprise_view().entreprises, name='entreprises'),
    path('my-entreprises', Entreprise_view().my_entreprise, name='my_entreprises'),
    path('create-entreprise', Entreprise_view().create_entreprise, name='create_entreprise'),
    path('update-entreprise/<int:entreprise_id>', Entreprise_view().update_entreprise, name='update_entreprise'),
    path('delete-entreprise/<int:entreprise_id>', Entreprise_view().delete_entreprise, name='delete_entreprise'),
    path('detail-entreprise/<int:entreprise_id>', Entreprise_view().detail_entreprise, name='detail_entreprise'),
]
