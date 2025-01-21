from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product

def view_cart(request):
    """ A view to render the cart contents page """
    return render(request, 'cart/cart.html')


def add_to_cart(request, product_id):
    """ Add a quantity of the specified product to the shopping cart """

    try:
        # Ensure the product exists
        get_object_or_404(Product, id=product_id)  # Validate the product ID exists

        # Validate quantity
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            messages.error(request, "Invalid quantity. Please enter a positive number.")
            return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to previous page

        # Retrieve the redirect URL and the session cart
        redirect_url = request.POST.get('redirect_url', '/')
        cart = request.session.get('cart', {})  # Get the cart from the session or initialize a new one

        # Update or add the product to the cart
        if str(product_id) in cart:
            cart[str(product_id)]['quantity'] += quantity
        else:
            cart[str(product_id)] = {'quantity': quantity}

        # Save the updated cart back into the session
        request.session['cart'] = cart

        # Add a generic success message
        messages.success(request, "Product added successfully!")

    except ValueError:
        # Handle invalid quantity values
        messages.error(request, "Invalid quantity provided.")
    except Exception as e:
        # Handle any other unexpected errors
        messages.error(request, f"An error occurred: {str(e)}")

    return redirect(redirect_url)