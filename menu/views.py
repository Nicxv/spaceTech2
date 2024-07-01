from decimal import Decimal
from pyexpat.errors import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from menu.forms import ArticulosForm, LoginForm, Usuario2Form, UsuarioForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test

from django.contrib.auth import authenticate, login as auth_login, logout

from menu.models import Articulos, Carrito, CarritoItem, Usuario, Venta, DetalleVenta


# Create your views here.
from django.shortcuts import render
from .models import RecepcionProducto

def home_view(request):
    productos = RecepcionProducto.objects.filter(en_resumen=True)

    # Asegurarnos de que todos los productos tengan un precio_venta válido
    for producto in productos:
        if not isinstance(producto.precio_venta, (int, float, Decimal)):
            producto.precio_venta = Decimal('0.0')
    
    return render(request, 'home.html', {'productos': productos})

def busqueda_productos(request):

    return render(request, "busqueda_productos.html")

def buscar(request):
    
    
    if request.GET.get("prd"):

    
        mensaje="Articulo buscado: %r" %request.GET.get("prd")
        producto=request.GET.get("prd")

        #articulos=Articulos.objects.filter(nombre__icontains=producto)

    else:

        mensaje="no has introducido nada"

    

    return HttpResponse(mensaje)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')  # Redirige a la página principal si el usuario ya está autenticado
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = Usuario.objects.get(email=email)
                if user.clave == password:
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    user_django, created = User.objects.get_or_create(username=user.email, defaults={'email': user.email})
                    if created:
                        user_django.set_password(user.clave)
                        user_django.save()

                    user_django = authenticate(request, username=user.email, password=user.clave)
                    
                    if user_django:
                        auth_login(request, user_django)
                        request.session['role'] = user.role  # Guardar el rol en la sesión
                        messages.success(request, 'Inicio de sesión exitoso.')
                        return redirect('/')  # Redirigir a la página principal
                    else:
                        messages.error(request, 'Error en la autenticación del usuario.')
                else:
                    messages.error(request, 'Correo o contraseña incorrectos.')
            except Usuario.DoesNotExist:
                messages.error(request, 'Correo o contraseña incorrectos.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def add_user_role_to_context(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                user = Usuario.objects.get(email=request.user.username)
                request.user.role = user.role
            except Usuario.DoesNotExist:
                request.user.role = None
        return view_func(request, *args, **kwargs)
    return wrapper

def logout_view(request):
    logout(request)
    return redirect('home')

def profile_view(request):
    if request.user.is_authenticated:
        try:
            # Obtener el perfil del usuario desde la base de datos
            perfil_usuario = Usuario.objects.get(email=request.user.email)
        except Usuario.DoesNotExist:
            perfil_usuario = None
        
        return render(request, 'profile.html', {'perfil_usuario': perfil_usuario})
    else:
        # Si el usuario no está autenticado, redirigir a la página de inicio de sesión
        return redirect('login')

# views.py
from django.shortcuts import render, get_object_or_404
from .models import RecepcionProducto

# views.py
from django.shortcuts import render, get_object_or_404
from .models import RecepcionProducto

def detalle_producto(request, id):
    producto = get_object_or_404(RecepcionProducto, pk=id)
    return render(request, 'detalle_producto.html', {'producto': producto})




def publicidad(request):
    return render(request, 'publicidad.html')



#paginas de admin 
@login_required
def listaU(request):
    role_filter = request.GET.get('role', None)
    if role_filter:
        usuarios = Usuario.objects.filter(role=role_filter)
    else:
        usuarios = Usuario.objects.all()
    roles = Usuario.ROLE_CHOICES
    return render(request, 'listaU.html', {'usuarios': usuarios, 'roles': roles})

@login_required
def listaP(request):
    productos = Articulos.objects.all()  # Recupera todos los usuarios
    return render(request, 'listaP.html', {'productos': productos})

def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    messages.success(request, 'Usuario eliminado con éxito')
    return redirect('listaU')
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        form = Usuario2Form(request.POST, instance=usuario)
        if form.is_valid():
            usuario = form.save(commit=False)
            role = form.cleaned_data.get('role')

            # Asignar el rol
            usuario.role = role

            usuario.save()

            messages.success(request, 'Usuario modificado con éxito')
            return redirect('listaU')
    else:
        form = Usuario2Form(instance=usuario)
    return render(request, 'editar_usuario.html', {'form': form, 'usuario': usuario})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Articulos, Comuna, RecepcionProducto
from .forms import ArticulosForm, UpdateProfileForm

def modificarP(request, producto_id):
    producto = get_object_or_404(Articulos, id=producto_id)
    if request.method == 'POST':
        form = ArticulosForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto modificado con éxito')
            return redirect('listaP')
        else:
            print("Formulario no válido:", form.errors)
    else:
        form = ArticulosForm(instance=producto)
    
    return render(request, 'modificarP.html', {'form': form, 'producto': producto})
#Plantillas de menu
@add_user_role_to_context
def menu(request):
    return render(request, 'plantilla/menu.html', {'user': request.user})

def formulario(request):
    # Redirige a la página principal si el usuario ya está autenticado
    if request.user.is_authenticated:
        return redirect('listaU')

    mensaje_exito = None
    mensaje_error = None

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.role = 'CLIENT'  # Asignar el rol de cliente
            usuario.save()
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('login')  # Redirigir a la página de login después del registro
        else:
            mensaje_error = "Por favor, corrige los errores del formulario."
    else:
        form = UsuarioForm()

    return render(request, 'formulario.html', {'form': form, 'mensaje_exito': mensaje_exito, 'mensaje_error': mensaje_error})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Articulos
from .forms import ArticulosForm

def agregar_producto(request):
    if request.method == 'POST':
        form = ArticulosForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            print("Formulario no válido:", form.errors)
    else:
        form = ArticulosForm()
    return render(request, 'agregarP.html', {'form': form})

from django.shortcuts import render, get_object_or_404
from .models import RecepcionProducto, Carrito, CarritoItem

def detalle_producto(request, producto_id):
    producto = get_object_or_404(RecepcionProducto, id=producto_id)
    
    carrito_items_count = 0
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        carrito_items_count = CarritoItem.objects.filter(carrito=carrito).count()
    
    return render(request, 'detalle_producto.html', {'producto': producto, 'carrito_items_count': carrito_items_count})


def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Articulos, id=producto_id)
    producto.delete()
    messages.success(request, 'Producto eliminado con éxito')
    return redirect('listaP')




