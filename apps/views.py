# views.py
from django.shortcuts import render
from .models import Product, Variant

def product_and_variant_list(request):
    products = Product.objects.all()
    return render(request, 'product_and_variant_list.html', {'products': products})
