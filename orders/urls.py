from django.urls import path
from . import views

urlpatterns = [
    path('add_to_cart/<int:pizza_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increment_quantity/<int:item_id>/', views.increment_quantity, name='increment_quantity'),
    path('decrement_quantity/<int:item_id>/', views.decrement_quantity, name='decrement_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('order_history/', views.order_history, name='order_history'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order_success/<int:order_id>/', views.order_success, name='order_success'),
    path('download_invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),
    path('delivery/', views.delivery_option, name='delivery_option'),

]