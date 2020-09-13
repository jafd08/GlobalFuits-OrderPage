from django.urls import path
from . import views
from .views import  (client_ajax_input_modify, PricesView, Client_OrderUpdateView, CreateOrderView, ajax_search_products, ajax_add_product, ajax_modify_order_item, client_done_order_view, OrderListView)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('misPedidos/', OrderListView.as_view(), name='myOrders_name'),
    path('crearPedido/', login_required(CreateOrderView.as_view()), name='client_create_order'),
    path('precios/', PricesView, name='client_prices'),
    path('gestionar/<int:pk>/', login_required(Client_OrderUpdateView.as_view()), name='client_update_order'),
    # path('<int:product_id>', views.detail, name='detailName'),
    # path('<int:product_id>/upvote', views.upvote, name='upvoteName'),
    path('ajax/search-products/<int:pk>/', ajax_search_products, name='client_ajax-search'),
    path('ajax/add-product/<int:pk>/<int:dk>/', ajax_add_product, name='client_ajax_add'),
    path('ajax/modify-product/<int:pk>/<slug:action>', ajax_modify_order_item, name='client_ajax_modify'),
    path('done/<int:pk>', client_done_order_view, name='client_done_order'),
    path('done/<int:pk>/<str:addt_comments>', client_done_order_view, name='client_done_order2'),
    path('ajax/modify-product/<int:pk>/<slug:action>/<slug:qty_float>', client_ajax_input_modify, name='client_ajax_input_modify'),
              ]
