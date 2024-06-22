from django import forms
from django.forms import ModelForm
from .models import Product, Return


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['barcode', 'name', 'unit', 'brand', 'price', 'discount', 'stock']



