from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Product, Category
from django.db.models import Q

def all_products(request):
    """ A view to show all products and handle search queries """
    query = request.GET.get('q')
    products = Product.objects.all()

    if not query:  # Case: No search input
        messages.error(request, "You didn't enter any search criteria!")
        return redirect(reverse('products'))

    if query:
        # Filter products based on the search query
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        # Show a success message with the number of results
        messages.success(request, f"Search results for '{query}': {products.count()} product(s) found.")

    context = {
        'products': products,
        'search_term': query, 
    }

    return render(request, 'products/all_products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """
    product = get_object_or_404(Product, id=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)