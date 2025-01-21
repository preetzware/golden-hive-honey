from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product

def view_cart(request):
    """ A view to render the cart contents page """
    return render(request, 'cart/cart.html')


from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from products.models import Product

def add_to_cart(request, product_id):
    """ Add a quantity of the specified product with a selected weight to the shopping cart """

    try:
        # Ensure the product exists
        product = get_object_or_404(Product, id=product_id)

        # Validate quantity
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            messages.error(request, "Invalid quantity. Please enter a positive number.")
            return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to previous page

        # Check if the product has weight options
        selected_weight = request.POST.get('weight')
        price = product.price  # Default price
        if product.has_weight and selected_weight:
            weight_prices = product.weight_prices or {}
            price = weight_prices.get(selected_weight)
            if price is None:
                messages.error(request, "Invalid weight selected.")
                return redirect(request.META.get('HTTP_REFERER', '/'))  # Redirect to previous page

        # Retrieve the redirect URL and the session cart
        redirect_url = request.POST.get('redirect_url', '/')
        cart = request.session.get('cart', {})  # Get the cart from the session or initialize a new one

        # Update or add the product to the cart
        product_key = f"{product_id}-{selected_weight}" if selected_weight else str(product_id)
        if product_key in cart:
            cart[product_key]['quantity'] += quantity
        else:
            cart[product_key] = {
                'quantity': quantity,
                'weight': selected_weight,
                'price': price,
            }

        # Save the updated cart back into the session
        request.session['cart'] = cart

        # Add a success message
        messages.success(request, f"{product.name} ({selected_weight if selected_weight else 'Standard'}) added to your cart!")

    except ValueError:
        # Handle invalid quantity values
        messages.error(request, "Invalid quantity provided.")
    except Exception as e:
        # Handle any other unexpected errors
        messages.error(request, f"An error occurred: {str(e)}")

    return redirect(redirect_url)