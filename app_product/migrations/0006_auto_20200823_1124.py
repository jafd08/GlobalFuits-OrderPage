# Generated by Django 2.2.5 on 2020-08-23 17:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_product', '0005_auto_20200802_2155'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categorias'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': 'Productos'},
        ),
    ]
