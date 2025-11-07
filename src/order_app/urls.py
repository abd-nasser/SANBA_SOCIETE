from django.urls import path
from . import views


app_name = "order_app"

urlpatterns = [
    path("ajouts-produit/<int:products_id>/au_panier", views.ajouter_au_panier, name="ajouter-au-panier"),
    path("mes-articles/", views.voir_panier, name="voir-panier"),
    path("modifier-article/<int:article_id>/", views.modifier_panier, name="modifier-article"),
    path("supprimer-article/<int:article_id>/", views.supprimer_article, name="supprimer-article"),
    path("detail-commande/<int:commande_id>/", views.detail_commande, name="detail-commande"),
    path("valide-commande/", views.valide_commande, name="valide-commande"),
    path("historique-commande/", views.historique_commandes, name="historique-commande")
    
]
