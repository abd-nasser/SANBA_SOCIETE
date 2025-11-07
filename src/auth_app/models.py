from django.db import models

from django.contrib.auth.models import AbstractUser

class Client(AbstractUser):
    TYPE_CHOICES = [
        ('particulier', 'Particulier'),
        ("entreprise", "Entreprise")
    ]
    type_client = models.CharField(max_length=100, choices=TYPE_CHOICES, default='particulier')
    telephone = models.CharField(max_length=50, blank=True)
    adress = models.TextField(blank=True)
    total_depense = models.DecimalField(max_digits=10, decimal_places=2, default=0) #pour dashboard 
    
    def __str__(self):
        return f"{self.username}-({self.type_client})"
    
