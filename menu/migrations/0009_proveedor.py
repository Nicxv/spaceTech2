# Generated by Django 5.0.4 on 2024-07-01 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0008_delete_proveedor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id_proveedor', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('rut_empresa', models.CharField(max_length=13, verbose_name='RUT de la Empresa')),
                ('nombre_empresa', models.CharField(max_length=100, verbose_name='Nombre de la Empresa')),
                ('representante_legal', models.CharField(default='', max_length=100, verbose_name='Representante Legal')),
                ('contacto_empresa', models.CharField(max_length=50, verbose_name='Contacto de la Empresa')),
                ('direccion_proveedor', models.CharField(default='sin direccion', max_length=255, verbose_name='Dirección')),
                ('email_proveedor', models.EmailField(blank=True, max_length=70, null=True, unique=True)),
            ],
        ),
    ]
