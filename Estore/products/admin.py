from django.contrib import admin

from .models import Product, Category, ProductVariation


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'price', 'stock', 'thumbnail',
    ]


@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'size', 'color',
    ]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]
