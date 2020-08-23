import django_tables2 as tables

from app_product.models import Product
from app_order.models import OrderItem, Order

import django_tables2 as tables

from app_product.models import Product
from app_order.models import OrderItem, Order


class OrderTable(tables.Table):
    tag_final_value = tables.Column(orderable=False, verbose_name='Precio')
    action = tables.TemplateColumn(
        '<a href="{{ record.client_get_edit_url }}" class="btn btn-info"><i class="fa fa-edit"></i></a>', orderable=False)

    class Meta:
        model = Order
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'title', 'tag_final_value']


class ProductTable(tables.Table):
    tag_final_value = tables.Column(orderable=False, verbose_name='Precio')
    accion = tables.TemplateColumn(
        '<button class="btn btn-info add_button" data-href="{% url "client_ajax_add" instance.id record.id %}">Añadir!</a>',
        orderable=False
    )

    class Meta:
        model = Product
        template_name = 'django_tables2/bootstrap.html'
        fields = ['title', 'category','unidad_o_kg', 'tag_final_value']




class OrderItemTable(tables.Table):
    TEMPLATE = """
    <input  onfocusout="update_price_quantity(this)"  style="width:40%" maxlength="5" name="qty" type="text" class="modify_qty" data-href="{% url "client_ajax_input_modify" record.id "modify" 0 %}"/>
    """
    tag_final_price = tables.Column(orderable=False, verbose_name='Precio')
    qty_input = tables.TemplateColumn(TEMPLATE, verbose_name=' ',orderable=False)
    acción = tables.TemplateColumn('''
            <button data-href="{% url "client_ajax_modify" record.id "add" %}" class="btn btn-success edit_button"><i class="fa fa-arrow-up"></i></button>
            <button data-href="{% url "client_ajax_modify" record.id "remove" %}" class="btn btn-warning edit_button"><i class="fa fa-arrow-down"></i></button>
            <button data-href="{% url "client_ajax_modify" record.id "delete" %}" class="btn btn-danger edit_button"><i class="fa fa-trash"></i></button>
    ''', orderable=False)

    class Meta:
        model = OrderItem
        template_name = 'django_tables2/bootstrap.html'
        fields = ['product', 'product.category', 'tag_final_price','product.unidad_o_kg' ,'qty']