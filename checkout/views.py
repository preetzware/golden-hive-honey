from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm

# Create your views here.

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "There's nothing in your cart at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51Ql8DlEinozhTRXFgAxiCU7INx1Y5rjXwrKQcT5zoN3uQgvS1rlhy3V1hwA6or1qfVrcnnt4Rug5xjwxzxIs5YhL00V5M7DnTq',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)