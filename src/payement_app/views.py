from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Commande

@login_required #views accecibles seulement quand user est connecté
def choix_paiement(request, commande_id):
    """
    PAGE DE CHOIX ENTRE STRIPE ET LIGDICASH
    """
    #recupère la commande du user
    commande = get_object_or_404(Commande, id=commande_id, panier__client=request.user )
    #comme dire: donne moi la commande N*x du panier qui apartient à user connecté
    
    #verifie qu'on peut faire le payement 
    if commande.statut != "validée":
        messages.error(request, "cette commande ne peut plus être payée")
        return redirect("order_app:detail-commande", commande_id=commande.id)
    #si la commande est déja payé, zombie, ne peut plus etre repayé
    
    ctx = {
        "commande": commande,
        "total":commande.panier.total_panier()
    }
    
    return render(request, 'payement_templates/choix_paiement.html', ctx)
    
    
@login_required