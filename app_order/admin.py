from django.contrib import admin
from app_order.models import Order, Status

# Register your models here.

admin.site.register(Order)
admin.site.register(Status)