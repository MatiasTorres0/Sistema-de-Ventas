from django.db import models
import json

class Product(models.Model):
    barcode = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=50)
    brand = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    stock = models.CharField(max_length=10, default=0)
    def __str__(self):
        return f'{self.name, self.stock}'

class Transaction(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    items = models.JSONField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    client_name = models.CharField(max_length=100)
    client_dni = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, default='efectivo')

class Return(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
