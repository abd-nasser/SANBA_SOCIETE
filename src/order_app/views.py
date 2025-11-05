from django.shortcuts import render,redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from product_app.models import Products
from django.contrib import messages
from.models import Panier, ArticlePanier, Commande
from .form import AticlePanierForm

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
        return redirect('product_app:products-list')
    
        
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

@login_required
def modifier_panier(request, article_id):
    panier = get_object_or_404(Panier, client=request.user)
    article = get_object_or_404(ArticlePanier, id=article_id, Panier_id=panier.pk)
    if request.method =="POST":
        form = AticlePanierForm(request.POST)
        if form.is_valid():
            new_quantite = form.cleaned_data.get("quantite")
            if  new_quantite > 0:
                article.quantite = new_quantite
                print("quantité changer")
                article.save() 
                messages.success(request, f"Quantité article {article.product.name} modifiée!")
                return redirect("order_app:voir-panier") 
            else:
                # suppression d'article if quantité inf = 0
                article.delete()
                message = messages.success(request, f"Article {article.product.name} supprimé du panier")
                return redirect("order_app:voir-panier") 
    return render(request, "order_templates/partials/modifier_article.html", {"form":AticlePanierForm(),
                                                                              'article':article}
                  )           
                
            
        
        
            