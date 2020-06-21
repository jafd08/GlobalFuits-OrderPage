from django.urls import path
from . import views
from .views import  (OrderUpdateView, CreateOrderView)
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('create/', views.create, name='createName'),
    path('misPedidos/', views.myOrders, name='myOrders_name'),
    path('crearPedido/', login_required(CreateOrderView.as_view()), name='client_create_order'),
    path('actualizar/<int:pk>/', login_required(OrderUpdateView.as_view()), name='client_update_order'),
    # path('<int:product_id>', views.detail, name='detailName'),
    # path('<int:product_id>/upvote', views.upvote, name='upvoteName'),
              ]
