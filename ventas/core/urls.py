from django.urls import path
from .views import index, add_product, complete_transaction, get_transaction, agregar_producto, search_products

urlpatterns = [
    path('', index, name='home'),
    path('add_product/', add_product, name='add_product'),
    path('complete_transaction/', complete_transaction, name='complete_transaction'),
    path('get_transaction/<str:transaction_id>/', get_transaction, name='get_transaction'),
    path('agregar_producto/', agregar_producto, name="agregar_producto"),
    path('search_products/', search_products, name='search_products'),
]
