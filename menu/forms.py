from django import forms
from . models import Articulos, Usuario


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre_usuario', 'nombre', 'apellido', 'email', 'tfno', 'clave', 'confirmar_clave', 'direccion']
        widgets = {
            'clave': forms.PasswordInput(),
            'confirmar_clave': forms.PasswordInput(),
        }
        
class Usuario2Form(forms.ModelForm):
    role = forms.ChoiceField(choices=Usuario.ROLE_CHOICES, label="Rol")

    class Meta:
        model = Usuario
        fields = [
            'nombre_usuario',
            'nombre',
            'apellido',
            'tfno',
            'role'
        ]

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre_usuario', 'nombre', 'apellido', 'tfno', 'direccion']        
        
class ArticulosForm(forms.ModelForm):
    class Meta:
        model = Articulos
        fields =[
            'nombre',
            'descripcion',
            'precio',
            'stock',
            'foto',
            'marca',
            'precio_oferta',
            'descuento',
           
        ]
    def clean(self):
        cleaned_data = super().clean()
        precio = cleaned_data.get('precio')
        descuento = cleaned_data.get('descuento')

        if precio and descuento:
            cleaned_data['precio_oferta'] = precio - (precio * (descuento / 100))

        return cleaned_data    


from django import forms





from django import forms
from .models import Articulos
from django.forms.models import inlineformset_factory

class ArticulosForm(forms.ModelForm):
    class Meta:
        model = Articulos
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'foto', 'marca', 'precio_oferta', 'descuento']



        
class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))   

from django import forms
from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['rut_empresa', 'nombre_empresa', 'representante_legal', 'contacto_empresa', 'direccion_proveedor', 'email_proveedor']

from django import forms
from .models import ProductosProveedor

class ProductosProveedorForm(forms.ModelForm):
    class Meta:
        model = ProductosProveedor
        fields = ['nombre_producto', 'foto_producto', 'precio_costo']
        widgets = {
            'nombre_producto': forms.TextInput(attrs={'class': 'form-control'}),
            'foto_producto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'precio_costo': forms.NumberInput(attrs={'class': 'form-control'}),
        }

from django import forms
from .models import RecepcionProducto, ProveedorCarritoItem
class RecepcionProductoForm(forms.ModelForm):
    class Meta:
        model = RecepcionProducto
        fields = ['cantidad_llegada', 'precio_venta', 'marca', 'descripcion']
        widgets = {
            'cantidad_llegada': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control'}),
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(RecepcionProductoForm, self).__init__(*args, **kwargs)
        # Asigna valores iniciales o ajusta comportamientos aquí si es necesario

    def clean_precio_venta(self):
        precio_venta = self.cleaned_data.get('precio_venta')
        if precio_venta is None:
            raise forms.ValidationError("El precio de venta no puede estar vacío.")
        return precio_venta