from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply the value by the argument."""
    try:
        return value * arg
    except (TypeError, ValueError):
        return 0  # Return 0 if the multiplication fails

@register.filter
def calc_subtotal(price, quantity):
    """Calculate the subtotal for an item."""
    return price * quantity