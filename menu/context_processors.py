# context_processors.py
from menu.models import Carrito, CarritoItem

def carrito_items_count(request):
    if request.user.is_authenticated:
        try:
            carrito = Carrito.objects.get(usuario=request.user)
            count = CarritoItem.objects.filter(carrito=carrito).count()
        except Carrito.DoesNotExist:
            count = 0
    else:
        count = 0
    return {
        'carrito_items_count': count
    }
