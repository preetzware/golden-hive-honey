from decimal import Decimal
from django.conf import settings

def cart_contents(request):
    """ 
    Context processor to make cart contents available across the application 
    """
    cart = request.session.get('cart', {})  # Retrieve cart from session or initialize an empty cart

    cart_items = []
    total = 0
    product_count = 0

    # Process each item in the cart
    for item_id, item_data in cart.items():
        try:
            price = Decimal(item_data['price'])  # Ensure proper decimal handling for price
            quantity = item_data['quantity']
            name = item_data.get('name', 'Unknown Product')
            image = item_data.get('image', None)

            # Add the product details to the cart items list
            cart_items.append({
                'id': item_id,
                'name': name,
                'quantity': quantity,
                'price': price,
                'subtotal': price * quantity,
                'image': image,
            })

            # Update totals
            total += price * quantity
            product_count += quantity
        except KeyError:
            continue  # Skip any improperly formatted cart items

    # Delivery cost calculations
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    # Grand total
    grand_total = delivery + total

    # Context to be passed to templates
    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
