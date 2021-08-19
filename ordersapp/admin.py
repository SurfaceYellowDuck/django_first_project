from django.contrib import admin
from .models import OrderItem, Order

# admin.site.register(Order)


@admin.register(OrderItem)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'order',
        'quantity',
    ]

@admin.register(Order)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'created',
        'update',
        'is_active',
        'status',
    ]
# Register your models here.
