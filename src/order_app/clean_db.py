from django.core.management.base import BaseCommand
from order_app.models import Panier, Commande, ArticlePanier

class Commande(BaseCommand):
    help = 'Nettoie complètement la base arder_app'
    
    def handle(self, *args, **options):
        ArticlePanier.objects.all().delete()
        Commande.objects.all().delete()
        Panier.objects.all().delete()
        
        self.stdout.write(
            self.style.SUCCESS("✅ Base order_app nettoyée !")
        )
        
       # Utilisation :

#bash
#python manage.py clean_db