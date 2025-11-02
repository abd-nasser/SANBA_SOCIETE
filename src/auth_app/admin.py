from django.contrib import admin
from .models import Client

@admin.register(Client)
class AdminClient(admin.ModelAdmin):
    list_display = ["username", "type_client","telephone","adress","total_depense","email"]


