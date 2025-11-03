from django.shortcuts import render
from product_app.models import Products



def home_view(request):
    return render (request,"home_templates/home.html")


def product_list(request):
    all_products =  Products.objects.all()[:5]
    ctx = {"all_products":all_products}
    return render(request, "home_templates/partials/part_products_list.html", ctx)