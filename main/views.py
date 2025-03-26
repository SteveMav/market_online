from django.shortcuts import render
from django.views import View
from products.models import Product

class Home(View):

    def index(self, request):
        products = Product.objects.all()
        return render(request, 'main/index.html', {'products': products})
