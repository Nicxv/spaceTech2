# Generated by Django 5.0.4 on 2024-07-03 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0019_remove_detalleventa_articulo_detalleventa_producto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publicidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='publicidad/')),
                ('segundos', models.PositiveIntegerField()),
                ('activa', models.BooleanField(default=True)),
            ],
        ),
    ]
