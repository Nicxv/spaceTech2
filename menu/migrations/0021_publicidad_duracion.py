# Generated by Django 5.0.4 on 2024-07-03 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0020_publicidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicidad',
            name='duracion',
            field=models.IntegerField(default=5),
        ),
    ]
