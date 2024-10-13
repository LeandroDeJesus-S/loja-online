from django.contrib import admin

from .models import Product, Category, ProductVariation
from store.models import StoreHasProductVariation
from mediafiles.models import MediaFile


class FileInline(admin.TabularInline):
    model = MediaFile
    extra = 1
    exclude = ['evaluation']


class VariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1
    verbose_name = 'Variação'
    verbose_name_plural = 'Variações'


class CategoryInline(admin.TabularInline):
    model = Product.categories.through
    extra = 1
    verbose_name = 'Categoria'
    verbose_name_plural = 'Categorias'


class StoreInline(admin.TabularInline):
    model = StoreHasProductVariation
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "thumbnail",
    ]
    inlines = [VariationInline, CategoryInline]
    exclude = ["variations", "categories"]


@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "size",
        "color",
        "price",
    ]
    inlines = [StoreInline, FileInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
