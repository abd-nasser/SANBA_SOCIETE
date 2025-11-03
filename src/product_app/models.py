from django.db import models
from django.contrib.auth.models import AbstractUser

class Categories(models.Model):
    name = models.CharField(max_length=50, null=True)
    icone = models.CharField(max_length=50, null=True)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    

class Products(models.Model):
    name = models.CharField(max_length=150)
    price = models.FloatField(default=0)
    image = models.ImageField(upload_to='products_images/', null=True)
    stock =  models.IntegerField(default=0)
    stock_reserve = models.IntegerField(default=0)
    categories = models.ForeignKey(Categories, null=True, on_delete=models.CASCADE)
    description = models.TextField( blank=True)
    is_on_promo = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name
   