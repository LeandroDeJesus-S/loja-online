from django.contrib import admin
from .models import OrderStatus, Order


@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'qtd',
        'created_at',
        'status',
        'user',
        'product_variation',
        'value'
    ]

    @admin.display(description='Valor')
    def value(self, obj: Order):
        """returns the value of the order"""
        return obj.qtd * obj.product_variation.price
