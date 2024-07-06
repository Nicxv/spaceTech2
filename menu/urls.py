from django.urls import path
from django.conf.urls.static import static
from spacetech import settings
from . import views
from django.urls import path
from .views import CustomPasswordResetConfirmView, actualizar_stock,  add_to_cart, checkout, crear_producto, crear_proveedor, decrement_quantity, descargar_pdf2, editar_proveedor, editar_publicidad, eliminar_proveedor, eliminar_publicidad, eliminar_solicitud_view,  enviar_publicidad, formulario_img, increment_quantity, inventario, listar_publicidades, publicar_solicitud_view,   remove_from_cart, remover_de_home, solicitud_publicidad_view, subir_a_home, transbank_response_publicidad,  ver_productos_proveedor, ver_solicitudes_view, view_cart
from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import path
from .views import  iniciar_pago, confirmar_pago


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
    

    path('listaU/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('listaU/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('listaP/eliminar/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path('listaP/modificar/<int:producto_id>/', views.modificarP, name='modificarP'),
    
    
    
    
  



    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar_del_carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('incrementar_cantidad/<int:item_id>/', views.incrementar_cantidad, name='incrementar_cantidad'),
    path('decrementar_cantidad/<int:item_id>/', views.decrementar_cantidad, name='decrementar_cantidad'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),

    path('comprar/', views.comprar, name='comprar'),

    path('venta_productos/', views.venta_productos, name='venta_productos'),
    path('guardar_direccion/', views.guardar_direccion, name='guardar_direccion'),



    path('webpay/iniciar/', views.iniciar_pago, name='iniciar_pago'),
    path('webpay/retorno/', views.retorno_pago, name='retorno_pago'),

    path('iniciar_pago/', iniciar_pago, name='iniciar_pago'),
    path('confirmar_pago/', confirmar_pago, name='confirmar_pago'),
    path('pago_exitoso/', views.pago_exitoso, name='pago_exitoso'),

    path('generar_pdf/', views.generar_pdf, name='generar_pdf'),
    path('enviar_pdf/', views.enviar_pdf, name='enviar_pdf'),

    path('gestion_ventas/', views.gestion_ventas, name='gestion_ventas'),
    path('detalle_venta_ajax/<int:venta_id>/', views.detalle_venta_ajax, name='detalle_venta_ajax'),    
    
    


   
    path('crear_proveedor/', views.crear_proveedor, name='crear_proveedor'),
    path('listar_proveedores/', views.listar_proveedores, name='listar_proveedores'),
    
   
    path('proveedor/eliminar/<int:id>/', eliminar_proveedor, name='eliminar_proveedor'),
    path('proveedor/editar/<int:id>/', editar_proveedor, name='editar_proveedor'),
    path('proveedor/<int:proveedor_id>/nuevo-producto/', crear_producto, name='crear_producto'),
    path('proveedor/<int:proveedor_id>/productos/', ver_productos_proveedor, name='ver_productos_proveedor'),
    
    path('producto/<int:producto_id>/añadir-al-carrito/', views.añadir_al_carrito, name='añadir_al_carrito'),   
    path('proveedor/<int:proveedor_id>/actualizar_carrito/', views.actualizar_carrito, name='actualizar_carrito'),

    path('proveedor/<int:proveedor_id>/crear_compra/', views.crear_compra, name='crear_compra'),
    path('compra/recepcion/', views.recepcion_compra, name='recepcion_compra'),
    path('compra/eliminar/<uuid:compra_id>/', views.eliminar_compra, name='eliminar_compra'),

    path('compra/<uuid:compra_id>/descargar_pdf2/', descargar_pdf2, name='descargar_pdf2'),

   
    path('inventario/', views.inventario, name='inventario'),
     path('subir_a_home/<int:producto_id>/', subir_a_home, name='subir_a_home'),
     path('remover_de_home/<int:producto_id>/', remover_de_home, name='remover_de_home'),
    path('producto/<int:id_producto>/', views.detalle_producto_view, name='detalle_producto'),




    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('increment_quantity/<int:item_id>/', increment_quantity, name='increment_quantity'),
    path('decrement_quantity/<int:item_id>/', decrement_quantity, name='decrement_quantity'),
    path('cart/', view_cart, name='view_cart'),
    path('checkout/', checkout, name='checkout'),
    
    path('transbank_response/', views.transbank_response, name='transbank_response'),
    path('purchase_success/', views.purchase_success, name='purchase_success'),
    path('cambiar_estado_venta/', views.cambiar_estado_venta, name='cambiar_estado_venta'),

    path('formulario_img/', formulario_img, name='formulario_img'),
    

    path('publicidades/', listar_publicidades, name='listar_publicidades'),
    path('publicidades/editar/<int:publicidad_id>/', editar_publicidad, name='editar_publicidad'),
    path('publicidades/eliminar/<int:publicidad_id>/', eliminar_publicidad, name='eliminar_publicidad'),

    path('solicitud_publicidad/', solicitud_publicidad_view, name='solicitud_publicidad'),
    path('ver_solicitudes/', ver_solicitudes_view, name='ver_solicitudes'),
    path('eliminar_solicitud/<int:id>/', eliminar_solicitud_view, name='eliminar_solicitud'),

    path('solicitud_publicidad/', solicitud_publicidad_view, name='solicitud_publicidad'),
    path('transbank_response_publicidad/', transbank_response_publicidad, name='transbank_response_publicidad'),
    path('publicar_solicitud/<int:id>/', publicar_solicitud_view, name='publicar_solicitud'),
    path('search/', views.search_view, name='search'),
    path('actualizar_stock/<uuid:compra_id>/', actualizar_stock, name='actualizar_stock'),
     
]



# Clave de google maps api
# <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAUjMYm_HVdhncKSb4nvc8e4Br3-pbfbfc&callback=initMap&libraries=places" async defer></script>
# AIzaSyAUjMYm_HVdhncKSb4nvc8e4Br3-pbfbfc
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
