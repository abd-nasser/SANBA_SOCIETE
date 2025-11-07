from django.contrib import admin
from .models import Commande, Panier, ArticlePanier

@admin.register(Panier)
class AdminPanier(admin.ModelAdmin):
    list_display = ["client", "status", 'total_panier']


@admin.register(ArticlePanier)
class AdminArticlePanier(admin.ModelAdmin):
    list_display = ["Panier", "product", "quantite", "sous_total"]
    
@admin.register(Commande)
class AdminCommand(admin.ModelAdmin):
    list_display=["panier", "statut", "date_commande", "paiements"]
    
    
        


