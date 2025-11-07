from django.contrib import admin
from .models import Paiement

@admin.register(Paiement)
class AdminPaiement(admin.ModelAdmin):
    list_display = ["commande", "methode", "montant", "statu","date_creation", "stripe_payement_intent_id", "ligdicash_transaction_id","ligdicash_phone" ]
    search_fields = ["statu"]