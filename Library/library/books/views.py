from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from account.models import Product
import re

# Create your views here.
def clean_category_string(category):
    cleaned_category = re.sub(r'[^a-zA-Z0-9_]', '', category.replace(' ', '_'))
    return cleaned_category

def books(request):
    products = Product.objects.all()
    categories = set()

    for book in products:
        for category in book.categories:
            categories.add(clean_category_string(category).capitalize())

    items_per_page = 16
    paginator = Paginator(products, items_per_page)

    page = request.GET.get('page')

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    return render(request,  'books.html', {'page_title': 'Books','book_count': len(products),'objects': objects, 'categories':sorted(categories), 'paginator': paginator, 'page_obj': objects})


def category(request, link_category):
    products = Product.objects.all()

    object_list = []
    categories = set()

    for book in products:
        for category in book.categories:
            ccs = clean_category_string(category)
            categories.add(clean_category_string(category).capitalize())
            if ccs.capitalize() == link_category:
                object_list.append(book)

    items_per_page = 16
    paginator = Paginator(object_list, items_per_page)
    page = request.GET.get('page')

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    link_category = link_category.replace("_", " ")
    return render(request,  'books.html', {'page_title': link_category, 'book_count': len(object_list),'objects': objects, 'categories':sorted(categories), 'paginator': paginator, 'page_obj': objects})
