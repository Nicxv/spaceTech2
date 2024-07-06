# context_processors.py
from .models import Cart, CartItem
from django.db.models import Sum
def carrito_items_count(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        carrito_items_count = CartItem.objects.filter(cart=cart).aggregate(total_quantity=Sum('quantity'))['total_quantity'] or 0
    else:
        carrito_items_count = 0
    return {
        'carrito_items_count': carrito_items_count
    }