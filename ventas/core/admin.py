from django.contrib import admin
from .models import Product, Return, Transaction
# Register your models here.

admin.site.register(Transaction)
admin.site.register(Product)
admin.site.register(Return)