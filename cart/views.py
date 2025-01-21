from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product

def view_cart(request):
    """ A view to render the cart contents page """
    return render(request, 'cart/cart.html')


def add_to_cart(request, product_id):
    """Add a quantity of the specified product to the shopping cart"""
    try:
        # Ensure the product exists
        product = get_object_or_404(Product, id=product_id)

        # Validate quantity
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            messages.error(request, "Invalid quantity. Please enter a positive number.")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        # Retrieve the selected weight (if applicable)
        weight = request.POST.get('weight', None)
        price = float(product.price)  # Convert product price to float

        # Adjust price if weight is selected and the product has weight options
        if weight and product.has_weight:
            weight_prices = product.weight_prices or {}
            price = float(weight_prices.get(weight, product.price))  # Convert Decimal to float

        # Retrieve the redirect URL and the session cart
        redirect_url = request.POST.get('redirect_url', '/')
        cart = request.session.get('cart', {})

        # Generate a unique key combining product_id and weight (if applicable)
        item_key = f"{product_id}-{weight}" if weight else str(product_id)

        # Update or add the product to the cart
        if item_key in cart:
            cart[item_key]['quantity'] += quantity
        else:
            cart[item_key] = {
                'quantity': quantity,
                'price': price,  # Ensure price is stored as float
                'weight': weight,
            }

        # Save the updated cart back into the session
        request.session['cart'] = cart
        messages.success(request, "Product added successfully!")

    except ValueError:
        messages.error(request, "Invalid quantity provided.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return redirect(redirect_url)