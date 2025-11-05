from django import forms
from order_app.models import ArticlePanier

class AticlePanierForm(forms.ModelForm):
    class Meta:
        model = ArticlePanier
        fields = ["quantite"]


