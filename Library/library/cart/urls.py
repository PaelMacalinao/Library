from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('removeItem/<int:product_id>/', views.remove_from_cart, name='removeItem'),
    path('update_quantity/', views.update_quantity, name='update_quantity'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]