# Generated by Django 5.0.4 on 2024-07-01 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_remove_proveedorcarrito_usuario_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DetalleCompra',
        ),
    ]
