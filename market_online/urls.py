from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls import handler404, handler500
from django.conf import settings

# handler404 = 'main.views.custom_404'
# handler500 = 'main.views.custom_500'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',  include('main.urls')),
    path('accounts/', include('accounts.urls')),
    path('entreprises/', include('entreprises.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    # path('orders/', include('orders.urls')),
    # path('reviews/', include('reviews.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
