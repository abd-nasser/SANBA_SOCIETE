#python manage.py shell

from order_app.models import Panier, Commande, ArticlePanier

print("=== AVANT NETTOYAGE ===")
print(f"Paniers: {Panier.objects.count()}")
print(f"Commandes: {Commande.objects.count()}") 
print(f"Articles panier: {ArticlePanier.objects.count()}")

# Voir les IDs problématiques
print("IDs commandes:", list(Commande.objects.values_list('id', flat=True)))
print("IDs paniers:", list(Panier.objects.values_list('id', flat=True)))


#2. Reset complet :
# SUPPRIMER TOUT dans le bon ordre
ArticlePanier.objects.all().delete()
Commande.objects.all().delete() 
Panier.objects.all().delete()

print("=== APRÈS NETTOYAGE ===")
print(f"Paniers: {Panier.objects.count()}")
print(f"Commandes: {Commande.objects.count()}")
print(f"Articles panier: {ArticlePanier.objects.count()}")

#3. Reset les séquences SQLite (pour les IDs) :
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='order_app_panier'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='order_app_commande'") 
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='order_app_articlepanier'")

print("Séquences SQLite réinitialisées !")