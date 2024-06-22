from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product, Transaction, Return
import json
from datetime import datetime
from .forms import ProductForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Transaction
import json

def index(request):
    products = Product.objects.all()
    return render(request, 'core/home.html', {'products': products})

def add_product(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product = get_object_or_404(Product, barcode=data['barcode'])
        return JsonResponse({
            'name': product.name,
            'unit': product.unit,
            'brand': product.brand,
            'price': float(product.price),
            'discount': float(product.discount)
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

def search_products(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query) | Product.objects.filter(barcode__icontains=query)
    product_list = [
        {
            'barcode': p.barcode,
            'name': p.name,
            'price': float(p.price),
            'stock': p.stock,
            'discount': float(p.discount)
        } for p in products
    ]
    return JsonResponse(product_list, safe=False)

@csrf_exempt
def complete_transaction(request):
    if request.method == "POST":
        data = json.loads(request.body)
        transaction = Transaction.objects.create(
            items=data['cart'],
            total=data['total'],
            client_name=data['client']['name'],
            client_dni=data['client']['dni']
        )
        return JsonResponse({'transaction_id': transaction.id})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return JsonResponse(transaction.items, safe=False)


def agregar_producto(request):
    data = {
        'form': ProductForm()

    }
    if request.method == 'POST':
        formulario = ProductForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            data['mensaje'] = "Producto guardado con exito"
    return render(request, 'core/agregar_producto.html', data)