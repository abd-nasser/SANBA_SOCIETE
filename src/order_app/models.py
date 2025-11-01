from django.db import models
from auth_app.models import Client
from product_app.models import Products

class Panier(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="actif")
    
    def total_panier(self):
        return sum(article.sous_total() for article in self.articlepanier_set.all())
  

class ArticlePanier(models.Model):
    Panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantite = models.IntegerField(default=1)
    
    def sous_total(self):
        return self.product.price * self.quantite
    
    
class Commande(models.Model):
    STATUT_COMMANDE = [
        ("validée", "Validée"),
        ("payee", "Payée"),
        ("livraison", "En livraison"),
        ("terminée", "terminée")
    ]
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    statut = models.CharField(max_length=20, choices=STATUT_COMMANDE, default="Validée")
    date_commande = models.DateTimeField(auto_now_add=True)
    paiements = models.OneToOneField("payement_app.Paiement",related_name="relat_paye", on_delete=models.SET_NULL, null=True, blank=True)
    