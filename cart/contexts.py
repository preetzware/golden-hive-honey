from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def cart_contents(request):
    cart = request.session.get('cart', {})

    cart_items = []
    total = 0
    product_count = 0

    for product_id, item_data in cart.items():
        try:
            product = get_object_or_404(Product, id=product_id)
            quantity = item_data.get('quantity', 0) if isinstance(item_data, dict) else item_data
            total += quantity * product.price
            product_count += quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_price': quantity * product.price,
            })
        except Exception as e:
            print(f"Error processing cart product {product_id}: {e}")

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    return {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }
