from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Client

class ClientForm(UserCreationForm):
    class Meta:
        model = Client
        fields = ["username", "first_name", "last_name", "email", "type_client", "telephone", "adress"]
        #     ↑↑↑↑↑              ↑↑↑↑↑↑        ↑↑↑↑↑
        #     AVEC 'S'        SANS ESPACES   CORRIGÉ 'adresse']
        
        
        