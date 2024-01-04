import os
import json
import django

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
django.setup()

from account.models import Product
import json


json_file_path = 'data/amazon_books.json'  # Replace with the actual path
data = json.load(open(json_file_path))

for entry in data:
    title = entry.get('title', '')
    pageCount = entry.get('pageCount', '')
    thumbnailUrl = entry.get('thumbnailUrl', '')
    description = entry.get('shortDescription', '')
    categories = entry.get('categories', '')
    authors = entry.get('authors', '')
    price = entry.get('price', '')

    if not Product.objects.filter(title=title).exists():
        Product.objects.create(title=title, pageCount=pageCount, thumbnailUrl=thumbnailUrl, description=description, categories=categories, authors=authors, price=price)
        print(f'Successfully added product: {title}')
    else:
        print(f'Product already exists: {title}')
