from django.urls import path
from django.conf.urls.static import static
from spacetech import settings
from . import views
from django.urls import path
from .views import CustomPasswordResetConfirmView,  detalle_producto, enviar_publicidad
from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import path
from .views import proveedor_list, proveedor_add, proveedor_edit, proveedor_delete, iniciar_pago, confirmar_pago,buscar_marca
from .views import actualizar_cantidad_llegada, recepcion_proveedor

urlpatterns = [
    path('', views.home_view, name='home'),
    path('menu', views.menu, name='menu'),

    path('busqueda_productos/', views.busqueda_productos),
    path('buscar/', views.buscar),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('agregarP', views.agregar_producto, name='agregarP'),
    path('update-profile/', views.update_profile_view, name='update_profile'),

    path('formulario', views.formulario, name='formulario'),
    path('listaU', views.listaU, name='listaU'),
    path('listaP', views.listaP, name='listaP'),
    path('publicidad', enviar_publicidad, name='publicidad'),

    path('listaU/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('listaU/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('listaP/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('listaP/modificar/<int:producto_id>/', views.modificarP, name='modificarP'),
    
    path('detalle_producto/<int:producto_id>/', detalle_producto, name='detalle_producto'),



    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar_del_carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('incrementar_cantidad/<int:item_id>/', views.incrementar_cantidad, name='incrementar_cantidad'),
    path('decrementar_cantidad/<int:item_id>/', views.decrementar_cantidad, name='decrementar_cantidad'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),


    path('recuperar_contraseña/', auth_views.PasswordResetView.as_view(template_name='recuperar_contraseña.html'), name='password_reset'),
    path('recuperar_contraseña/enviado/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('recuperar_contraseña/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('recuperar_contraseña/completo/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
   
   
    path('comprar/', views.comprar, name='comprar'),


    


    path('venta_productos/', views.venta_productos, name='venta_productos'),
    path('guardar_direccion/', views.guardar_direccion, name='guardar_direccion'),





    path('proveedores/', proveedor_list, name='proveedor_list'),
    path('proveedor/add/', proveedor_add, name='proveedor_add'),
    path('proveedor/edit/<int:pk>/', proveedor_edit, name='proveedor_edit'),
    path('proveedor/delete/<int:pk>/', proveedor_delete, name='proveedor_delete'),

    path('proveedor/<int:proveedor_id>/', views.detalle_proveedor, name='detalle_proveedor'),
    path('proveedor/<int:proveedor_id>/agregar_producto/', views.agregar_producto_proveedor, name='agregar_producto_proveedor'),
    path('producto/<int:producto_id>/editar/', views.editar_producto_proveedor, name='editar_producto_proveedor'),
    path('producto/<int:producto_id>/eliminar/', views.eliminar_producto_proveedor, name='eliminar_producto_proveedor'),
    path('proveedor/<int:proveedor_id>/comprar_productos/', views.comprar_productos_proveedor, name='comprar_productos_proveedor'),
    path('producto/<int:producto_id>/comprar/', views.comprar_producto, name='comprar_producto'),



    path('proveedor_carrito/', views.proveedor_carrito, name='proveedor_carrito'),
    path('proveedor_carrito/agregar/<int:producto_id>/', views.agregar_al_proveedor_carrito, name='agregar_al_proveedor_carrito'),
    path('proveedor_carrito/eliminar/<int:item_id>/', views.eliminar_del_proveedor_carrito, name='eliminar_del_proveedor_carrito'),
    path('proveedor_carrito/aumentar/<int:item_id>/', views.aumentar_cantidad, name='aumentar_cantidad'),
    path('proveedor_carrito/disminuir/<int:item_id>/', views.disminuir_cantidad, name='disminuir_cantidad'),
    path('resumen_compra/', views.resumen_compra, name='resumen_compra'),
    path('aceptar_producto/<int:proveedor_id>/', views.aceptar_producto, name='aceptar_producto'),
    path('rechazar_producto/<int:item_id>/', views.rechazar_producto, name='rechazar_producto'),
    path('descargar_pdf/<int:proveedor_id>/', views.descargar_pdf, name='descargar_pdf'),


    path('webpay/iniciar/', views.iniciar_pago, name='iniciar_pago'),
    path('webpay/retorno/', views.retorno_pago, name='retorno_pago'),

    path('iniciar_pago/', iniciar_pago, name='iniciar_pago'),
    path('confirmar_pago/', confirmar_pago, name='confirmar_pago'),
    path('pago_exitoso/', views.pago_exitoso, name='pago_exitoso'),

    path('generar_pdf/', views.generar_pdf, name='generar_pdf'),
    path('enviar_pdf/', views.enviar_pdf, name='enviar_pdf'),

    path('gestion_ventas/', views.gestion_ventas, name='gestion_ventas'),
    path('detalle_venta_ajax/<int:venta_id>/', views.detalle_venta_ajax, name='detalle_venta_ajax'),    
    
    path('recepcion_proveedor/', recepcion_proveedor, name='recepcion_proveedor'),
    path('actualizar_cantidad_llegada/', actualizar_cantidad_llegada, name='actualizar_cantidad_llegada'),

    path('buscar_marca/', buscar_marca, name='buscar_marca'),
    

    path('publicar_productos/', views.publicar_productos, name='publicar_productos'),
    
]

# Clave de google maps api
# <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAUjMYm_HVdhncKSb4nvc8e4Br3-pbfbfc&callback=initMap&libraries=places" async defer></script>
# AIzaSyAUjMYm_HVdhncKSb4nvc8e4Br3-pbfbfc
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
