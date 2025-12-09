from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from .models import Product, Sale, SaleItem

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            cart[str(product_id)] += quantity
        else:
            cart[str(product_id)] = quantity

        request.session['cart'] = cart
        return redirect('product_list')
    
TAX_RATE = Decimal('0.10')

def checkout(request):
    cart = request.session.get('cart', {})

    if request.method == 'POST':
        # Handle cart updates and removals
        for product_id in list(cart.keys()):
            if request.POST.get(f'remove_{product_id}'):
                del cart[product_id]
            else:
                new_qty_str = request.POST.get(f'quantity_{product_id}')
                if new_qty_str and new_qty_str.isdigit():
                    new_qty = int(new_qty_str)
                    cart[product_id] = new_qty

        request.session['cart'] = cart

        # Only process payment if it exists and cart is not empty
        payment_str = request.POST.get('payment')
        if payment_str and cart:
            try:
                payment = Decimal(payment_str)
            except:
                payment = None

            # Prepare products_in_cart
            products_in_cart = []
            subtotal = Decimal('0.00')
            for product_id, quantity in cart.items():
                product = get_object_or_404(Product, id=int(product_id))
                item_total = product.price * quantity
                subtotal += item_total
                products_in_cart.append({
                    'product': product,
                    'quantity': quantity,
                    'item_total': item_total
                })

            tax = subtotal * TAX_RATE
            total = subtotal + tax

            if payment is None or payment < total:
                error = "Payment is not enough or invalid!"
                return render(request, 'checkout.html', {
                    'products_in_cart': products_in_cart,
                    'subtotal': subtotal,
                    'tax': tax,
                    'total': total,
                    'error': error
                })

            # Complete sale
            change = payment - total
            sale = Sale.objects.create(
                subtotal=subtotal,
                tax=tax,
                total=total,
                payment=payment,
                change=change
            )

            for item in products_in_cart:
                SaleItem.objects.create(
                    sale=sale,
                    product=item['product'],
                    quantity=item['quantity'],
                    item_total=item['item_total']
                )
                item['product'].stock_quantity -= item['quantity']
                item['product'].save()

            request.session['cart'] = {}
            return redirect('receipt', sale_id=sale.id)

    # For GET requests or if no payment yet
    products_in_cart = []
    subtotal = Decimal('0.00')
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        item_total = product.price * quantity
        subtotal += item_total
        products_in_cart.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

    tax = subtotal * TAX_RATE
    total = subtotal + tax

    return render(request, 'checkout.html', {
        'products_in_cart': products_in_cart,
        'subtotal': subtotal,
        'tax': tax,
        'total': total
    })
    
def receipt(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    items = sale.saleitem_set.all()
    return render(request, 'receipt.html', {'sale': sale, 'items': items})

def add_all_to_cart(request):
    if request.method == "POST":
        cart = request.session.get('cart', {})
        
        product_ids = request.POST.getlist('product_ids')

        for pid in product_ids:
            quantity = int(request.POST.get(f'quantity_{pid}', 0))

            if quantity > 0:
                if pid in cart:
                    cart[pid] += quantity
                else:
                    cart[pid] = quantity

        request.session['cart'] = cart

        return redirect('checkout')


    return redirect('product_list')
