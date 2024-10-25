from django.contrib import admin
from .models import (
    Product,
    ProductVariationFile,
    ProductVariationOption,
)
from .forms import ProductVariationForm


class ProductInline(admin.TabularInline):
    model = Product
    exclude = ()
    extra = 1


class VariationInline(admin.TabularInline):
    model = Product.variations.through
    exclude = ()
    form = ProductVariationForm
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
