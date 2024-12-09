from django.contrib import admin
from .models import (
    Product,
    ProductVariationFile,
    ProductVariationOption,
    ProductVariationOptionData,
)


class ProductInline(admin.TabularInline):
    model = Product
    exclude = ()
    extra = 1


class VariationOptionInline(admin.TabularInline):
    model = ProductVariationOption
    exclude = ()
    extra = 1


class ProductCategoryInline(admin.TabularInline):
    model = Product.categories.through
    exclude = ()
    extra = 1


class VariationFileInline(admin.TabularInline):
    model = ProductVariationFile
    exclude = ()
    extra = 1


class VariationOptionDataInline(admin.StackedInline):
    model = ProductVariationOptionData
    exclude = ()
    extra = 1
