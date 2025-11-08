from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Paiement
from order_app.models import Commande
from django.conf import settings
import stripe



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
def initier_sripe(request, commande_id):
    """
    LANCE LE PAIEMENT STRIPE (CARTES)
    """
    #"Trouvé la commande à payé"
    commande = get_object_or_404(Commande, id=commande_id, panier__client=request.user)
    
    # convertit le prix en centimes
    montant = int(commande.panier.total_panier()*100)
    #Stripe veut 1000 pour 10,00(comme les centimes)
    
    try:
        #Dit à stripe de préparer le paiement"
        intent = stripe.PaymentIntent.create(
            amount=montant,
            currency='xof',
            metadata={
                'commande_id':commande.id,
                'client_id':request.user.id
            }
        )
         # 👆 Comme dire: "Hé Stripe, prépare-toi à recevoir un paiement!"
         
         # 🎯en meme temps on initialise les champs de model paiements dans db
        paiement = Paiement.objects.create(
            commande=commande,
            methode="stripe",
            montant=commande.panier.total_panier(),
            statu="reussi",
            stripe_payement_intent_id=intent.id,
         )
        
        # initialise le champs paiement dans le model Commande 
        commande.paiements=paiement
        commande.save()
        
        #préparer l'ecran de paiement
        ctx = {
            "commande":commande,
            "client_secret":intent.client_secret, #clé secrète pour Stripe
            #"stripe_public_key":settings.STRIPE_PUBLIC_KEY #clé publique
        }
        # 🎯 Ligne 7: "Montre l'écran où on tape la carte"
        return render(request, 'payement_templates/paiement_stripe.html', ctx)
    
    except stripe.StripeError as e:
         # 🎯 Ligne 8: "Si erreur, affiche un message"
         messages.error(request,f'Erreur Stripe:{str(e)}')
         return redirect('payement_app:choix_paiement', commande_id=commande.id)
      # 👆 Comme dire: "Le terminal ne marche pas, retourne au menu"
    
