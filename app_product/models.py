from django.db import models
from django.conf import settings
from .managers import ProductManager

CURRENCY = settings.CURRENCY


class Category(models.Model):
    title = models.CharField(max_length=150, unique=True,null=False)

    class Meta:
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.title


class Measure(models.Model):
    title = models.CharField(max_length=150, unique=True,null=False)

    class Meta:
        verbose_name_plural = 'Medidas'

    def __str__(self):
        return self.title


class Product(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField( max_length=150, unique=True, verbose_name="Producto")
    category = models.ForeignKey(Category, null=False,default=1, on_delete=models.PROTECT, verbose_name="Categoria")
    value = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, verbose_name="Precio")
    measure = models.ForeignKey(Measure, null=False,default=1, on_delete=models.PROTECT, verbose_name="Medida")
    discount_value = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    final_value = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
    qty = models.PositiveIntegerField(default=0)

    objects = models.Manager()
    broswer = ProductManager()

    class Meta:
        verbose_name_plural = 'Productos'

    def save(self, *args, **kwargs):
        self.final_value = self.discount_value if self.discount_value > 0 else self.value
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def tag_final_value(self):
        return f'{self.final_value}{CURRENCY}'
    tag_final_value.short_description = 'Valor'


