from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Precios_Excel
from app_product.models import Product
from app_order.models import Order,OrderItem, CURRENCY
from app_accounts.models import Profile
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils import timezone


"""" CREATE ORDER IMPORTS"""
from django.views.generic import ListView, CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import reverse
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Sum
from django_tables2 import RequestConfig
from .forms import OrderCreateForm, OrderEditForm
from .tables import ProductTable, OrderItemTable, OrderTable
from django.contrib.auth.mixins import PermissionRequiredMixin
from django import forms

# Create your views here.

def home(request):
    products = Product.objects
    excel_filename = get_object_or_404(Precios_Excel, nombre="precios")
    #print("excel_filename.excel_file: ", excel_filename.excel_file)
    user_firstname = " "

    try:
        logged_user = request.user
        user_obj = get_object_or_404(User, username=logged_user)
        requestor_obj = get_object_or_404(Profile, user=user_obj)
        fullname_splitted = requestor_obj.fullname.split()

        user_firstname = fullname_splitted[0]

    except:
        print("no logged in user")

    return render(request, 'app_client/home.html', {'excel_file_name': excel_filename.excel_file, 'products':products, "user_firstname":user_firstname})

def PricesView(request):
    products = Product.objects
    excel_filename = get_object_or_404(Precios_Excel, nombre="precios")
    #print("excel_filename.excel_file: ", excel_filename.excel_file)
    user_firstname = " "

    try:
        logged_user = request.user
        user_obj = get_object_or_404(User, username=logged_user)
        requestor_obj = get_object_or_404(Profile, user=user_obj)
        fullname_splitted = requestor_obj.fullname.split()

        user_firstname = fullname_splitted[0]

    except:
        print("no logged in user")

    return render(request, 'app_client/precios.html', {'excel_file_name': excel_filename.excel_file, 'products':products, "user_firstname":user_firstname})


@login_required
def myOrders(request):
    return render(request, 'app_client/home.html')


# def detail(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)
#     return render(request, 'app_client/detail.html', {'product': product})
#
#
# @login_required(login_url="/accounts/signup")

"""" HERE ARE THE CLIENT CREATE ORDER ... """

@login_required
def ajax_add_product(request, pk, dk):
    instance = get_object_or_404(Order, id=pk)
    product = get_object_or_404(Product, id=dk)
    order_item, created = OrderItem.objects.get_or_create(order=instance, product=product)
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
    data['result'] = render_to_string(template_name='app_client/include/client_order_container.html',
                                      request=request,
                                      context={'instance': instance,
                                               'order_items': order_items
                                               }
                                    )
    return JsonResponse(data)

@login_required
def ajax_search_products(request, pk):
    instance = get_object_or_404(Order, id=pk)
    q = request.GET.get('q', None)
    products = Product.broswer.active().filter(title__startswith=q) if q else Product.broswer.active()
    products = products[:12]
    products = ProductTable(products)
    RequestConfig(request).configure(products)
    data = dict()
    data['products'] = render_to_string(template_name='app_client/include/product_container.html',
                                        request=request,
                                        context={
                                            'products': products,
                                            'instance': instance
                                        })
    return JsonResponse(data)


@login_required
def ajax_modify_order_item(request, pk, action):
    order_item = get_object_or_404(OrderItem, id=pk)
    product = order_item.product
    instance = order_item.order
    if action == 'remove':
        order_item.qty -= 1
        product.qty += 1
        if order_item.qty < 1: order_item.qty = 1
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
    data['result'] = render_to_string(template_name='app_client/include/client_order_container.html',
                                      request=request,
                                      context={
                                          'instance': instance,
                                          'order_items': order_items
                                      }
                                      )
    return JsonResponse(data)

@login_required
def delete_order(request, pk):
    instance = get_object_or_404(Order, id=pk)
    instance.delete()
    messages.warning(request, 'La orden ha sido eliminada!')
    return redirect(reverse('home'))


@login_required
def done_order_view(request, pk):
    instance = get_object_or_404(Order, id=pk)
    instance.is_paid = True
    instance.save()
    return redirect(reverse('home'))

