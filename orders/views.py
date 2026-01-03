from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart,CartItem,Order,OrderItem
from store.models import Pizaa
from django.contrib.auth.decorators import login_required
import razorpay
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def get_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return cart

@login_required
def add_to_cart(request, pizza_id):
    pizza = get_object_or_404(Pizaa, id=pizza_id)
    cart = get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, pizza=pizza)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart = get_cart(request)
    items = cart.items.all()
    total=sum(item.subtotal() for item in items)
    return render(request, 'cart.html', {'cart': cart, 'items': items,'total':total})
@login_required
def remove_from_cart(request, item_id):
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    return redirect('view_cart')
@login_required
def increment_quantity(request, item_id):
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')
@login_required
def decrement_quantity(request, item_id):
    cart = get_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('view_cart')


@login_required
def delivery_option(request):
    if request.method == "POST":
        delivery_type = request.POST.get('delivery_type')
        address = request.POST.get('address')

        request.session['delivery_type'] = delivery_type
        request.session['address'] = address

        return redirect('checkout')

    return render(request, 'delivery_option.html')


@login_required
def checkout(request):
    delivery_type = request.session.get('delivery_type')
    address = request.session.get('address')

    if not delivery_type:
        return redirect('delivery_option')

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()

    total_amount = sum(item.subtotal() for item in items)

    razorpay_order = client.order.create({
        "amount": int(total_amount * 100),
        "currency": "INR",
        "payment_capture": 1
    })

    order = Order.objects.create(
        user=request.user,
        total_amount=total_amount,
        delivery_type=delivery_type,
        delivery_address=address,
        razorpay_order_id=razorpay_order['id'],
        payment_status="Paid"
    )

    return render(request, 'checkout.html', {
        'items': items,
        'total': total_amount,
        'order': order,
        'delivery_type': delivery_type,
        'address': address,
        'razorpay_key': settings.RAZORPAY_KEY_ID
    })

@login_required
@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        data = json.loads(request.body)

        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_signature = data.get('razorpay_signature')

        order = get_object_or_404(Order, razorpay_order_id=razorpay_order_id)

        # ✅ Update order payment info
        order.razorpay_payment_id = razorpay_payment_id
        order.razorpay_signature = razorpay_signature
        order.payment_status = "COMPLETED"
        order.save()

        # ✅ Get delivery info from session
        delivery_type = request.session.get('delivery_type')
        address = request.session.get('address')

        # ✅ Move cart items to OrderItem
        cart = Cart.objects.get(user=order.user)
        cart_items = cart.items.all()

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                pizza=item.pizza,
                quantity=item.quantity,
                price=item.pizza.price,
                delivery_type=delivery_type,
                address=address,
                payment_status="PAID",
            )

        # ✅ CLEAR CART (ONCE, outside loop)
        cart_items.delete()

        # ✅ CLEAR DELIVERY SESSION DATA (SAFE)
        request.session.pop('delivery_type', None)
        request.session.pop('address', None)

        return HttpResponse(status=200)

    return HttpResponse(status=400)

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_success.html', {'order': order})

@login_required
def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_order_{order.id}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, height - 50, "Invoice")

    p.setFont("Helvetica", 12)
    p.drawString(50, height - 100, f"Order ID: {order.id}")
    p.drawString(50, height - 120, f"Customer: {order.user.username}")
    p.drawString(50, height - 140, f"Total Amount: ₹{order.total_amount}")
    p.drawString(50, height - 160, f"Payment Status: {order.payment_status}")
    p.drawString(50, height - 180, "Items:")

    y = height - 200
    for item in order.items.all():
        p.drawString(60, y, f"{item.pizza.name} - Qty: {item.quantity} - Price: ₹{item.price} - Subtotal: ₹{item.subtotal()}")
        y -= 20

    p.showPage()
    p.save()
    return response