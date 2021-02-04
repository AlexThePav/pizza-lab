from django.contrib import admin

from pizzalabapp.models import Order, OrderItem

admin.site.register(Order)
admin.site.register(OrderItem)
