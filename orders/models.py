from django.db import models
from django.conf import settings
from store.models import Pizaa

class Cart(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart of {self.user}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    pizza = models.ForeignKey(Pizaa, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.pizza.price * self.quantity

    def __str__(self):
        return f"{self.pizza.name} ({self.quantity})"
    

from django.db import models
from django.conf import settings

class Order(models.Model):

    DELIVERY_CHOICES = [
        ('HOME', 'Home Delivery'),
        ('PICKUP', 'Store Pickup'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    total_amount = models.PositiveIntegerField()

    # 🔹 Delivery fields
    delivery_type = models.CharField(
        max_length=100,
        choices=DELIVERY_CHOICES
    )
    delivery_address = models.TextField(
        blank=True,
        null=True
    )

    # 🔹 Payment fields
    payment_status = models.CharField(
        max_length=100,
        default="PENDING"
    )

    razorpay_order_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    razorpay_payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    razorpay_signature = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user}"



class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    pizza = models.ForeignKey(Pizaa, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    delivery_type = models.CharField(max_length=10)
    address = models.TextField(blank=True, null=True)
    payment_status = models.CharField(max_length=20)

