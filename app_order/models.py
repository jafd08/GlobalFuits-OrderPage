from django.db import models

# Create your models here.
from django.db.models import Sum
from django.conf import settings
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_delete
import datetime
# import pytz
from django.utils import timezone
from app_product.models import Product
from app_accounts.models import Profile

from decimal import Decimal

CURRENCY = settings.CURRENCY

def returnSTRcurrency( int_var ):
    toStr = str(int_var)
    return toStr + " " + CURRENCY
class OrderManager(models.Manager):

    def active(self):
        return self.filter(active=True)


class Status(models.Model):
    name = models.CharField(max_length=150, unique=True,
                            null=False, default="Abierto")

    class Meta:
        verbose_name_plural = 'Estados'

    def __str__(self):
        return self.name


DEFAULT_REQUESTOR_ID = 1


class Order(models.Model):
    date = models.DateField("Fecha Entrega", default=timezone.now)
    requestor = models.ForeignKey(
        Profile, on_delete=models.CASCADE, default=DEFAULT_REQUESTOR_ID, verbose_name="Comprador")
    title = models.CharField("Titulo Nuevo Pedido", max_length=150)
    timestamp = models.DateField(auto_now_add=True)
    created = models.DateTimeField("Fecha Orden Creada", editable=False)
    value = models.DecimalField(default=0.00, decimal_places=2, max_digits=20)
    discount = models.DecimalField(
        default=0.00, decimal_places=2, max_digits=20, verbose_name="Descuento")
    final_value = models.DecimalField(
        "precio", default=0.00, decimal_places=2, max_digits=20)
    is_paid = models.BooleanField(default=False, verbose_name="Esta Pagado")
    comments = models.CharField(
        "Comentarios", max_length=200, null=True, default="No hay comentarios")
    status = models    .ForeignKey(
        Status, null=False, default=1, on_delete=models.PROTECT, verbose_name="Estado Orden")
    objects = models.Manager()
    browser = OrderManager()

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        order_items = self.order_items.all()
        self.value = order_items.aggregate(Sum('total_price'))[
            'total_price__sum'] if order_items.exists() else 0.00
        self.final_value = Decimal(self.value) - Decimal(self.discount)
        if not self.id:
            self.created = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title if self.title else 'New Order'

    def get_edit_url(self):
        return reverse('update_order', kwargs={'pk': self.id})

    def client_get_edit_url(self):
        return reverse('client_update_order', kwargs={'pk': self.id})

    def get_delete_url(self):
        return reverse('delete_order', kwargs={'pk': self.id})

    def tag_final_value(self):
        return returnSTRcurrency(self.final_value)
        #return str(self.final_value) + " " + CURRENCY

    def tag_discount(self):
        return returnSTRcurrency(self.discount)

    def tag_value(self):
        return returnSTRcurrency(self.value)

    @staticmethod
    def filter_data(request, queryset):
        search_name = request.GET.get('search_name', None)
        date_start = request.GET.get('date_start', None)
        date_end = request.GET.get('date_end', None)
        queryset = queryset.filter(
            title__contains=search_name) if search_name else queryset
        if date_end and date_start and date_end >= date_start:
            date_start = datetime.datetime.strptime(
                date_start, '%m/%d/%Y').strftime('%Y-%m-%d')
            date_end = datetime.datetime.strptime(
                date_end, '%m/%d/%Y').strftime('%Y-%m-%d')
            print(date_start, date_end)
            queryset = queryset.filter(date__range=[date_start, date_end])
        return queryset


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, verbose_name="Nombre")
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_items')
    qty = models.DecimalField("Cantidad/Kg", default=1,
                              decimal_places=2, max_digits=20)
    price = models.DecimalField(
        "Precio", default=0.00, decimal_places=2, max_digits=20)
    discount_price = models.DecimalField(
        default=0.00, decimal_places=2, max_digits=20)
    final_price = models.DecimalField(
        default=0.00, decimal_places=2, max_digits=20)
    total_price = models.DecimalField(
        "Total", default=0.00, decimal_places=2, max_digits=20)

    def __str__(self):
        return self.product.title

    def save(self, *args, **kwargs):
        self.final_price = self.discount_price if self.discount_price > 0 else self.price
        self.total_price = Decimal(self.qty) * Decimal(self.final_price)
        super().save(*args, **kwargs)
        self.order.save()

    def tag_final_price(self):
        return returnSTRcurrency(self.final_price)

    def tag_discount(self):
        return returnSTRcurrency(self.discount_price)

    def tag_price(self):
        return returnSTRcurrency(self.price)


    def total_price_return(self):
        return returnSTRcurrency(self.total_price)



@receiver(post_delete, sender=OrderItem)
def delete_order_item(sender, instance, **kwargs):
    product = instance.product
    product.qty += instance.qty
    product.save()
    instance.order.save()
