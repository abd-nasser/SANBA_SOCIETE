from django.db import models

class Contact(models.Model):
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    
