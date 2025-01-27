from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def cart_contents(request):
    cart = request.session.get('cart', {})  # Retrieve the cart from the session

    cart_items = []
    total = Decimal(0)
    product_count = 0

    for product_key, item_data in cart.items():
        try:
            # Extract product ID and weight (if applicable)
            product_id = product_key.split('-')[0]  # Extract product ID
            weight = product_key.split('-')[1] if '-' in product_key else None

            # Fetch the product object
            product = get_object_or_404(Product, id=product_id)

            # Quantity of the product in the cart
            quantity = item_data.get('quantity', 0) if isinstance(item_data, dict) else item_data

            # Determine the price (based on weight if applicable)
            if product.has_weight and weight:
                weight_prices = product.weight_prices or {}
                price = Decimal(weight_prices.get(weight, 0))  # Fetch weight-specific price
                if price == 0:
                    raise ValueError(f"Invalid weight '{weight}' for product '{product.name}'.")
            else:
                price = Decimal(product.price)

            # Update totals and add to cart items
            total += quantity * price
            product_count += quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'total_price': quantity * price,
                'weight': weight,  # Include weight for display purposes
            })

        except Exception as e:
            print(f"Error processing cart product {product_key}: {e}")


    # Delivery Charges Calculation
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * (Decimal(settings.STANDARD_DELIVERY_PERCENTAGE) / Decimal(100))
        free_delivery_delta = Decimal(settings.FREE_DELIVERY_THRESHOLD) - total
    else:
        delivery = Decimal(0)
        free_delivery_delta = Decimal(0)

    # Calculate grand total
    grand_total = total + delivery

    # Return context
    return {
        'cart_items': cart_items,               # List of all items in the cart
        'total': total,                         # Total cost of products
        'product_count': product_count,         # Total quantity of products
        'delivery': delivery,                   # Delivery cost
        'free_delivery_delta': free_delivery_delta,  # Amount needed for free delivery
        'free_delivery_threshold': Decimal(settings.FREE_DELIVERY_THRESHOLD),
        'grand_total': grand_total,             # Grand total including delivery
    }
