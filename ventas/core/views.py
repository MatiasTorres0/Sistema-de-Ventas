from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Product, Transaction, Return
from .forms import ProductForm
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

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

import logging
logger = logging.getLogger(__name__)

@csrf_exempt
@transaction.atomic
def complete_transaction(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            logger.info(f"Received data: {data}")
            cart = data['cart']

            for item in cart:
                product = Product.objects.select_for_update().get(barcode=item['barcode'])
                if product.stock < item['quantity']:
                    logger.warning(f"Insufficient stock for {product.name}")
                    return JsonResponse({'error': f'Stock insuficiente para {product.name}'}, status=400)
                product.stock -= item['quantity']
                product.save()
                logger.info(f"Updated stock for {product.name}")

            transaction = Transaction.objects.create(
                items=cart,
                total=data['total'],
                client_name=data['client']['name'],
                client_dni=data['client']['dni'],
                payment_method=data['paymentMethod']
            )

            logger.info(f"Transaction created: {transaction.id}")

            return JsonResponse({'transaction_id': transaction.id, 'message': 'Transacción completada con éxito'})
        except Exception as e:
            logger.error(f"Error in complete_transaction: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
def get_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return JsonResponse(transaction.items, safe=False)

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'core/agregar_producto.html', {'form': ProductForm(), 'mensaje': "Producto guardado con éxito"})
    else:
        form = ProductForm()
    return render(request, 'core/agregar_producto.html', {'form': form})

def transaction_list(request):
    transactions = Transaction.objects.all().order_by('-created_at')
    return render(request, 'core/transacciones.html', {'transactions': transactions})

def transaction_detail(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    return render(request, 'core/transaction_detail.html', {'transaction': transaction})

def generate_transaction_pdf(transaction):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    
    p.drawString(100, 750, f"Transacción ID: {transaction.id}")
    p.drawString(100, 730, f"Cliente: {transaction.client_name}")
    p.drawString(100, 710, f"Total: ${transaction.total}")
    
    y = 690
    for item in transaction.items:
        p.drawString(100, y, f"{item['name']} - Cantidad: {item['quantity']} - Precio: ${item['price']}")
        y -= 20
    
    p.showPage()
    p.save()
    
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

def download_transaction_pdf(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    pdf = generate_transaction_pdf(transaction)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="transaction_{transaction_id}.pdf"'
    response.write(pdf)
    return response

@csrf_exempt
@transaction.atomic
def process_return(request):
    if request.method == "POST":
        data = json.loads(request.body)
        transaction_id = data['transaction_id']
        items = data['items']

        transaction = get_object_or_404(Transaction, id=transaction_id)

        for item in items:
            product = Product.objects.select_for_update().get(barcode=item['barcode'])
            product.stock += item['quantity']
            product.save()

            Return.objects.create(
                transaction=transaction,
                product=product,
                quantity=item['quantity']
            )

        # Actualizar el total de la transacción si es necesario
        # transaction.total -= total_devuelto
        # transaction.save()

        return JsonResponse({'message': 'Devolución procesada con éxito'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@csrf_exempt
@transaction.atomic
def delete_transaction(request, transaction_id):
    if request.method == "POST":
        transaction = get_object_or_404(Transaction, id=transaction_id)
        
        # Revertir el stock
        for item in transaction.items:
            product = Product.objects.select_for_update().get(barcode=item['barcode'])
            product.stock += item['quantity']
            product.save()

        # Eliminar devoluciones asociadas
        Return.objects.filter(transaction=transaction).delete()

        # Eliminar la transacción
        transaction.delete()

        return JsonResponse({'message': 'Transacción eliminada con éxito'})
    return JsonResponse({'error': 'Invalid request'}, status=400)