from django.urls import path
from .views import CartView

app_name = 'cart'

# Créer une instance de la classe CartView
cart_view = CartView()

urlpatterns = [
    path('', cart_view.cart_summary, name='cart_summary'),
    path('add/<int:product_id>/', cart_view.add_to_cart, name='add_to_cart'),
    path('update/<int:item_id>/', cart_view.update_cart, name='update_cart'),
    path('remove/<int:item_id>/', cart_view.remove_from_cart, name='remove_from_cart'),
    path('clear/', cart_view.clear_cart, name='clear_cart'),
]
