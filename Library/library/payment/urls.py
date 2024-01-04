from django.urls import path
from . import views

urlpatterns = [
    path('buy/<int:product_id>/', views.buy, name='payment_buy'),
    path('checkout/<int:cart_id>/', views.checkout, name='payment_checkout'),
]