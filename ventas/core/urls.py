from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('add_product/', views.add_product, name='add_product'),
    path('search_products/', views.search_products, name='search_products'),
    path('complete_transaction/', views.complete_transaction, name='complete_transaction'),
    path('get_transaction/<str:transaction_id>/', views.get_transaction, name='get_transaction'),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transaction/<str:transaction_id>/', views.transaction_detail, name='transaction_detail'),
    path('transaction/<str:transaction_id>/pdf/', views.download_transaction_pdf, name='transaction_pdf'),
    
]