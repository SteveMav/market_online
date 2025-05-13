from django.urls import path
from .views import ProductsView

app_name = 'products'

# Créer une instance de la classe ProductsView
products_view = ProductsView()

urlpatterns = [
    path('', products_view.product_list, name='product_list'),
    path('<int:product_id>/', products_view.product_detail, name='product_detail'),
    path('my-products/', products_view.my_products, name='my_products'),
    path('create/', products_view.create_product, name='create_product'),
    path('create/<int:entreprise_id>/', products_view.create_product, name='create_product_for_entreprise'),
    path('update/<int:product_id>/', products_view.update_product, name='update_product'),
    path('delete/<int:product_id>/', products_view.delete_product, name='delete_product'),
    path('categories/', products_view.manage_categories, name='manage_categories'),
]