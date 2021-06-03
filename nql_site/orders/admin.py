from django.contrib import admin

from .models import Order, OrderMeta, Photo

admin.site.register(Order)
admin.site.register(OrderMeta)
admin.site.register(Photo)
