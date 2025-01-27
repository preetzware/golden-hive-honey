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
    if price is None or quantity is None:
        return 0  # Return 0 for invalid inputs
    return price * quantity