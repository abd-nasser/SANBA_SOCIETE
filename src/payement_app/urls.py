from django.urls import path
from . import views

app_name = "payement_app"

urlpatterns = [
    path("choix-paiement/<int:commande_id>/", views.choix_paiement, name="choix-paiement"),
    path("paiement-par-carte-bancaire/<int:commande_id>", views.initier_sripe, name="paiement-stripe")
]
