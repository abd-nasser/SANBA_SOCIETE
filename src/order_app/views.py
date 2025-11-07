from django.shortcuts import render,redirect ,get_object_or_404
from django.contrib.auth.decorators import login_required
from product_app.models import Products
from django.contrib import messages
from.models import Panier, ArticlePanier, Commande
from .form import AticlePanierForm
from django.db.models import Q

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
    
     # RÉACTIVE la commande Zombie si elle existe
    try:
        commande_zombie = Commande.objects.get(panier=panier, statut="Zombie")
        commande_zombie.statut = "en cours"  
        commande_zombie.save()
    except Commande.DoesNotExist:
        pass  # Pas de commande zombie, on continue
    
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
    try:
        panier = Panier.objects.get(client=request.user, status="actif")
        commande = None  # ← INITIALISE à None
        
        # Crée commande SEULEMENT si le panier a des articles
        if panier.articlepanier_set.exists():
            commande, created = Commande.objects.get_or_create(
                panier_id=panier.pk
            )
            commande.statut="en cours"
            commande.save()
            
        articles = panier.articlepanier_set.all()
        total = panier.total_panier()
        
    except Panier.DoesNotExist:
        panier = None
        articles = []
        total = 0
        commande = None  # ← IMPORTANT ici aussi
        
    ctx = {
        "commande": commande,  # ← Maintenant toujours défini (None ou objet)
        "panier": panier, 
        "articles": articles,
        "total": total
    }
    return render(request, 'order_templates/panier.html', ctx)

@login_required
def modifier_panier(request, article_id):
    panier = get_object_or_404(Panier, client=request.user, status="actif")
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
                
            
def supprimer_article(request, article_id ):
    panier = get_object_or_404(Panier, client=request.user, status="actif")  
    article = get_object_or_404(ArticlePanier, id=article_id, Panier_id=panier.pk)
    article.delete()
    commande = Commande.objects.get(panier_id=panier.pk)
    if not article.Panier.articlepanier_set.exists():
        commande.statut = "Zombie"
        commande.save()
        
    messages.success(request, f"L'article{article.product.name} été supprimé de votre panier" ) 
    return redirect("order_app:voir-panier")




def valide_commande(request):
    
    """
    TRANSFORME LE PANIER EN COMMANDE
    
    """
    #récupère panier actif du client
    panier = get_object_or_404(Panier, client=request.user, status="actif")
    
    #verifie si panier n'est pas vide
    if not panier.articlepanier_set.exists():
        messages.error(request, "votre panier est vide")
        return redirect("order_app:voir-panier")
    
    else:
        #verifie les stoks pour tous les articles
        for article in panier.articlepanier_set.all():
            if article.quantite > article.product.stock:
                messages.error(request, f"stock insuffisant pour {article.product.name}")
                return redirect("order_app:voir-panier")

        #crée la commande 
        commande = Commande.objects.create(panier_id=panier.pk)
        commande.statut="validée"
        commande.save()
                                           
        
        
        #mise à jour des stocks
        for article in panier.articlepanier_set.all():
            article.product.stock -= article.quantite
            article.product.save()
        
        #change le statu du panier
        panier.status = "validé"
        panier.save()  
        messages.success(request,"Commande validée avec succès !")
        
    return redirect('order_app:detail-commande', commande_id=commande.pk)
    
    
def detail_commande(request, commande_id):
    """
    AFFICHE LES DETAILS DE LA COMMANDE
    """
    # 1. Trouve la commande par son ID
    commande = get_object_or_404(Commande, pk=commande_id)
    
    # 2. Vérifie que cette commande appartient bien à l'utilisateur
    if commande.panier.client != request.user:
        from django.http import Http404
        raise Http404("Commande non trouvée")
    
    # 3. Passe à ton template
    ctx = {
        "commande_detail": commande,
        "panier": commande.panier  # Le panier lié à cette commande
    }
    return render(request, "order_templates/detail_commande.html", ctx)


def historique_commandes(request):
    """
    AFFICHE L'HISTORIQUE DES COMMANDES DU USER
    """
    commandes = Commande.objects.filter(panier__client=request.user).order_by("-date_commande")
    ctx = {'historique_commande':commandes}
    return render(request, "order_templates/historique-commande.html", ctx)