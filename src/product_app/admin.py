from django.contrib import admin
from .models import Products, Categories

@admin.register(Products)
class AdminProduct(admin.ModelAdmin):
    list_display = ["name","price","stock","stock_reserve", "is_on_promo"]
    list_filter = ["categories"]
    

@admin.register(Categories)
class AdminCategories(admin.ModelAdmin):
    list_display=["order", "name", "icone"]