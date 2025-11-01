from django.db import models
from django.contrib.auth.models import AbstractUser



class Products(models.Model):
    name = models.CharField(max_length=150)
    price = models.FloatField(default=0)
    stock =  models.IntegerField(default=0)
    stock_reserve = models.IntegerField(default=0)
    description = models.TextField( blank=True)
    is_on_promo = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
   