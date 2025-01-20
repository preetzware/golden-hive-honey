from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Product, Category
from django.db.models import Q

def all_products(request):
    """ A view to show all products and handle category filtering and search queries """
    products = Product.objects.all()  # Retrieve all products
    query = None  # Initialize query for search
    categories = None  # Initialize categories

    # Handle category filtering
    if 'category' in request.GET:
        categories = request.GET['category'].split(',')  # Split categories into a list
        products = products.filter(category__name__in=categories)  # Filter by category names
        categories = Category.objects.filter(name__in=categories)  # Fetch the category objects

    # Handle search input
    if 'q' in request.GET:
        query = request.GET['q']  # Get the search term
        if not query.strip():  # Check if the search query is empty or whitespace
            messages.error(request, "You didn't enter any search criteria!")
            return redirect(reverse('all_products'))  # Redirect back to the products page

        # Filter products by search term
        queries = Q(name__icontains=query) | Q(description__icontains=query)
        products = products.filter(queries)

        # Add success or error message based on results
        if products.exists():
            messages.success(request, f"Search results for '{query}': {products.count()} product(s) found.")
        else:
            messages.error(request, f"No results found for '{query}'.")

    # Prepare context for the template
    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
    }

    return render(request, 'products/all_products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """
    product = get_object_or_404(Product, id=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)