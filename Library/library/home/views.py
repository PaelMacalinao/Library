from django.contrib.auth import logout
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from account.models import Product

# Create your views here.

def home(request):
    products = Product.objects.filter(categories=[])

    items_per_page = 12
    paginator = Paginator(products, items_per_page)

    page = request.GET.get('page')

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request,  'home.html', {'book_count': len(products),'objects': objects, 'paginator': paginator, 'page_obj': objects})


def logout_user(request):
 logout(request)
 messages.success(request, ("You have been logged Out..."))
 return redirect('home')