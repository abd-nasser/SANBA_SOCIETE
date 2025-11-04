from django.shortcuts import render,redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from product_app.models import Products
from django.contrib import messages
from.models import Panier, ArticlePanier, Commande


@login_required
def ajouter_au_panier(request, products_id):
    """
    AJOUTE UN PRODUIT AU PANIER
    """
    #récup le produit ou rtrn 404 si pas trouvé
    product = get_object_or_404(Products, id=products_id)
    
    #recupère le panit Actif de user ou crée un nouveau
    panier, created = Panier.objects.get_or_create(
        client= request.user,
        status="actif"
        
    )
    
    #Verifie si le produit(article) est deja dansl e panier
    article , article_created = ArticlePanier.objects.get_or_create(
        Panier_id=panier.pk,
        product_id=product.pk,
        defaults={'quantite': 1}# Valeur par defaut si création
    )
    
    if not article_created:
        #si l'article existe déjà, augmente la quantité
        article.quantite +=1
        article.save()
        messages.success(request,f'Quantité de {product.name} augmentée')
        return redirect('product_app:products-list')
    else:
        #redirige vers la page précedente ou la liste des produits
        return redirect(request,'product_app:products-list')
        
@login_required
def voir_panier(request):
    """ 
    AFFICHE LE PANIER DE L'UTLISATEUR
    """
    try:
        panier = Panier.objects.get(client=request.user, status="actif")
        articles = panier.articlepanier_set.all() #tous les articles du panier
        total = panier.total_panier()
    except Panier.DoesNotExist:
        #Si pas de panier, creation de variable vides
        panier = None
        articles = []
        total = 0
        
    ctx = {
        "panier":panier,
        "articles": articles,
        "total": total
    }
    return render(request, 'order_templates/panier.html', ctx)


        