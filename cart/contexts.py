from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def cart_contents(request):
    cart = request.session.get('cart', {})

    cart_items = []
    total = Decimal(0)
    product_count = 0

    for product_key, item_data in cart.items():
        try:
            # Extract product ID and weight (if present)
            product_id = product_key.split('-')[0]  # Extract product ID
            weight = None
            if '-' in product_key:
                weight = product_key.split('-')[1]  # Extract weight if present

            # Fetch product object
            product = get_object_or_404(Product, id=product_id)
            quantity = item_data.get('quantity', 0) if isinstance(item_data, dict) else item_data

            # Determine price based on weight or default to product's base price
            if weight and product.has_weight:
                price = Decimal(product.weight_prices.get(weight, product.price))
            else:
                price = Decimal(product.price)

            # Update totals and cart items
            total += quantity * price
            product_count += quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'weight': weight,
                'price': price,
                'total_price': quantity * price,
            })
        except Exception as e:
            print(f"Error processing cart product {product_key}: {e}")

    # Calculate delivery charges
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * (Decimal(settings.STANDARD_DELIVERY_PERCENTAGE) / Decimal(100))
        free_delivery_delta = Decimal(settings.FREE_DELIVERY_THRESHOLD) - total
    else:
        delivery = Decimal(0)
        free_delivery_delta = Decimal(0)

    grand_total = delivery + total

    return {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': Decimal(settings.FREE_DELIVERY_THRESHOLD),
        'grand_total': grand_total,
    }
    