from django.urls import path
from . import views
from . import webhooks

app_name = "payement_app"

urlpatterns = [
    path("choix-paiement/<int:commande_id>/", views.choix_paiement, name="choix-paiement"),
    path("paiement-ligdicash/<int:commande_id>/<str:type_paiement>", views.initier_paiement_ligdicash, name="paiement-ligdicash"),
    path('webhook/ligdicash/', webhooks.webhook_ligdicash, name='webhook_ligdicash')

]    