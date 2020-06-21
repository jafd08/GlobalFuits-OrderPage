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
    print("excel_filename.excel_file: ", excel_filename.excel_file)
    return render(request, 'app_client/home.html', {'excel_file_name': excel_filename.excel_file, 'products':products})


def myOrders(request):
    return render(request, 'app_client/home.html')


@login_required
def create(request):
    #return render(request, 'app_client/create.html')
    if request.method == 'POST':
        if request.POST['value'] and request.POST['products']:
            logged_user = request.user
            user_obj = get_object_or_404(User, username=logged_user)
            requestor_obj = get_object_or_404(Profile, user=user_obj)
            ## continue from here...

            new_order = Order()
            new_order.requestor = requestor_obj
            print(requestor_obj)
            print(requestor_obj.fullname)
            new_order.title = "Pedido para " + requestor_obj.Profile.fullname
            #checkear si es requestor_obj.Profile.fullname , o requestor_obj.fullname ...

            #we need to add the products here...

            new_order.save()
            # product = Product()
            # product.title = request.POST['title']
            # product.body = request.POST['body']
            # 
            # if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
            #     product.url = request.POST['url']
            # else:
            #     product.url = 'http://' + request.POST['url']

            # product.icon = request.FILES['icon']
            # product.image = request.FILES['image']
            # product.pub_date = timezone.datetime.now()
            # product.votes_total = 1
            # product.hunter = request.user
            # product.save()
            Vote_objects = Vote(product=Product.objects.get(title=str(product)), voter=request.user)
            Vote_objects.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'app_client/create.html', {'error': 'All fields are required'})
    else:
        return render(request, 'app_client/create.html')

#
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
    data['result'] = render_to_string(template_name='include/order_container.html',
                                      request=request,
                                      context={'instance': instance,
                                               'order_items': order_items
                                               }
                                    )
    return JsonResponse(data)



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
        print("get_success_url")
        self.new_object.refresh_from_db()
        return reverse('client_update_order', kwargs={'pk': self.new_object.id})

    def form_valid(self, form):
        logged_user = self.request.user
        user_obj = get_object_or_404(User, username=logged_user)
        requestor_obj = get_object_or_404(Profile, user=user_obj)
        #aqui le enviamos el requestor obj al new order...

        form.instance.requestor = requestor_obj

        object = form.save()
        #object.requestor = requestor_obj
        object.refresh_from_db()
        self.new_object = object
        return super().form_valid(form)


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'client_order_update.html'
    form_class = OrderEditForm

    def get_success_url(self):
        return reverse('client_update_order', kwargs={'pk': self.object.id})

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



"""" HERE ARE THE CLIENT VIEW MY ORDERS"""