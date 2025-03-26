from django.urls import path
from .views import Accounts

app_name = 'accounts'

urlpatterns = [
    path('login/', Accounts().login, name='login'),
    # path('logout/', views.deconnect, name='logout'),
    path('register/', Accounts().register, name='register'),
    path('logout/', Accounts().deconnect, name='logout'),
]
