from django.contrib import admin
from .models import Paiement

@admin.register(Paiement)
class AdminPaiement(admin.ModelAdmin):
    list_display = ["commande", "methode", "montant","ligdicash_transaction_id","ligdicash_phone" ,"ligdicash_payment_method"]
    search_fields = ["statu"]