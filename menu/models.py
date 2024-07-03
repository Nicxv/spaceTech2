import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


# Create your models here.


from django.db import models

class Usuario(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrador'),
        ('BODEGA', 'Bodeguero'),
        ('CLIENT', 'Cliente'),
    ]
    
    nombre_usuario = models.CharField(max_length=30)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    tfno = models.CharField(max_length=8, verbose_name="Telefono")
    clave = models.CharField(max_length=30)
    confirmar_clave = models.CharField(max_length=30)
    direccion = models.CharField(max_length=255, verbose_name="Dirección", null=True, blank=True)
    role = models.CharField(max_length=6, choices=ROLE_CHOICES)
    
    def __str__(self):
        return f'{self.nombre} {self.apellido}'


    

class Articulos(models.Model):
    
    nombre = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=50)
    precio = models.IntegerField()
    stock = models.IntegerField()
    foto = models.ImageField(upload_to='static/img/', blank=True, null=True)
    marca = models.CharField(max_length=30, default='Sin Marca')
    precio_oferta = models.IntegerField(blank=True, null=True)
    descuento = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    

    def __str__(self):
        return self.nombre

class Pedidos(models.Model):
        numero=models.IntegerField()
        fecha=models.DateField()
        entregado=models.BooleanField()


class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    creado_en = models.DateTimeField(auto_now_add=True)

class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Articulos, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    agregado_en = models.DateTimeField(default=timezone.now)        
    




class Comuna(models.Model):
    nombre = models.CharField(max_length=100)
    precio_envio = models.IntegerField(default=1)  # Precio de envío en pesos chilenos

    def __str__(self):
        return self.nombre



class Imagen(models.Model):
    
    imagen = models.ImageField(upload_to='static/img/')

    def __str__(self):
        return f"Imagen de {self.articulo.nombre}"
    

class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True, editable=False)
    rut_empresa = models.CharField(max_length=13, verbose_name='RUT de la Empresa')
    nombre_empresa = models.CharField(max_length=100, verbose_name='Nombre de la Empresa')
    representante_legal = models.CharField(max_length=100, verbose_name='Representante Legal', default="")
    contacto_empresa = models.CharField(max_length=50, verbose_name='Contacto de la Empresa')
    direccion_proveedor = models.CharField(max_length=255, verbose_name='Dirección', default="sin direccion")
    email_proveedor = models.EmailField(max_length=70, unique=True, null=True, blank=True)

    def str(self):
        return self.nombre_empresa



    



class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True, editable=False)
    nombre_producto = models.CharField(max_length=100, verbose_name='Nombre del Producto')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, verbose_name='Proveedor')
    stock_actual = models.IntegerField(verbose_name='Stock Actual', null=True, blank=True)
    stock_minimo = models.IntegerField(verbose_name='Stock Mínimo', null=True, blank=True)
    precio_costo = models.IntegerField(verbose_name='Precio de Costo')
    precio_venta = models.IntegerField(verbose_name='Precio de Venta', default=0)
    foto_producto = models.ImageField(upload_to='static/img/', verbose_name='Foto del Producto', null=True, blank=True)
    mostrar_en_home = models.BooleanField(default=False, verbose_name='Mostrar en Home')    
    
    def __str__(self):
        return self.nombre_producto


class Compra(models.Model):
    id_orden_compra = models.UUIDField(primary_key=True, editable=False)
    fecha = models.DateTimeField(auto_now_add=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, verbose_name='Proveedor')
    sub_total = models.IntegerField()
    iva = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return f'Compra {self.id_orden_compra} - {self.proveedor.nombre_empresa}'  


class DetalleCompra(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    orden_compra = models.ForeignKey(Compra, on_delete=models.CASCADE, verbose_name='Orden de Compra', related_name='detalles')
    correlativo = models.IntegerField(verbose_name='Número Correlativo')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, verbose_name='Producto')
    cantidad = models.IntegerField()
    precio_costo = models.IntegerField()
    sub_total = models.IntegerField()

    def __str__(self):
        return f'Detalle {self.correlativo} de {self.orden_compra}'
    
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_at = models.DateTimeField(default=timezone.now)

class Venta(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_boleta = models.CharField(max_length=30)
    fecha = models.DateTimeField(default=timezone.now)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Venta {self.id} - Usuario {self.usuario.nombre_usuario}'

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Detalle de Venta {self.venta.id} - Producto {self.producto.nombre_producto}'    