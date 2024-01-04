from django.shortcuts import render, redirect
from account.models import Cart, CartItem
from django.http import JsonResponse
from account.models import Product
from django.contrib import messages


def cart(request):
 user = request.user
 user_cart = Cart.objects.get(user=user)
 cart_items = CartItem.objects.filter(cart=user_cart)

 total_cost = 0
 for cart_item in cart_items:
    total_cost += cart_item.total_cost
 
 return render(request, "cart.html", {'cart_items': cart_items, 'total_cost': total_cost, 'cart_id':user_cart.id})



def remove_from_cart(request, product_id):
    user = request.user
    user_cart = Cart.objects.get(user=user)
    cart_item = CartItem.objects.filter(product_id=product_id, cart=user_cart).first()

    if cart_item:
       cart_item.delete()

    return redirect('cart')



def update_quantity(request):
    if request.method == 'POST':
        cart_item_id = request.POST.get('cart_item_id')
        new_quantity = request.POST.get('new_quantity')

        cart_item = CartItem.objects.filter(id=cart_item_id).first()
        cart_item.quantity = new_quantity
        cart_item.save()

        return JsonResponse({'message': 'Quantity updated successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=400)
    

def add_to_cart(request, product_id):
    product = Product.objects.filter(id=product_id).first()

    if not product:
        messages.success(request, ("Sorry something went wrong..."))
        return redirect(request.META.get('HTTP_REFERER', '/'))
    
    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        cart = Cart.objects.create(user=request.user)

    cart_item = CartItem.objects.filter(cart=cart, product=product).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, ("Item already added..."))
    else:
        messages.success(request, ("Item added successful..."))
        CartItem.objects.create(cart=cart, product=product, quantity=1)

    return redirect(request.META.get('HTTP_REFERER', '/'))