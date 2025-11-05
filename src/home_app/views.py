from django.shortcuts import render, get_object_or_404
from product_app.models import Products
from order_app.models import ArticlePanier, Panier



def home_view(request):
    panier = Panier.objects.get(client=request.user, status="actif")
    articles_in_panier = panier.articlepanier_set.all()
    ctx = {"num_articlepanier":len(articles_in_panier)}
    return render(request, "home_templates/home.html",ctx)

    



def product_list(request):
    all_products =  Products.objects.all()[:5]
    ctx = {"all_products":all_products}
    return render(request, "home_templates/partials/part_products_list.html", ctx)