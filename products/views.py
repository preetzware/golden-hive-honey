from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q, Case, When


#Create your views here.

def all_products(request):
    """ A view to show all products """
    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/all_products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """
    product = get_object_or_404(Product, id=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)