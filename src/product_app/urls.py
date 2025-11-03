from django.urls import path
from . import views

app_name = "product_app"

urlpatterns = [
    path("produits/",views.product_list, name="products-list"),
    path("detail/<int:product_pk>/product/", views.product_detail, name="product-detail")
         ] 