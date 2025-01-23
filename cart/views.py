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

        # Retrieve the session cart
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
                'weight': weight,  # Store weight if applicable
            }

        # Save the updated cart back into the session
        request.session['cart'] = cart
        messages.success(request, "Product added successfully!")

    except ValueError:
        messages.error(request, "Invalid quantity provided.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return redirect(request.POST.get('redirect_url', '/'))


def adjust_cart(request, product_id):
    """Adjust the quantity of the specified product in the shopping cart."""
    try:
        # Ensure the product exists
        product = get_object_or_404(Product, id=product_id)

        # Validate quantity
        quantity = int(request.POST.get('quantity', 0))
        if quantity < 0:
            messages.error(request, "Invalid quantity provided.")
            return redirect('view_cart')

        # Retrieve the selected weight (if applicable)
        weight = request.POST.get('weight', None)

        # Retrieve the session cart
        cart = request.session.get('cart', {})

        # Generate a unique key combining product_id and weight (if applicable)
        item_key = f"{product_id}-{weight}" if weight else str(product_id)

        if item_key in cart:
            if quantity > 0:
                # Update the quantity for the item
                cart[item_key]['quantity'] = quantity
            else:
                # Remove the item if quantity is zero
                cart.pop(item_key)
        else:
            messages.error(request, "The item does not exist in the cart.")
            return redirect('view_cart')

        # Save the updated cart back into the session
        request.session['cart'] = cart

        # Redirect to the view cart page
        return redirect('view_cart')

    except ValueError:
        messages.error(request, "Invalid quantity provided.")
        return redirect('view_cart')
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('view_cart')


def remove_from_cart(request, product_id):
    """Remove the specified product from the shopping cart."""
    try:
        # Retrieve the weight if applicable
        weight = request.POST.get('product_weight', None)

        # Retrieve the session cart
        cart = request.session.get('cart', {})

        # Generate a unique key combining product_id and weight (if applicable)
        item_key = f"{product_id}-{weight}" if weight else str(product_id)

        # Remove the item from the cart
        if item_key in cart:
            cart.pop(item_key)
            request.session['cart'] = cart  # Save updated cart to session
            messages.success(request, "Item removed successfully.")
        else:
            messages.error(request, "Item not found in the cart.")

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return redirect('view_cart')  # Redirect back to the cart page
