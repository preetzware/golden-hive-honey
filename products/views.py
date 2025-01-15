from django.shortcuts import render
from .models import Product, Category

def all_products(request):
    """
    View to display all products with optional sorting and search functionality.
    """
    products = Product.objects.all()
    categories = Category.objects.all()

    # Get sorting and search query parameters
    sort = request.GET.get('sort', None)
    direction = request.GET.get('direction', None)
    search_query = request.GET.get('q', None)

    # Search functionality
    if search_query:
        products = products.filter(name__icontains=search_query) | products.filter(description__icontains=search_query)

    # Sorting functionality
    if sort:
        if sort == 'price':
            sort_key = 'price'
        elif sort == 'name':
            sort_key = 'name'
        elif sort == 'category':
            sort_key = 'category__name'
        else:
            sort_key = None

        if sort_key and direction == 'desc':
            sort_key = f'-{sort_key}'
        if sort_key:
            products = products.order_by(sort_key)

    context = {
        'products': products,
        'categories': categories,
        'current_sorting': f'{sort}_{direction}',
        'search_query': search_query,
    }
    return render(request, 'products/all_products.html', context)
