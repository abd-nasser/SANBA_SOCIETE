from django.urls import path
from . import views


app_name = "order_app"
urlpatterns = [
    path("ajouts_produit/<int:products_id>/au_panier", views.ajouter_au_panier, name="ajouter-au-panier"),
    path("mes_articles/", views.voir_panier, name="voir-panier")
    
]
