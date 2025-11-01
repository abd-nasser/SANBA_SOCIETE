from django.contrib import admin
from .models import Services, Categories, Realisation, Commentaire

@admin.register(Services)
class AdminService(admin.ModelAdmin):
    list_display = ["name", "thumbnail", "ref", "descriptions"]
    list_filter=["categories"]


@admin.register(Categories)
class AdminCategories(admin.ModelAdmin):
    list_display = ["name"]