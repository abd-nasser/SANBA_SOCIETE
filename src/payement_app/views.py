from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Paiement
from order_app.models import Commande
from django.conf import settings

import requests
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
def initier_paiement_ligdicash(request, commande_id, type_paiement):
    """PAIEMENT LIGDICASH UNIFIE (CARTE + MOBILE)
    """
    commande = get_object_or_404(Commande, id=commande_id, panier__client=request.user)
    
    if request.method =='POST':
        #configuration selon le type
        if type_paiement=="mobile":
            phone = request.POST.get('phone') #recupère phone du client
            
            #prépare les donnée du client pour post à API ligdicash
            payload = {
                "amount":str(commande.panier.total_panier()),
                "currency":"XOF",
                "order_id":str(commande.id),
                "phone_number":phone,
                "payement_method":'mobile_money',
                'callback_url':f'{settings.BASE_URL}/payement/ligdicash/webhook/',
                
            }
        else:
            payload = {
                "amount":str(commande.panier.total_panier()),
                "currency":"XOF",
                "order_id":str(commande.id),
                "payement_method":'card',
                "callback_url":f'{settings.BASE_URL}/payement/ligdicash/webhook/',
                  
            }
            
            headers = {
                "Authorization":f"Bearer {settings.LIGDICASH_API_KEY}",
                'Accept': 'application/json',
                "Content-Type":'application/json'
            }
            
            try:
                api = ""
                response = requests.post(url=api,
                                         json=payload,
                                         headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    #on initialise le model paiement avec l'etat de la response
                    paiement = Paiement.objects.create(
                        commande=commande,
                        methode ="ligdicash",
                        statu = "reussi",
                        montant=commande.panier.total_panier(),
                        ligdicash_transaction_id= data.get('transaction_id'),
                        ligdicash_phone=phone if type_paiement=="mobile" else'',
                        ligdicash_payment_method = "mobile_money" if type_paiement=="mobile" else "card"
                    )
                    
                    #lier paiement à la commande
                    commande.paiements = paiement
                    commande.save()
                    
                    messages.success(request, f"Paiement {type_paiement} initié !")
                    return redirect('order_app:detail-commande', commande_id=commande.id)
            except requests.RequestException as e:
                messages.error(request,f"Erreur: {str(e)}" )
        
        ctx = {
            'commande': commande,
            'type_paiement': type_paiement
            }
    return render(request, f'payment_templates/paiement_ligdicash_{type_paiement}.html', ctx)