from django.contrib import admin
from .models import CustomerOrders, OrderDeliveryStatus
# Register your models here.

admin.site.register(CustomerOrders)
admin.site.register(OrderDeliveryStatus)
