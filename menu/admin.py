from django.contrib import admin


from .models import Usuario, Articulos, Pedidos, Carrito, CarritoItem, Comuna, Venta, DetalleVenta
# Register your models here.

class UsuariosAdmin(admin.ModelAdmin):
    list_display=("nombre", "tfno")
    search_fields=("nombre","apellido")

class ArticulosAdmin(admin.ModelAdmin):
    list_filter=("stock",)

class PedidosAdmin(admin.ModelAdmin):
    list_display=("numero","fecha")
    list_filter=("fecha",)
    date_hierarchy="fecha"


admin.site.register(Usuario,UsuariosAdmin)
admin.site.register(Articulos,ArticulosAdmin)
admin.site.register(Pedidos,PedidosAdmin)
admin.site.register(Carrito)
admin.site.register(CarritoItem)
admin.site.register(Comuna)
admin.site.register(Venta)
admin.site.register(DetalleVenta)

