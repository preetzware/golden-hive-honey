from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Product, Category
from django.db.models import Q

def all_products(request):
    """ A view to show all products and handle category filtering, search queries, and sorting """
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = 'asc'

    # Handle category filtering
    if 'category' in request.GET:
        categories = request.GET['category'].split(',')
        products = products.filter(category__name__in=categories)
        categories = Category.objects.filter(name__in=categories)

    # Handle search input
    if 'q' in request.GET:
        query = request.GET['q']
        if not query.strip():
            messages.error(request, "You didn't enter any search criteria!")
            return redirect(reverse('all_products'))

        queries = Q(name__icontains=query) | Q(description__icontains=query)
        products = products.filter(queries)

        if products.exists():
            messages.success(request, f"Search results for '{query}': {products.count()} product(s) found.")
        else:
            messages.error(request, f"No results found for '{query}'.")

    # Handle sorting
    if 'sort' in request.GET:
        sort = request.GET['sort']
        if '&direction=' in sort:
            sort, direction = sort.split('&direction=')

        if direction == 'desc':
            sort = f'-{sort}'
        products = products.order_by(sort)

    # Current sorting for template
    current_sorting = f"{sort}_{direction}" if sort else "None_None"

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/all_products.html', context)



def product_detail(request, product_id):
    """ A view to show individual product details """
    product = get_object_or_404(Product, id=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)