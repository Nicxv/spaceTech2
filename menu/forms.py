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

from .models import Proveedor

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'


from .models import Producto
from django import forms
from .models import Producto
from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_producto', 'foto_producto', 'precio_costo']
        widgets = {
            'foto_producto': forms.FileInput(),  # Asegura que se use el widget correcto para la carga de archivos
        }




from django import forms
from .models import Producto
from django import forms
from .models import Producto
from django import forms
from .models import Producto

class ProductoInventarioForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['stock_actual', 'stock_minimo', 'precio_venta']