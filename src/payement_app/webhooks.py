
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Paiement
from order_app.models import Commande
import json
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def webhook_ligdicash(request):
    """
    WEBHOOK UNIQUE POUR CARTE ET MOBILE MONEY
    """
    if request.method =="POST":
        try:
            data =json.loads(request.body) 
            transaction_id = data.get("transaction_id")
            status = data.get("status")
            payement_method = data.get("payement_method", "unknown")
            
            #trouver paiement
            paiement = Paiement.objects.get(ligdicash_transaction_id=transaction_id)
            
            if status == 'SUCCESSFUL':
                paiement.statu= "reussi"
                paiement.save()
                
                commande = paiement.commande
                commande.statut="payée"
                commande.save()

                # 📧 Envoyer email de confirmation
                #envoyer_email_confirmation(commande)
                
                # 📊 Log pour analytics
                logger.info(f"Paiement {payement_method} réussi:{transaction_id}")
                
            elif status in ["FAILED", "CANCELLED" ]:
                # ❌ Paiement échoué
                 paiement.statu = 'echec'
                 paiement.save()
                 logger.warning(f"Paiement {payement_method} réussi:{transaction_id}")
            return JsonResponse({'status': 'webhook_processed'})
        
        except Paiement.DoesNotExist:
            logger.error(f"Paiement non trouvé: {transaction_id}")
            return JsonResponse({'error':'paiement_not_found'}, status=404)
        except Exception as e:
            logger.error(f'Erreur webhook:{str(e)}')
            return JsonResponse({'error':'server_error'},status=500)
        
                
                
            
          