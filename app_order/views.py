from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, reverse
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Sum
from django_tables2 import RequestConfig
from .models import Order, OrderItem, CURRENCY
from .forms import OrderCreateForm, OrderEditForm
from app_product.models import Product
from .tables import ProductTable, OrderItemTable, OrderTable
from app_accounts.models import Profile
from django.contrib.auth.models import User


import datetime

def returnSTRcurrency(int_var):
    toStr = str(int_var)
    return CURRENCY  + " " + toStr  

@method_decorator(staff_member_required, name='dispatch')
class HomepageView(ListView):
    template_name = 'index.html'
    model = Order
    queryset = Order.objects.all()[:10]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = Order.objects.all()
        total_sales = orders.aggregate(Sum('final_value'))[
            'final_value__sum'] if orders.exists() else 0
        paid_value = orders.filter(is_paid=True).aggregate(Sum('final_value'))['final_value__sum']\
            if orders.filter(is_paid=True).exists() else 0
        remaining = total_sales - paid_value
        diviner = total_sales if total_sales > 0 else 1
        paid_percent, remain_percent = round(
            (paid_value/diviner)*100, 1), round((remaining/diviner)*100, 1)
        total_sales =  returnSTRcurrency( total_sales )
        paid_value =  returnSTRcurrency( paid_value )
        remaining = returnSTRcurrency( remaining )
        orders = OrderTable(orders)
        RequestConfig(self.request).configure(orders)
        context.update(locals())
        return context


@staff_member_required
def auto_create_order_view(request):
    logged_user = request.user
    user_obj = get_object_or_404(User, username=logged_user)
    requestor_obj = get_object_or_404(Profile, user=user_obj)

    new_order = Order.objects.create(
        title='Orden Globalfruits',
        date=datetime.datetime.now(),
        requestor=requestor_obj
    )
    new_order.title = new_order.title = 'Orden Num:{} Creada por:{}'.format(
        new_order.id, logged_user)
    new_order.save()
    return redirect(new_order.get_edit_url())


@method_decorator(staff_member_required, name='dispatch')
class OrderListView(ListView):
    template_name = 'list.html'
    model = Order
    paginate_by = 50

    def get_queryset(self):
        print("get_queryset ")
        qs = Order.objects.all()
        if self.request.GET:
            qs = Order.filter_data(self.request, qs)
            # print("qs: ", qs)
            # if not qs:
            #     print(" qs is null")
            #     print("self.request: ", self.request)

            #     qs = Order.filter_data(self.request, qs)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = OrderTable(self.object_list)
        RequestConfig(self.request).configure(orders)
        context.update(locals())
        return context


@staff_member_required
def ajax_calculate_results_view(request):
    orders = Order.filter_data(request, Order.objects.all())
    total_value, total_paid_value, remaining_value, data = 0, 0, 0, dict()
    if orders.exists():
        total_value = orders.aggregate(Sum('final_value'))['final_value__sum']
        total_paid_value = orders.filter(is_paid=True).aggregate(Sum('final_value'))['final_value__sum'] if\
            orders.filter(is_paid=True) else 0
        remaining_value = total_value - total_paid_value
        total_value, total_paid_value, remaining_value = returnSTRcurrency(total_value) ,returnSTRcurrency(total_paid_value) , returnSTRcurrency(remaining_value)

    data['result'] = render_to_string(template_name='include/result_container.html',
                                      request=request,
                                      context=locals())
    return JsonResponse(data)


@method_decorator(staff_member_required, name='dispatch')
class CreateOrderView(CreateView):
    template_name = 'form.html'
    form_class = OrderCreateForm
    model = Order

    def get_success_url(self):
        self.new_object.refresh_from_db()
        return reverse('update_order', kwargs={'pk': self.new_object.id})

    def form_valid(self, form):
        print("form: ", form)
        object = form.save()
        print("object: ", object)
        object.refresh_from_db()
        self.new_object = object
        return super().form_valid(form)


@method_decorator(staff_member_required, name='dispatch')
class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'order_update.html'
    form_class = OrderEditForm

    def get_success_url(self):
        return reverse('update_order', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object
        qs_p = Product.objects.filter(active=True)[:12]
        products = ProductTable(qs_p)
        order_items = OrderItemTable(instance.order_items.all())
        RequestConfig(self.request).configure(products)
        RequestConfig(self.request).configure(order_items)
        context.update(locals())
        return context


@staff_member_required
def ajax_search_products(request, pk):
    instance = get_object_or_404(Order, id=pk)
    q = request.GET.get('q', None)
    print("q: ", q)
    if q:
        products = Product.broswer.active()
        products = list(filter(lambda x: (x.title.upper().count(q.upper()) > 0 ), products))   
    else:
        products = Product.broswer.active()

    products = products[:12]
    products = ProductTable(products)
    RequestConfig(request).configure(products)
    data = dict()
    data['products'] = render_to_string(template_name='include/product_container.html',
                                        request=request,
                                        context={
                                            'products': products,
                                            'instance': instance
                                        })
    return JsonResponse(data)


@staff_member_required
def ajax_add_product(request, pk, dk):
    instance = get_object_or_404(Order, id=pk)
    product = get_object_or_404(Product, id=dk)
    order_item, created = OrderItem.objects.get_or_create(
        order=instance, product=product)
    if created:
        order_item.qty = 1
        order_item.price = product.value
        order_item.discount_price = product.discount_value
    else:
        order_item.qty += 1
    order_item.save()
    product.qty -= 1
    product.save()
    instance.refresh_from_db()
    order_items = OrderItemTable(instance.order_items.all())
    RequestConfig(request).configure(order_items)
    data = dict()
    data['result'] = render_to_string(template_name='include/order_container.html',
                                      request=request,
                                      context={'instance': instance,
                                               'order_items': order_items
                                               }
                                      )
    return JsonResponse(data)


@staff_member_required
def ajax_modify_order_item(request, pk, action):
    order_item = get_object_or_404(OrderItem, id=pk)
    product = order_item.product
    instance = order_item.order
    if action == 'remove':
        order_item.qty -= 1
        product.qty += 1
        if order_item.qty < 1:
            order_item.qty = 1
    if action == 'add':
        order_item.qty += 1
        product.qty -= 1
    product.save()
    order_item.save()
    if action == 'delete':
        order_item.delete()
    data = dict()
    instance.refresh_from_db()
    order_items = OrderItemTable(instance.order_items.all())
    RequestConfig(request).configure(order_items)
    data['result'] = render_to_string(template_name='include/order_container.html',
                                      request=request,
                                      context={
                                          'instance': instance,
                                          'order_items': order_items
                                      }
                                      )
    return JsonResponse(data)


@staff_member_required
def delete_order(request, pk):
    instance = get_object_or_404(Order, id=pk)
    instance.delete()
    messages.warning(request, 'The order is deleted!')
    return redirect(reverse('homepage'))


@staff_member_required
def done_order_view(request, pk):
    instance = get_object_or_404(Order, id=pk)
    #instance.is_paid = True
    instance.save()
    return redirect(reverse('homepage'))


@staff_member_required
def ajax_calculate_category_view(request):
    orders = Order.filter_data(request, Order.objects.all())
    order_items = OrderItem.objects.filter(order__in=orders)
    category_analysis = order_items.values_list('product__category__title').annotate(qty=Sum('qty'),
                                                                                     total_incomes=Sum(
                                                                                         'total_price')
                                                                                     )
    data = dict()
    category, currency = True, CURRENCY
    data['result'] = render_to_string(template_name='include/result_container.html',
                                      request=request,
                                      context=locals()
                                      )
    return JsonResponse(data)