from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.conf import settings

from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.conf import settings
  # Importa el modelo Fotos

from datetime import datetime, timedelta

def enviar_publicidad(request):
    if request.method == 'POST':
        imagen = request.FILES['imagen']
        tiempo = int(request.POST['tiempo'])  # Convierte el tiempo a entero
        segundos = int(request.POST['segundos'])  # Convierte los segundos a entero
        # Calcula el precio basado en el tiempo y los segundos
        precio = calcular_precio(tiempo, segundos)
        
        # Calcula la fecha de hoy
        fecha_hoy = datetime.now().date()
        # Calcula la fecha de término de la publicidad
        fecha_termino = fecha_hoy + timedelta(weeks=tiempo)

        # Procesa los datos y envía el correo electrónico
        asunto = 'Nueva Publicidad'
        mensaje = f'Se ha recibido una nueva solicitud de publicidad.\n\nPrecio: {precio} CLP\nTiempo: {tiempo} semanas\nSegundos: {segundos}\nFecha de inicio: {fecha_hoy}\nFecha de término: {fecha_termino}'
        email = EmailMessage(asunto, mensaje, settings.EMAIL_HOST_USER, ['alvarover.x@gmail.com'])
        
        # Adjunta la imagen al correo electrónico
        email.attach(imagen.name, imagen.read(), imagen.content_type)
        email.send()

        # Guarda la foto en la base de datos
        
        return redirect('publicidad')
    
    return render(request, 'publicidad.html')

def calcular_precio(tiempo, segundos):
    # Define el precio base en pesos chilenos
    precio_base = 3000
    # Ajusta el precio basado en el tiempo seleccionado
    if tiempo == 2:
        precio_base *= 2  # Duplica el precio para 2 semanas
    elif tiempo == 4:
        precio_base *= 4  # Cuadruplica el precio para 1 mes
    elif tiempo == 12:
        precio_base *= 12  # Multiplica el precio por 12 para 3 meses
    # Ajusta el precio basado en la duración en segundos
    precio_total = precio_base * segundos / 15  # Ajusta el precio en función de la relación 15 segundos = $100
    return precio_total


def update_profile_view(request):
    usuario = Usuario.objects.get(email=request.user.email)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UpdateProfileForm(instance=usuario)

    return render(request, 'update_profile.html', {'form': form})



def recuperar_contraseña(request):
    return render(request, 'recuperar_contraseña.html')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Articulos, Carrito, CarritoItem

@login_required

def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Articulos, id=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)

    if not created:
        carrito_item.cantidad += 1
    carrito_item.save()

    return redirect('ver_carrito')


@login_required
def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    producto = item.producto

    # Aumentar el stock del producto antes de eliminar el item del carrito
    producto.stock += item.cantidad
    producto.save()

    item.delete()
    return redirect('ver_carrito')


