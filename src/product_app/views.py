from django.shortcuts import render, get_object_or_404
from .models import Products

def product_list(request):
    all_products =  Products.objects.all()
    ctx = {"all_products":all_products}
    return render(request, "home_templates/partials/products_list.html", ctx)
    

def product_detail(request, product_pk):
    product = get_object_or_404(Products, pk=product_pk)
    ctx = {"product":product}
    return render(request, "product_templates/product_detail.html", ctx)
    