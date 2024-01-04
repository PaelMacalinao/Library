from django.shortcuts import render, redirect
from account.models import Cart, CartItem
from account.models import Product, Order, OrderItem, PurchaseHistory
from django.contrib import messages

# Create your views here.

def buy(request, product_id):
    total_balance = Product.objects.filter(id=product_id).first().price

    if request.method == "POST":
        card = request.POST.get('card')
        if not card:
            messages.error(request, "Please enter your card.")
            return render(request, 'payment.html', {'product_id': product_id, 'total_balance': total_balance})
        
        user = request.user
        product = Product.objects.filter(id=product_id).first()
        new_order = Order.objects.create(user=user)

        OrderItem.objects.create(order=new_order, product=product)

        purchase_history = PurchaseHistory.objects.create(user=user)
        purchase_history.orders.add(new_order)
        purchase_history.total_amount = product.price
        purchase_history.save()

        return redirect('history')
    else:
        return render(request, 'payment.html', {'product_id':product_id, 'total_balance':total_balance})

def checkout(request, cart_id):
    user_cart = Cart.objects.get(id=cart_id)
    cart_items = CartItem.objects.filter(cart=user_cart)

    total_balance = 0
    for cart_item in cart_items:
        total_balance += cart_item.total_cost

    if request.method == "POST":
        card = request.POST.get('card')

        if not card:
            messages.error(request, "Please enter your card.")
            return render(request, 'payment.html', {'cart_id': cart_id, 'total_balance': total_balance})
        
        user = request.user
        new_order = Order.objects.create(user=user)

        for cart_item in cart_items:
            product = Product.objects.filter(id=cart_item.product.id).first()
            OrderItem.objects.create(order=new_order, product=product)
            cart_item.delete()

        purchase_history = PurchaseHistory.objects.create(user=user)
        purchase_history.orders.add(new_order)
        purchase_history.total_amount = total_balance
        purchase_history.save()

        return redirect('history')
    else:
        return render(request, 'payment.html', {'cart_id': cart_id, 'total_balance': total_balance})