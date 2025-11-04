from django.shortcuts import render, get_object_or_404
from .models import Products, Product_search_by_client, Categories
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def product_list(request):
    all_products =  Products.objects.all()
    
    #pagination - 5 produitspar page
    paginator = Paginator(all_products, 5)
    page = request.GET.get("page", 1) #page actuelle 
    
    try:
        products_by_page = paginator.page(page)
    except EmptyPage:
        products_by_page = paginator.page(paginator.num_pages)
        
    
    ctx = {"products_by_page":products_by_page}
    return render(request, "product_templates/product_list.html", ctx)


    
    
    
def product_search(request):
    query = request.GET.get("search", "").strip()
    
    if query:  # Seulement si recherche non vide
        product_find = Products.objects.filter(
            Q(name__icontains=query)|Q(description__icontains=query)
        )
        # Sauvegarder la recherche
        Product_search_by_client.objects.create(name=query)
    else:
        product_find = Products.objects.all()
    
    ctx = {"all_products": product_find, "query": query}
    return render(request, "product_templates/product_list.html", ctx)
    


def product_detail(request, product_pk):
    product = get_object_or_404(Products, pk=product_pk)
    ctx = {"product_detail":product}
    return render(request, "product_templates/product_detail.html", ctx)
    