class CreateOrderView(CreateView):

    template_name = 'client_form.html'
    form_class = OrderCreateForm
    #https://www.google.com/search?client=opera&hs=UBk&sxsrf=ALeKk02KdHk_3elPKEGVYFPBHKqe31BZog%3A1592274944881&ei=ADDoXv75NPOEwbkPs8almAo&q=django+hide+form+choicefield+&oq=django+hide+form+choicefield+&gs_lcp=CgZwc3ktYWIQAzIICCEQFhAdEB46BAgAEEc6BggAEBYQHjoECCMQJzoFCAAQywE6CAgAEBYQChAeUKjUA1jf8wNgx_QDaABwAXgAgAGmAYgB6BKSAQQwLjE4mAEAoAEBqgEHZ3dzLXdpeg&sclient=psy-ab&ved=0ahUKEwj--eSzpoXqAhVzQjABHTNjCaMQ4dUDCAs&uact=5
    # https://docs.djangoproject.com/en/2.2/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.get_form_kwargs
    #https://www.google.com/search?sxsrf=ALeKk03JnyNgb7Fa8eh-6tEqONR9Pzi7Aw%3A1592613546882&ei=qlrtXrqpNcHk_Abhl4n4Cg&q=pass+model+object+to+class+based+view+django&oq=pass+model+object+to+class+based+view+django&gs_lcp=CgZwc3ktYWIQAzIECCEQCjoECAAQR1CI6gtYt_QLYPf0C2gAcAJ4AIABlQGIAdoKkgEEMC4xMZgBAKABAaoBB2d3cy13aXo&sclient=psy-ab&ved=0ahUKEwi6puflk4_qAhVBMt8KHeFLAq8Q4dUDCAw&uact=5
    #form_class = OrderCreateForm(initial={'requestor': "sdada"}) #en vez de esto, se esconde el field de form  y en form_valid se envia el perfil

    model = Order

    # https://stackoverflow.com/questions/54275970/how-to-pass-database-queryset-objects-from-class-based-viewsclass-signupgeneri

    def get_context_data(self, **kwargs):

        context = super(CreateOrderView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        self.new_object.refresh_from_db()
        return reverse('client_update_order', kwargs={'pk': self.new_object.id})

    def form_valid(self, form):
        logged_user = self.request.user
        user_obj = get_object_or_404(User, username=logged_user)
        requestor_obj = get_object_or_404(Profile, user=user_obj)
        #aqui le enviamos el requestor obj al new order...
        now = timezone.now().date()
        order_date = form.instance.date

        was_orderdate_before_now = order_date < now
        if was_orderdate_before_now:
            # try once with an old date.. then with a current date and then with future date
            return render(self.request, 'client_form.html', {'error': 'La fecha del pedido no puede ser en el pasado ni hoy!', "form": form})

        form.instance.requestor = requestor_obj

        object = form.save()
        #object.requestor = requestor_obj
        object.refresh_from_db()
        self.new_object = object
        return super().form_valid(form)


class Client_OrderUpdateView(UpdateView):
    model = Order
    template_name = 'client_order_update.html'
    form_class = OrderEditForm

    def get_success_url(self):
        return reverse('client_update_order', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = self.object
        queryset_products = Product.objects.filter(active=True)[:12]
        products = ProductTable(queryset_products)
        order_items = OrderItemTable(instance.order_items.all())
        RequestConfig(self.request).configure(products)
        RequestConfig(self.request).configure(order_items)
        context.update(locals())
        return context

@login_required
def client_done_order_view(request, pk, addt_comments=" No hay comentarios"):

    instance = get_object_or_404(Order, id=pk)

    print("addt_comments: ", addt_comments)
    if (addt_comments != "0"):
        print("addt comments doesnt equals 0 ... saving addt here")
        instance.comments = addt_comments

    #instance.is_paid = True
    instance.save()
    return redirect(reverse('myOrders_name'))

class OrderListView(ListView):
    template_name = 'client_latest_orders.html'
    model = Order
    paginate_by = 50

    def get_queryset(self):
        qs = Order.objects.all()
        logged_user = self.request.user
        user_obj = get_object_or_404(User, username=logged_user)
        requester_obj = get_object_or_404(Profile, user=user_obj)
        qs_of_logged_user= Order.objects.filter(requestor=requester_obj).all()
        #qs_of_logged_user = Order.objects.get(requestor=requester_obj).all()

        if self.request.GET:
            qs_of_logged_user = Order.filter_data(self.request, qs_of_logged_user)
        return qs_of_logged_user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = OrderTable(self.object_list)
        RequestConfig(self.request).configure(orders)
        context.update(locals())
        return context
"""" HERE ARE THE CLIENT VIEW MY ORDERS"""



@login_required
def client_ajax_input_modify(request, pk ,action, qty_float):
    #print("INTO client_ajax_input_modify")
    order_item = get_object_or_404(OrderItem, id=pk)
    product = order_item.product
    instance = order_item.order

    #print("qty_float: ", qty_float)
    qty_float = qty_float.replace("-", ".")
    qty_float = float(qty_float)
    #print("qty_float: ", qty_float)



    if action == 'modify':
        order_item.qty = qty_float
        product.qty = qty_float

    product.save()
    order_item.save()

    if action == 'delete':
        order_item.delete()
    data = dict()
    instance.refresh_from_db()
    order_items = OrderItemTable(instance.order_items.all())
    RequestConfig(request).configure(order_items)
    data['result'] = render_to_string(template_name='app_client/include/client_order_container.html',
                                      request=request,
                                      context={
                                          'instance': instance,
                                          'order_items': order_items
                                      }
                                      )
    return JsonResponse(data)
