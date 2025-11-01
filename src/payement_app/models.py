from django.db import models
from order_app.models import Commande

class Paiement(models.Model):
    # 1. Comment on paye ?
    METHOD = [
        ("stripe", "Carte Bancaire"),
        ("ligdicash", "Mobile Money"),
    ]
    
    # 2. Est ce que ça marché ?
    STATUS = [
        ('en_attente',"Attente"),
        ("reussi", "Reussi"),
        ("echec","Echoué"),
        ("annule","Annule")
    ]
    
    # 3. A quelle commande ce paiement est il lié ?
    commande = models.ForeignKey(Commande, related_name="relat_cmd", on_delete=models.CASCADE)
    
    # 4. Avec quel moyen de paiement ?
    methode = models.CharField(max_length=20, choices=METHOD)
    
    # 5. Combien d'argent ?
    montant = models.DecimalField(max_digits=10, decimal_places=2)

    # 6. Ou en est-on ?
    statu = models.CharField(max_length=20,choices=STATUS, default="en_attente")
    
    # 7 Quand est-ce que le paiement à été crée ?
    date_creation = models.DateTimeField(auto_now_add=True)
    
    # 8. est ce avec la carte bancaire (stripe)
    stripe_payement_intent_id = models.CharField(max_length=100, blank=True)
    
    # 9. est ce avec le telephone (ligdicash)
    ligdicash_transaction_id = models.CharField(max_length=100, blank=True)
    ligdicash_phone = models.CharField(max_length=20, blank=True)