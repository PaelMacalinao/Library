from django.urls import path
from . import views

urlpatterns = [
    path('', views.books, name='books'),
    path('category/<str:link_category>/', views.category, name='category'),
]