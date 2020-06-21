"""blog_pos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# from app_order.views import (HomepageView, OrderUpdateView, CreateOrderView, delete_order,
#                          OrderListView, done_order_view, auto_create_order_view,
#                          ajax_add_product, ajax_modify_order_item, ajax_search_products, ajax_calculate_results_view,
#                          order_action_view, ajax_calculate_category_view
#                          )
#order_action_view is not found . Removing it.
from app_order.views import (HomepageView, OrderUpdateView, CreateOrderView, delete_order,
                         OrderListView, done_order_view, auto_create_order_view,
                         ajax_add_product, ajax_modify_order_item, ajax_search_products, ajax_calculate_results_view,
                          ajax_calculate_category_view)

#from app_client.views import (home, create, detail, upvote)
from app_client.views import (home)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_homepage', HomepageView.as_view(), name='homepage'),
    path('', home, name='home'),
    path('client-order/', include('app_client.urls')),
    path('order-list/', OrderListView.as_view(), name='order_list'),
    path('create/', CreateOrderView.as_view(), name='create-order'),
    path('create-auto/', auto_create_order_view, name='create_auto'),
    path('update/<int:pk>/', OrderUpdateView.as_view(), name='update_order'),
    path('done/<int:pk>/', done_order_view, name='done_order'),
    path('delete/<int:pk>/', delete_order, name='delete_order'),
    #path('action/<int:pk>/<slug:action>/', order_action_view, name='order_action'),


    #  ajax_calls
    path('ajax/search-products/<int:pk>/', ajax_search_products, name='ajax-search'),
    path('ajax/add-product/<int:pk>/<int:dk>/', ajax_add_product, name='ajax_add'),
    path('ajax/modify-product/<int:pk>/<slug:action>', ajax_modify_order_item, name='ajax_modify'),
    path('ajax/calculate-results/', ajax_calculate_results_view, name='ajax_calculate_result'),
    path('ajax/calculate-category-results/', ajax_calculate_category_view, name='ajax_category_result'),
    path('accounts/', include('app_accounts.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
