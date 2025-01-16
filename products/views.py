from django.shortcuts import render
from .models import Product, Category
from django.db.models import Q, Case, When

def all_products(request):
    """
    View to display all products with optional sorting and search functionality.
    """
    products = Product.objects.all()
    # Categories in the desired order: Honey, Propolis, Hampers, Beeswax
    categories = Category.objects.filter(name__in=["Honey", "Propolis", "Hampers", "Beeswax"]).order_by(
        Case(
            When(name="Honey", then=0),
            When(name="Propolis", then=1),
            When(name="Hampers", then=2),
            When(name="Beeswax", then=3),
            default=4,
        )
    )

    # Get sorting and search query parameters
    sort = request.GET.get('sort', None)
    direction = request.GET.get('direction', None)
    search_query = request.GET.get('q', None)

    # Search functionality
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

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
