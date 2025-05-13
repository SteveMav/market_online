from django.urls import path
from .views import AccountsView

app_name = 'accounts'

# Créer une instance de la classe AccountsView
accounts_view = AccountsView()

urlpatterns = [
    path('login/', accounts_view.login_view, name='login'),
    path('register/', accounts_view.register, name='register'),
    path('logout/', accounts_view.logout_view, name='logout'),
    path('profile/', accounts_view.profile, name='profile'),
    path('delete-account/', accounts_view.delete_account, name='delete_account'),
]