@login_required
def incrementar_cantidad(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    producto = item.producto

    if producto.stock > item.cantidad:
        item.cantidad += 1
        item.save()
    else:
        messages.error(request, f"No hay suficiente stock para {producto.nombre}")

    return redirect('ver_carrito')

@login_required
def decrementar_cantidad(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    else:
        item.delete()
    return redirect('ver_carrito')

@login_required(login_url='login')  # Redirigir a la página de login si no está autenticado
def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = CarritoItem.objects.filter(carrito=carrito)
    
    carrito_items = []
    total = 0
    
    for item in items:
        subtotal = item.producto.precio * item.cantidad
        total += subtotal
        carrito_items.append({
            'producto': item.producto,
            'cantidad': item.cantidad,
            'subtotal': subtotal,
            'id': item.id
        })
    
    return render(request, 'ver_carrito.html', {'items': carrito_items, 'total': total})

def my_view(request):
    carrito_items_count = 0
    if request.user.is_authenticated:
        carrito, created = Carrito.objects.get_or_create(usuario=request.user)
        carrito_items_count = CarritoItem.objects.filter(carrito=carrito).count()
    return render(request, 'mi_template.html', {'carrito_items_count': carrito_items_count})

@login_required
def comprar(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = CarritoItem.objects.filter(carrito=carrito)

    # Verificar stock antes de actualizar
    for item in items:
        producto = item.producto
        if producto.stock < item.cantidad:
            messages.error(request, f"No hay suficiente stock para {producto.nombre}")
            return redirect('ver_carrito')

    # Actualizar stock y vaciar carrito si hay suficiente stock
    for item in items:
        producto = item.producto
        producto.stock -= item.cantidad
        producto.save()

    # Vaciar el carrito después de la compra
    items.delete()

    messages.success(request, "Compra realizada con éxito")
    return redirect('ver_carrito')





from django.shortcuts import render
from .models import Carrito, CarritoItem



from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
# views.py
@csrf_exempt
@login_required
def guardar_direccion(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            direccion = data['direccion']

            if direccion == 'Av. Principal 123, Ciudad':
                precio_envio = 0  # Precio de envío para retiro en local
            else:
                usuario = request.user
                perfil_usuario = Usuario.objects.get(email=usuario.email)
                perfil_usuario.direccion = direccion
                perfil_usuario.save()

                # Buscar la comuna en la dirección
                comunas = Comuna.objects.all()
                comuna_nombre = None
                for comuna in comunas:
                    if comuna.nombre in direccion:
                        comuna_nombre = comuna.nombre
                        precio_envio = comuna.precio_envio
                        break

                if comuna_nombre is None:
                    return JsonResponse({'status': 'error', 'message': 'No Comuna matches the given query.'})

            # Guardar la dirección y el precio de envío en la sesión
            request.session['direccion'] = direccion
            request.session['precio_envio'] = precio_envio

            return JsonResponse({'status': 'success', 'precio_envio': precio_envio})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'})

    
 
    

@csrf_exempt
@login_required
def calcular_precio_envio(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            direccion = data['direccion']

            # Extraer la comuna de la dirección
            # Suponemos que la dirección está en el formato "Calle, Comuna, Ciudad, País"
            comuna_nombre = direccion.split(",")[1].strip()
            
            # Buscar la comuna en la base de datos
            comuna = get_object_or_404(Comuna, nombre=comuna_nombre)
            
            # Obtener el precio de envío
            precio_envio = comuna.precio_envio

            return JsonResponse({'status': 'success', 'precio_envio': precio_envio})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'})    
    

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Proveedor
from .forms import ProveedorForm

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_admin)
def proveedor_list(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'proveedor_list.html', {'proveedores': proveedores})

@login_required
@user_passes_test(is_admin)
def proveedor_add(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proveedor_list')
    else:
        form = ProveedorForm()
    return render(request, 'proveedor_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def proveedor_edit(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            return redirect('proveedor_list')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'proveedor_form.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def proveedor_delete(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('proveedor_list')
    return render(request, 'proveedor_confirm_delete.html', {'proveedor': proveedor})


# Clave de google maps api
# <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAUjMYm_HVdhncKSb4nvc8e4Br3-pbfbfc&callback=initMap&libraries=places" async defer></script>
# AIzaSyAUjMYm_HVdhncKSb4nvc8e4Br3-pbfbfc


from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor, ProductosProveedor
from .forms import ProductosProveedorForm

def agregar_producto_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id_proveedor=proveedor_id)
    if request.method == 'POST':
        form = ProductosProveedorForm(request.POST, request.FILES)
        if form.is_valid():
            producto_proveedor = form.save(commit=False)
            producto_proveedor.proveedor = proveedor
            producto_proveedor.save()
            return redirect('detalle_proveedor', proveedor_id=proveedor.id_proveedor)
    else:
        form = ProductosProveedorForm()
    return render(request, 'agregar_producto_proveedor.html', {'form': form, 'proveedor': proveedor})

def detalle_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id_proveedor=proveedor_id)
    productos = ProductosProveedor.objects.filter(proveedor=proveedor)
    return render(request, 'detalle_proveedor.html', {'proveedor': proveedor, 'productos': productos})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor, ProductosProveedor
from .forms import ProductosProveedorForm

def editar_producto_proveedor(request, producto_id):
    producto = get_object_or_404(ProductosProveedor, id=producto_id)
    if request.method == 'POST':
        form = ProductosProveedorForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('detalle_proveedor', proveedor_id=producto.proveedor.id_proveedor)
    else:
        form = ProductosProveedorForm(instance=producto)
    return render(request, 'editar_producto_proveedor.html', {'form': form, 'producto': producto})

def eliminar_producto_proveedor(request, producto_id):
    producto = get_object_or_404(ProductosProveedor, id=producto_id)
    proveedor_id = producto.proveedor.id_proveedor
    if request.method == 'POST':
        producto.delete()
        return redirect('detalle_proveedor', proveedor_id=proveedor_id)
    return render(request, 'eliminar_producto_proveedor.html', {'producto': producto})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Proveedor, ProductosProveedor

def comprar_productos_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id_proveedor=proveedor_id)
    productos = ProductosProveedor.objects.filter(proveedor=proveedor)
    return render(request, 'comprar_productos_proveedor.html', {'proveedor': proveedor, 'productos': productos})

from django.shortcuts import render, get_object_or_404, redirect
from .models import ProveedorCarrito, ProveedorCarritoItem, ProductosProveedor
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404, redirect
from .models import ProveedorCarrito, ProveedorCarritoItem, ProductosProveedor
from django.contrib.auth.decorators import login_required

@login_required
def comprar_producto(request, producto_id):
    producto = get_object_or_404(ProductosProveedor, id=producto_id)
    carrito, created = ProveedorCarrito.objects.get_or_create(usuario=request.user)
    item, item_created = ProveedorCarritoItem.objects.get_or_create(carrito=carrito, producto=producto)

    if not item_created:
        item.cantidad += 1
        item.save()

    return redirect('proveedor_carrito')



from django.shortcuts import render, get_object_or_404, redirect
from .models import ProveedorCarrito, ProveedorCarritoItem, ProductosProveedor
from django.contrib.auth.decorators import login_required

@login_required
def proveedor_carrito(request):
    carrito, created = ProveedorCarrito.objects.get_or_create(usuario=request.user)
    items = ProveedorCarritoItem.objects.filter(carrito=carrito)
    total = sum(item.producto.precio_costo * item.cantidad for item in items)
    return render(request, 'proveedor_carrito.html', {'carrito': carrito, 'items': items, 'total': total})

@login_required
def agregar_al_proveedor_carrito(request, producto_id):
    producto = get_object_or_404(ProductosProveedor, id=producto_id)
    carrito, created = ProveedorCarrito.objects.get_or_create(usuario=request.user)
    item, item_created = ProveedorCarritoItem.objects.get_or_create(carrito=carrito, producto=producto)

    if not item_created:
        item.cantidad += 1
        item.save()

    return redirect('proveedor_carrito')

@login_required
def eliminar_del_proveedor_carrito(request, item_id):
    item = get_object_or_404(ProveedorCarritoItem, id=item_id)
    item.delete()
    return redirect('proveedor_carrito')

@login_required
def aumentar_cantidad(request, item_id):
    item = get_object_or_404(ProveedorCarritoItem, id=item_id)
    item.cantidad += 1
    item.save()
    return redirect('proveedor_carrito')

@login_required
def disminuir_cantidad(request, item_id):
    item = get_object_or_404(ProveedorCarritoItem, id=item_id)
    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
    return redirect('proveedor_carrito')



from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ProveedorCarrito, ProveedorCarritoItem

@login_required
def resumen_compra(request):
    carrito, created = ProveedorCarrito.objects.get_or_create(usuario=request.user)
    items = ProveedorCarritoItem.objects.filter(carrito=carrito, en_resumen=True)  # Filtrar solo los productos en resumen
    total = sum(item.producto.precio_costo * item.cantidad for item in items)
    
    # Agrupar los productos por proveedor y calcular subtotales
    items_by_proveedor = {}
    subtotales_by_proveedor = {}
    for item in items:
        proveedor = item.producto.proveedor
        if proveedor not in items_by_proveedor:
            items_by_proveedor[proveedor] = []
            subtotales_by_proveedor[proveedor] = 0
        items_by_proveedor[proveedor].append(item)
        subtotales_by_proveedor[proveedor] += item.producto.precio_costo * item.cantidad
    
    return render(request, 'resumen_compra.html', {
        'items_by_proveedor': items_by_proveedor,
        'subtotales_by_proveedor': subtotales_by_proveedor,
        'total': total
    })


from fpdf import FPDF
from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ProveedorCarritoItem, Proveedor, ProveedorCarrito
from django.core.mail import EmailMessage
from django.conf import settings

def format_price(value):
    try:
        value = float(value)
        return "${:,.0f}".format(value).replace(',', '.')
    except (ValueError, TypeError):
        return value

class PDF(FPDF):
    def header(self):
        self.image('static/img/your_logo.png', 10, 8, 33)  # Ajusta la ruta a tu imagen
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Resumen de la Compra', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_table(self, items):
        self.set_font('Arial', 'B', 12)
        self.cell(60, 10, 'Producto', 1)
        self.cell(30, 10, 'Precio', 1)
        self.cell(30, 10, 'Cantidad', 1)
        self.cell(40, 10, 'Subtotal', 1)
        self.ln()

        self.set_font('Arial', '', 12)
        for item in items:
            self.cell(60, 10, item.producto.nombre_producto, 1)
            self.cell(30, 10, format_price(item.producto.precio_costo), 1)
            self.cell(30, 10, str(item.cantidad), 1)
            self.cell(40, 10, format_price(item.cantidad * item.producto.precio_costo), 1)
            self.ln()

    def add_total(self, subtotal):
        self.ln(10)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f"Subtotal: {format_price(subtotal)}", 0, 1, 'R')
@login_required
def descargar_pdf(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id_proveedor=proveedor_id)  # Usar id_proveedor en lugar de id
    carrito = get_object_or_404(ProveedorCarrito, usuario=request.user)
    items = ProveedorCarritoItem.objects.filter(carrito=carrito, producto__proveedor=proveedor)

    subtotal = sum(item.cantidad * item.producto.precio_costo for item in items)

    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title("Detalles del Proveedor")
    pdf.chapter_body(f"Nombre de la Empresa: {proveedor.nombre_empresa}")
    pdf.chapter_title("Detalles de los Productos")
    pdf.add_table(items)
    pdf.add_total(subtotal)

    pdf_buffer = BytesIO()
    pdf_buffer.write(pdf.output(dest='S').encode('latin1'))  # Generar el PDF y escribirlo en memoria como bytes
    pdf_buffer.seek(0)  # Reposicionar al inicio del buffer

    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="resumen_compra_proveedor_{proveedor_id}.pdf"'

    return response



from django.core.mail import EmailMessage
from django.conf import settings
from io import BytesIO
from fpdf import FPDF
from .models import ProveedorCarritoItem, Proveedor, ProveedorCarrito
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Resumen de la Compra', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_table(self, items):
        self.set_font('Arial', 'B', 12)
        self.cell(60, 10, 'Producto', 1)
        self.cell(30, 10, 'Precio', 1)
        self.cell(30, 10, 'Cantidad', 1)
        self.cell(40, 10, 'Subtotal', 1)
        self.ln()

        self.set_font('Arial', '', 12)
        for item in items:
            self.cell(60, 10, item.producto.nombre_producto, 1)
            self.cell(30, 10, f"${item.producto.precio_costo:,.2f}", 1)
            self.cell(30, 10, str(item.cantidad), 1)
            self.cell(40, 10, f"${item.cantidad * item.producto.precio_costo:,.2f}", 1)
            self.ln()

    def add_total(self, subtotal):
        self.ln(10)
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f"Subtotal: ${subtotal:,.2f}", 0, 1, 'R')


from io import BytesIO
from django.core.mail import EmailMessage
from django.conf import settings
from fpdf import FPDF
from .models import ProveedorCarritoItem, Proveedor, ProveedorCarrito
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def aceptar_producto(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id_proveedor=proveedor_id)
    carrito = get_object_or_404(ProveedorCarrito, usuario=request.user)
    items = ProveedorCarritoItem.objects.filter(carrito=carrito, producto__proveedor=proveedor)

    # Generar PDF
    pdf = PDF()
    pdf.add_page()
    pdf.chapter_title("Detalles del Proveedor")
    pdf.chapter_body(f"Nombre de la Empresa: {proveedor.nombre_empresa}")
    pdf.add_table(items)
    subtotal = sum(item.cantidad * item.producto.precio_costo for item in items)
    pdf.add_total(subtotal)

    pdf_buffer = BytesIO()
    pdf_buffer.write(pdf.output(dest='S').encode('latin1'))
    pdf_buffer.seek(0)

    # Enviar email con el PDF adjunto
    email = EmailMessage(
        'Resumen de la Compra',
        'Adjunto encontrará el resumen de la compra.',
        settings.DEFAULT_FROM_EMAIL,
        [proveedor.email_proveedor],
    )
    email.attach(f'resumen_compra_proveedor_{proveedor_id}.pdf', pdf_buffer.getvalue(), 'application/pdf')
    email.send()

    # Crear registros en RecepcionProducto y actualizar visibilidad en ProveedorCarritoItem
    for item in items:
        RecepcionProducto.objects.update_or_create(
            carrito_item=item,
            defaults={
                'cantidad_llegada': 0,  # Puedes ajustar según la lógica de negocio
                'confirmado': False,  # Suponiendo que inicialmente no está confirmado
                'estado': 'en_recepcion',  # Actualizamos el estado
                'precio_venta': 0.0,  # Valor por defecto para evitar errores
                'marca': item.producto.nombre_producto,  # Puedes ajustar este valor si tienes un campo específico para la marca
                'descripcion': item.producto.nombre_producto  # Puedes ajustar este valor si tienes un campo específico para la descripción
            }
        )
        item.en_resumen = False  # Oculta el ítem del resumen de compra sin borrarlo
        item.save()

    messages.success(request, 'Resumen de compra enviado por email exitosamente.')
    return redirect('proveedor_list')








from django.views.decorators.http import require_POST


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

@login_required
@require_POST
def rechazar_producto(request, item_id):
    item = get_object_or_404(ProveedorCarritoItem, id=item_id)
    item.delete()
    return JsonResponse({'success': True})




# views.py
from django.shortcuts import render, redirect
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions
from transbank.common.integration_type import IntegrationType
from transbank.error.transbank_error import TransbankError

def iniciar_pago(request):
    buy_order = str(uuid.uuid4())  # Generar una orden de compra única
    session_id = request.session.session_key
    amount = request.POST.get('total')  # Obtén el monto total desde el formulario
    return_url = request.build_absolute_uri('/webpay/retorno/')

    try:
        response = Transaction(WebpayOptions(IntegrationType.TEST, '597055555532')).create(
            buy_order=buy_order, session_id=session_id, amount=amount, return_url=return_url
        )
        return redirect(response['url'] + '?token_ws=' + response['token'])
    except TransbankError as e:
        print(e.message)
        return render(request, 'error.html', {'message': e.message})

def retorno_pago(request):
    token = request.GET.get('token_ws')
    if not token:
        return redirect('error')

    try:
        response = Transaction(WebpayOptions(IntegrationType.TEST, '597055555532')).commit(token=token)
        if response['status'] == 'AUTHORIZED':
            # Procesar la orden aquí
            return render(request, 'success.html', {'response': response})
        else:
            return render(request, 'error.html', {'message': 'Pago no autorizado'})
    except TransbankError as e:
        print(e.message)
        return render(request, 'error.html', {'message': e.message})


# menu/views.py

from django.shortcuts import render, redirect
from django.urls import reverse
from transbank.webpay.webpay_plus.transaction import Transaction, WebpayOptions, IntegrationCommerceCodes, IntegrationApiKeys
from transbank.common.integration_type import IntegrationType
from django.conf import settings
from django.contrib.auth.decorators import login_required
import uuid


@login_required
def venta_productos(request):
    if request.user.is_authenticated:
        try:
            # Obtener el perfil del usuario desde la base de datos
            perfil_usuario = Usuario.objects.get(email=request.user.email)
            direccion = perfil_usuario.direccion
        except Usuario.DoesNotExist:
            perfil_usuario = None
            direccion = ""
    else:
        return redirect('login')
    
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    items = CarritoItem.objects.filter(carrito=carrito)
    subtotal = sum(item.producto.precio * item.cantidad for item in items)
    iva = subtotal * 0.19  # Calcular el IVA (19%)
    total = subtotal + iva
    
    return render(request, 'venta_productos.html', {
        'items': items,
        'subtotal': subtotal,
        'iva': iva,
        'total': total,
        'direccion': direccion
    })


@login_required
def iniciar_pago(request):
    total = request.GET.get('total')
    if total is None:
        return redirect('venta_productos')  # Redirigir a la página de venta si no hay total

    total = int(total)  # Asegurarse de que el total sea un entero

    tx = Transaction(WebpayOptions(
        commerce_code=IntegrationCommerceCodes.WEBPAY_PLUS,
        api_key=IntegrationApiKeys.WEBPAY,
        integration_type=IntegrationType.TEST
    ))

    response = tx.create(
        buy_order='ordenDeCompra12345',  # Debes generar un buy_order único
        session_id='session123456',
        amount=total,
        return_url=request.build_absolute_uri(reverse('confirmar_pago'))
    )

    return redirect(f"{response['url']}?token_ws={response['token']}")

@login_required
def confirmar_pago(request):
    token = request.GET.get('token_ws')
    tx = Transaction(WebpayOptions(
        commerce_code=IntegrationCommerceCodes.WEBPAY_PLUS,
        api_key=IntegrationApiKeys.WEBPAY,
        integration_type=IntegrationType.TEST
    ))
    response = tx.commit(token)

    if response['status'] == 'AUTHORIZED':
        # Obtener el carrito y los items
        carrito = Carrito.objects.get(usuario=request.user)
        items = CarritoItem.objects.filter(carrito=carrito)

        # Calcular subtotal, IVA y total
        subtotal = sum(item.producto.precio * item.cantidad for item in items)
        iva = subtotal * 0.19  # Suponiendo que el IVA es del 19%
        total = subtotal + iva

        # Obtener la instancia de Usuario personalizada
        usuario = Usuario.objects.get(email=request.user.email)

        # Obtener la dirección y el precio de envío desde la sesión
        direccion_envio = request.session.get('direccion', '')
        precio_envio = request.session.get('precio_envio', 0)
        total += precio_envio  # Añadir el precio de envío al total

        # Crear el registro de Venta
        venta = Venta.objects.create(
            usuario=usuario,
            id_boleta=str(uuid.uuid4()),  # Generar un id_boleta único
            subtotal=subtotal,
            iva=iva,
            total=total
        )

        # Crear los registros de DetalleVenta
        for item in items:
            DetalleVenta.objects.create(
                venta=venta,
                articulo=item.producto,
                cantidad=item.cantidad,
                precio_unitario=item.producto.precio,
                total=item.producto.precio * item.cantidad
            )

            # Disminuir el stock del producto
            item.producto.stock -= item.cantidad
            item.producto.save()

        # Vaciar el carrito
        items.delete()

        # Almacenar los datos en la sesión
        request.session['response'] = {
            'buy_order': venta.id_boleta,  # Utilizar id_boleta en lugar de buy_order
            'transaction_date': response['transaction_date'],
            'amount': response['amount'],
            'status': response['status'],
            'authorization_code': response['authorization_code'],
            'payment_type_code': response['payment_type_code'],
            'vci': response['vci']
        }
        request.session['venta'] = {
            'id_boleta': venta.id_boleta,
            'nombre_usuario': usuario.nombre,
            'apellido_usuario': usuario.apellido,
            'subtotal': float(venta.subtotal),
            'iva': float(venta.iva),
            'total': float(venta.total),
            'direccion_envio': direccion_envio,
            'precio_envio': float(precio_envio),
            'productos': [
                {
                    'nombre': detalle.articulo.nombre,
                    'cantidad': detalle.cantidad,
                    'precio_unitario': float(detalle.precio_unitario),
                    'total': float(detalle.total)
                } for detalle in venta.detalleventa_set.all()
            ]
        }

        # Redirigir a la página de éxito
        return redirect('pago_exitoso')
    else:
        return render(request, 'pago_fallido.html', {'response': response})




@login_required
def pago_exitoso(request):
    response = request.session.get('response')
    venta = request.session.get('venta')

    if not response or not venta:
        return redirect('venta_productos')  # Redirigir si no hay datos en la sesión

    return render(request, 'pago_exitoso.html', {
        'response': response,
        'venta': venta,
        'nombre_usuario': venta['nombre_usuario'],
        'apellido_usuario': venta['apellido_usuario']
    })


from fpdf import FPDF
from django.http import HttpResponse


class PDFFF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Boleta de Venta', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_detail(self, label, value):
        self.set_font('Arial', '', 12)
        self.cell(0, 10, f'{label}: {value}', 0, 1, 'L')

def format_price(price):
    return f"${price:,.0f}".replace(",", ".")

@login_required
def generar_pdf(request):
    venta = request.session.get('venta')
    response = request.session.get('response')

    if not response or not venta:
        return redirect('venta_productos')

    pdf = PDFFF()
    pdf.add_page()

    # Detalles de la transacción
    pdf.chapter_title("Detalles de la Transacción")
    pdf.add_detail("Orden de Compra", venta['id_boleta'])
    pdf.add_detail("Fecha de Transacción", response['transaction_date'])
    pdf.add_detail("Monto Total", format_price(venta['total']))

    # Detalles de la venta
    pdf.chapter_title("Detalles de la Venta")
    pdf.add_detail("ID Boleta", venta['id_boleta'])
    pdf.add_detail("Nombre del Cliente", f"{venta['nombre_usuario']} {venta['apellido_usuario']}")
    if venta['direccion_envio'] == "Av. Principal 123, Ciudad":
        pdf.add_detail("Dirección del Local", venta['direccion_envio'])
    else:
        pdf.add_detail("Dirección de Envío", venta['direccion_envio'])

    # Totales
    pdf.chapter_title("Totales")
    pdf.add_detail("Subtotal", format_price(venta['subtotal']))
    pdf.add_detail("IVA", format_price(venta['iva']))
    pdf.add_detail("Precio de Envío", format_price(venta['precio_envio']))
    pdf.add_detail("Total", format_price(venta['total']))

    # Productos comprados
    pdf.chapter_title("Productos Comprados")
    for producto in venta['productos']:
        pdf.multi_cell(0, 10, f"{producto['nombre']} - {producto['cantidad']} x {format_price(producto['precio_unitario'])}")

    # Guardar el PDF en un BytesIO buffer
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    
    # Crear la respuesta HTTP con el PDF
    response = HttpResponse(pdf_buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Boleta_{venta["id_boleta"]}.pdf"'
    
    return response



from django.core.mail import EmailMessage

@login_required
def enviar_pdf(request):
    venta = request.session.get('venta')
    response = request.session.get('response')

    if not response or not venta:
        return redirect('venta_productos')

    pdf = PDFFF()
    pdf.add_page()

    # Detalles de la transacción
    pdf.chapter_title("Detalles de la Transacción")
    pdf.add_detail("Orden de Compra", venta['id_boleta'])
    pdf.add_detail("Fecha de Transacción", response['transaction_date'])
    pdf.add_detail("Monto Total", format_price(venta['total']))

    # Detalles de la venta
    pdf.chapter_title("Detalles de la Venta")
    pdf.add_detail("ID Boleta", venta['id_boleta'])
    pdf.add_detail("Nombre del Cliente", f"{venta['nombre_usuario']} {venta['apellido_usuario']}")
    if venta['direccion_envio'] == "Av. Principal 123, Ciudad":
        pdf.add_detail("Dirección del Local", venta['direccion_envio'])
    else:
        pdf.add_detail("Dirección de Envío", venta['direccion_envio'])

    # Totales
    pdf.chapter_title("Totales")
    pdf.add_detail("Subtotal", format_price(venta['subtotal']))
    pdf.add_detail("IVA", format_price(venta['iva']))
    pdf.add_detail("Precio de Envío", format_price(venta['precio_envio']))
    pdf.add_detail("Total", format_price(venta['total']))

    # Productos comprados
    pdf.chapter_title("Productos Comprados")
    for producto in venta['productos']:
        pdf.multi_cell(0, 10, f"{producto['nombre']} - {producto['cantidad']} x {format_price(producto['precio_unitario'])}")

    # Guardar el PDF en un BytesIO buffer
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    
    # Crear el correo electrónico
    email = EmailMessage(
        'Boleta de Venta',
        'Estimado/a cliente,\n\nGracias por su compra en nuestra tienda. Adjuntamos a este correo la boleta de su compra.\n\nSi tiene alguna pregunta o necesita más información, no dude en contactarnos.\n\nSaludos cordiales,\n\nEl equipo de SpaceTech',
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email],  # Enviar al email del usuario logueado
    )
    email.attach(f'Boleta_{venta["id_boleta"]}.pdf', pdf_buffer.getvalue(), 'application/pdf')
    
    try:
        # Enviar el correo
        email.send()
        messages.success(request, 'Boleta enviada por email exitosamente.')
    except Exception as e:
        messages.error(request, f'Error al enviar el email: {e}')
    
    return redirect('pago_exitoso')



from django.contrib.auth.views import PasswordResetConfirmView

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'

from django.db.models import Q
def gestion_ventas(request):
    query = request.GET.get('q')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')

    ventas = Venta.objects.select_related('usuario').all()

    if query:
        ventas = ventas.filter(Q(usuario__nombre_usuario__icontains=query) | Q(id_boleta__icontains=query))

    if date_from:
        ventas = ventas.filter(fecha__gte=date_from)

    if date_to:
        ventas = ventas.filter(fecha__lte=date_to)

    context = {'ventas': ventas}
    return render(request, 'gestion_ventas.html', context)

def detalle_venta_ajax(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)
    html = render_to_string('detalle_venta_ajax.html', {'venta': venta, 'detalles': detalles})
    return HttpResponse(html)

def detalle_venta_ajax(request, venta_id):
    venta = get_object_or_404(Venta, id=venta_id)
    detalles = DetalleVenta.objects.filter(venta=venta)
    html = render_to_string('detalle_venta_ajax.html', {'venta': venta, 'detalles': detalles})
    return HttpResponse(html)

from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST
from .models import ProveedorCarritoItem
from django.contrib.auth.decorators import login_required

@login_required
@require_POST
def actualizar_cantidad_llegada(request):
    for key, value in request.POST.items():
        if key.startswith('cantidad_llegada_'):
            item_id = key.split('_')[-1]
            cantidad_llegada = int(value)
            item = get_object_or_404(ProveedorCarritoItem, id=item_id)
            item.cantidad_llegada = cantidad_llegada
            item.save()
    return redirect('recepcion_proveedor')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ProveedorCarritoItem, Proveedor

@login_required
def recepcion_proveedor(request):
    recepciones = RecepcionProducto.objects.filter(
        carrito_item__carrito__usuario=request.user
    ).select_related('carrito_item__producto', 'carrito_item__producto__proveedor')

    return render(request, 'recepcion_proveedor.html', {'recepciones': recepciones})

from django.http import JsonResponse
from .models import RecepcionProducto

def buscar_marca(request):
    if request.is_ajax() and 'term' in request.GET:
        qs = RecepcionProducto.objects.filter(marca__icontains=request.GET.get('term')).distinct()
        marcas = list(qs.values_list('marca', flat=True))
        return JsonResponse(marcas, safe=False)
    return JsonResponse([], safe=False)

from django.shortcuts import redirect
from .models import RecepcionProducto


from django.shortcuts import render, redirect
from .models import RecepcionProducto
from django.contrib.auth.decorators import login_required
from django.contrib import messages





@login_required
def publicar_productos(request):
    if request.method == 'POST':
        for item in RecepcionProducto.objects.filter(carrito_item__carrito__usuario=request.user, estado='en_recepcion'):
            item_id_str = str(item.id)
            cantidad_llegada = request.POST.get(f'cantidad_llegada_{item_id_str}')
            precio_venta = request.POST.get(f'precio_venta_{item_id_str}')
            marca = request.POST.get(f'marca_{item_id_str}')
            descripcion = request.POST.get(f'descripcion_{item_id_str}')
            publicar = request.POST.get(f'publicar_{item_id_str}')

            item.cantidad_llegada = int(cantidad_llegada) if cantidad_llegada else item.cantidad_llegada
            item.precio_venta = float(precio_venta) if precio_venta else item.precio_venta
            item.marca = marca if marca else item.marca
            item.descripcion = descripcion if descripcion else item.descripcion

            if publicar == 'true':
                if item.cantidad_llegada >= 1:
                    item.estado = 'publicado'
                    item.save()
                else:
                    messages.error(request, f'El producto {item.carrito_item.producto.nombre_producto} debe tener al menos 1 en cantidad llegada para ser publicado.')

        return redirect('recepcion_proveedor')
    else:
        return redirect('recepcion_proveedor')